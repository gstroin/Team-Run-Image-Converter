#POorly OPtimized converter

from PIL import Image

import utils.image_converter
import utils.map_parser

class Color:

    def __init__(self, r, g, b, a = 255, tol = 0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.tol = tol

    def tuple(self) -> tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)
    
    def __eq__(self, other):
        firowst, second = self.tuple(), other.tuple()
        return all(abs(firowst[i] - second[i]) <= self.tol for i in range(4))

    def get_hex(self, full: bool = False) -> str:
        return utils.image_converter.get_hex(self.r, self.g, self.b, self.a, full)

    def __len__(self):
        return len(self.get_hex())



class Rect():
    
    def __init__(self, x: float, y: float, width: float, height: float, color: Color):
        self.x = x 
        self.y = y    
        self.width = width
        self.height = height
        self.color = color

    def totr(self, index: int, layer: int, pix_size: float, lvl_x: float, lvl_y: float):
        return f"20;{index};{str(lvl_x  + pix_size * (self.x + ((self.width - 1) / 2))).replace('.',',')};{str(lvl_y - pix_size * (self.y + ((self.height - 1) / 2))).replace('.',',')};{str(self.width * pix_size).replace('.',',')};{str(self.height * pix_size).replace('.', ',')};;C;{self.color.get_hex()};{layer};C;"
    

    @classmethod
    def cut_matrix(cls, matrix: list[list[Color]]):
        res = []
        rows = len(matrix)
        cols = len(matrix[0])
        #this algorithm may not be optimal, but i guess it works - tttpm
        used = [[0] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if not used[i][j]:
                    cur_max = [1, 1]
                    k = 0
                    l_min = cols + 1
                    while i + k < rows and matrix[i+k][j] == matrix[i][j] and not used[i+k][j]:
                        l = 0
                        cur = [k+1, 0]
                        while j + l < cols and l < l_min and matrix[i + k][j + l] == matrix[i][j] and not used[i+k][j+l]:
                            l += 1
                        cur[1] = l
                        l_min = min(l_min, l)
                        cur_max = max(cur_max, cur, key = lambda x: x[0] * x[1])
                        k += 1

                    res.append(Rect(j, i, cur_max[1], cur_max[0], matrix[i][j]))
                    for i1 in range(i, i + cur_max[0]):
                        for j1 in range(j, j + cur_max[1]):
                            used[i1][j1] = 1

        return res

    
       
def to_blocks(img: Image.Image, level_path: str, pix_size: float = 1, layer: int = 0, rewrite: bool = True, level_x: float = 0, level_y: float = 0, tol: int = 0):
    if rewrite:
        tres, info, level = utils.map_parser.new_map()
    else:
        tres, info, level = utils.map_parser.open_file(level_path)
    max_id = utils.map_parser.max_id(level)       
   
    matrix: list[list[Color]] = []
    for i in range(img.size[1]):
        matrix.append([])
        for j in range(img.size[0]):
            matrix[-1].append(Color(*img.getpixel((j, i)), tol=tol))
            
    optimized: list[Rect] = Rect.cut_matrix(matrix)
    for rect in optimized:
        level.append(rect.totr(max_id, layer, pix_size, level_x, level_y))
        max_id += 1

    utils.map_parser.save_map((tres, info, level), level_path)



def to_text(img: Image.Image, level_path: str, size: float, level_x: float = 0, level_y: float = 0, rewrite: bool = False, tol: int = 0, close_all_tags: bool = False, stack_size: int = 10):
    if rewrite:
        tres, info, level = utils.map_parser.new_map()
    else:
        tres, info, level = utils.map_parser.open_file(level_path)
    max_id = utils.map_parser.max_id(level)   
        
    string = ""
    string += "<size=" + str(size) + ">"
    
    color_stack = []
    ctcnt = 0
    closing_tags = "</color></mark>"
    #tbh i don't like this code but it works as well... right? - tttpm
    for y in range(0, img.size[1]):
        for x in range(0, img.size[0]):
            color = Color(*img.getpixel((x, y)), tol=tol)
            if color not in color_stack:
                ctcnt += 1
                color_stack.append(color)
                string += f"<#{color.get_hex()}><mark=#{color.get_hex(True)}>"
            else:
                while color_stack[-1] != color:
                    ctcnt -= 1
                    string += closing_tags
                    color_stack.pop()
            if len(color_stack) > stack_size:
                color_stack.pop(0)
            string += "-|"
            
        if y < img.size[1] - 1:
            string += "<br>"
            
    if close_all_tags:
        string += closing_tags * (ctcnt * close_all_tags)
        string += "</size>"
    level.append("17;" + str(max_id) + ";" + str(level_x) + ";" + str(level_y) + ";1;1;;¶;" + string + ";¶;")
    utils.map_parser.save_map((tres, info, level), level_path)
    return string