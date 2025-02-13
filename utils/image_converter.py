from PIL import Image
import utils.skin_converter
import utils.map_parser

SKIN_WIDTH = 20
SKIN_HEIGHT = 18

def get_hex(r: int, g: int, b: int, a: int = 255, full: bool = False):
    include_alpha = (a != 255)
    if r % 17 == g % 17 == b % 17 == a % 17 == 0 and not full:
        r, g, b, a = map(lambda x : x // 17, (r, g, b, a))
        result = f"{r:x}{g:x}{b:x}"
        if include_alpha:
            result += f"{a:x}"
        return result
    result = f"{r:02x}{g:02x}{b:02x}"
    if include_alpha:
        result += f"{a:02x}"
    return result




def to_blocks(img: Image.Image, level_path: str, pix_size: float = 1, layer: int = 0, rewrite: bool = True, level_x: float = 0, level_y: float = 0) -> None:
    if rewrite:
        tres, info, level = utils.map_parser.new_map()
    else:
        tres, info, level = utils.map_parser.open_file(level_path)
    max_id = utils.map_parser.max_id(level)
        
    for y in range(0, img.size[1]):
        for x in range(0, img.size[0]):
            red, green, blue, alpha = img.getpixel((x, img.size[1] - 1 - y))
            if alpha < 20:
                continue
            color = get_hex(red, green, blue, alpha)
            level.append("20;" + str(max_id) + ";" + str(level_x + x * pix_size).replace(".", ",") + ";" + str(level_y - img.size[1] * pix_size + (y * pix_size)).replace(".", ",") + ";" + str(pix_size).replace(".", ",") + ";" + str(pix_size).replace(".", ",") + ";;C;" + color + ";" + str(layer) + ";C;")
            max_id += 1
    utils.map_parser.save_map((tres, info, level), level_path)



def to_text(img: Image.Image, level_path: str, size, level_x: float = 0, level_y: float = 0, rewrite: bool = False) -> None:
    if rewrite:
        tres, info, level = utils.map_parser.new_map()
    else:
        tres, info, level = utils.map_parser.open_file(level_path)
    max_id = utils.map_parser.max_id(level)

    string = ""
    string += "<size=" + str(size) + ">"
    prev_color = None
    for y in range(0, img.size[1]):
        for x in range(0, img.size[0]):
            red, green, blue, alpha = img.getpixel((x, y))
            modified_color = get_hex(red, green, blue, alpha)
            hex_color = get_hex(red, green, blue, alpha, full=True)
            if prev_color != hex_color:
                string += "<#" + modified_color + "><mark=#" + hex_color + ">"
                prev_color = hex_color
            string += "-|"
        if y < img.size[1] - 1:
            string += "<br>"
    level.append("17;" + str(max_id) + ";" + str(level_x) + ";" + str(level_y) + ";1;1;;¶;" + string + ";¶;")
    utils.map_parser.save_map((tres, info, level), level_path)
    return string



def to_skins16(img: Image.Image, level_path: str, skin_size: float = 1, layer: int = 0, rewrite: bool = True, level_x: float = 0, level_y: float = 0):
    if rewrite:
        tres, info, level = utils.map_parser.new_map()
    else:
        tres, info, level = utils.map_parser.open_file(level_path)
    max_id = utils.map_parser.max_id(level) 
    
    pwidth = img.width
    if pwidth % 16 != 0:
        pwidth += 16 - (pwidth % 16)

    pheight = img.height
    if pheight % 16 != 0:
        pheight += 16 - (pheight % 16)
        
    pad = Image.new('RGBA', (pwidth, pheight))
    pad.paste(img)
    img = pad

    images = []
    for y in range(0, img.height, 16):
        for x in range(0, img.width, 16):
            images.append((x // 16, (img.width - y) // 16, img.crop((x, y, x + 16, y + 16))))

    final_height = (img.height // 16) * skin_size
    for image in images:
        imx, imy, img_ = image
        x = (imx * skin_size) + level_x
        y = (imy * skin_size) + level_y - final_height
        skin = utils.skin_converter.to_skin(img_)
        level.append(f"67;{max_id};{x};{y};{skin_size};{skin_size};;¶;00000000;00000000;0;{skin};¶;C;FFFFFFFF;{layer};C;")
        max_id += 1
    
    utils.map_parser.save_map((tres, info, level), level_path)
