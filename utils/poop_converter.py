#created by tttpm.
#poorly opimized converter
from PIL import Image

class Color:

    def __init__(self, r, g, b, a = 255, tol = 0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.tol = tol

    def tuple(self):
        return (self.r, self.g, self.b, self.a)
    
    def __eq__(self, other):
        first, second = self.tuple(), other.tuple()
        return all(abs(first[i] - second[i]) <= self.tol for i in range(4))

    def to_hex(self, full = False):
        color = self.tuple()
        if color[-1] == 255:
            color = color[:-1]
        fres = ""
        sres = ""
        for c in color:
            f, s = tuple("{:02x}".format(c))
            fres += f + s
            if f == s:
                sres += f

        return (fres if full or len(sres) < len(color) else sres)

    def __len__(self):
        return len(self.to_hex())

class Rect():
    
    def __init__(self, x, y, width, height, color):
        self.x = x 
        self.y = y    
        self.width = width
        self.height = height
        self.color = color

    def totr(self, index, layer, pix_size, lvl_x, lvl_y):
        return f"20;{index};{str(lvl_x  + pix_size * (self.x + ((self.width - 1) / 2))).replace('.',',')};{str(lvl_y  + pix_size * (self.y + ((self.height - 1) / 2))).replace('.',',')};{str(self.width * pix_size).replace('.',',')};{str(self.height * pix_size).replace('.', ',')};;C;{self.color.to_hex()};{layer};C;"
    

    @classmethod
    def cut_matrix(cls, matrix):
        res = []
        rs = len(matrix)
        cs = len(matrix[0])
        
        used = [[0] * cs for _ in range(rs)]
        
        for i in range(rs):
            
            for j in range(cs):
                
                if not used[i][j]:
                    
                    cur_max = [1, 1]
                    
                    k = 0
                    l_min = cs + 1
                    while i + k < rs and matrix[i+k][j] == matrix[i][j] and not used[i+k][j]:
                        l = 0
                        cur = [k+1, 0]
                        while j + l < cs and l < l_min and matrix[i + k][j + l] == matrix[i][j] and not used[i+k][j+l]:
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

        
def to_blocks(img, level_path, pix_size = 1, layer = 0, rewrite = True, level_x = 0, level_y = 0, tol = 0):
    
    pixels = img.load()
    
    if rewrite:
        level = open(level_path, "w", encoding = "utf-8")
        ind = 0
        level.write("0;1;1;808080FF;15;;;;;\n")
    else:
        level = open(level_path, "r+", encoding = "utf-8")
        lastline = level.readlines()[-1]
        lastlinearray = lastline.split(";")
        ind = int(lastlinearray[1]) + 1        
   
    matrix = []
    for i in range(img.size[1]):
        matrix.append([])
        for j in range(img.size[0]):
            matrix[-1].append(Color(*pixels[j, img.size[1] - i - 1], tol=tol))
            
    optimized = Rect.cut_matrix(matrix)
    for rect in optimized:
        level.write(rect.totr(ind, layer, pix_size, level_x, level_y) + "\n")

    level.close()

def to_text(img, level_path, size, level_x = 0, level_y = 0, rewrite = False, tol = 0, close_all_tags = False, stack_size = 10):
    img_data = img.load()
    
    if rewrite:
        level = open(level_path, "w", encoding="utf-8")
        last_obj = 0
        level.write("0;1;1;808080FF;15;;;;;\n")
    else:
        level = open(level_path, "r+", encoding="utf-8")
        last_obj = int(level.readlines()[-1].split(";")[1])
        
    string = ""
    string += "<size=" + str(size) + ">"
    
    color_stack = []
    ctcnt = 0
    closing_tags = "</color></mark>"
    
    for y in range(0, img.size[1]):
        for x in range(0, img.size[0]):
            color = Color(*img_data[x, y], tol=tol)
            if color not in color_stack:
                ctcnt += 1
                color_stack.append(color)
                string += f"<#{color.to_hex()}><mark=#{color.to_hex(1)}>"
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
            
    string += closing_tags * (ctcnt * close_all_tags)
    if close_all_tags:
        string += "</size>"
    level.write("17;" + str(last_obj + 1) + ";" + str(level_x) + ";" + str(level_y) + ";1;1;;¶;" + string + ";¶;\n")
    level.close()
    last_obj += 1
    return string