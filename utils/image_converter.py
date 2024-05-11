from PIL import Image
import utils.skin_converter

SKIN_WIDTH = 20
SKIN_HEIGHT = 18

def to_blocks(img, levelPath, pix_size = 1, layer = 0, rewrite = True, level_x = 0, level_y = 0):
    offset = 1 - pix_size
    
    pixels = img.load()
    
    if rewrite:
        level = open(levelPath, "w", encoding = "utf-8")
        last_obj = 0
        level.write("0;1;1;808080FF;15;;;;;\n")
    else:
        level = open(levelPath, "r+", encoding = "utf-8")
        lastline = level.readlines()[-1]
        lastlinearray = lastline.split(";")
        last_obj = int(lastlinearray[1]) + 1
        
    try:
        img.mode = "RGBA"
        is_rgba = True
    except:
        is_rgba = False
        
    for y in range(0, img.size[1]):
        for x in range(0, img.size[0]):
            
            red = pixels[x, img.size[1] - 1 - y][0]
            green = pixels[x, img.size[1] - 1 - y][1]
            blue = pixels[x, img.size[1] - 1 - y][2]
            
            alpha = pixels[x, img.size[1] - 1 - y][3] if is_rgba else 255

            if alpha < 20:
                continue
            
            color = ('%02x%02x%02x%02x' % (red, green, blue, alpha)).upper()
            
            level.write("20;" + str(last_obj + 1) + ";" + str(level_x + x - (x * offset)).replace(".", ",") + ";" + str(level_y + y + 1 - img.size[1] * pix_size- (y * offset)).replace(".", ",") + ";" + str(pix_size).replace(".", ",") + ";" + str(pix_size).replace(".", ",") + ";;C;" + color + ";" + str(layer) + ";C;\n")
            last_obj += 1
    level.close()

def to_text(img, level_path, size, level_x = 0, level_y = 0, mode = "RGBA", rewrite = False):
    img = img.convert(mode).convert("RGBA")
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
    prev_color = None
    for y in range(0, img.size[1]):
        for x in range(0, img.size[0]):
            color = img_data[x, y]
            hex_values = len(list(val for val in color if val % 17 == 0 or val % 16 == 0))
            hexColor = "%02x%02x%02x%02x" % color
            if color[3] == 255:
                hexColor = hexColor[:6]
            modifiedColor = hexColor
            if hex_values == len(color):
                modifiedColor = hexColor[0:-1:2]
            if prev_color != hexColor:
                string += "<color=#" + modifiedColor + "><mark=#" + hexColor + ">"
                prev_color = hexColor
            string += "-|"
        if y < img.size[1] - 1:
            string += "<br>"
    level.write("17;" + str(last_obj + 1) + ";" + str(level_x) + ";" + str(level_y) + ";1;1;;¶;" + string + ";¶;\n")
    level.close()
    last_obj += 1
    return string

def to_skins16(img: Image.Image, level_path, skin_size = 1, layer = 0, rewrite = True, level_x = 0, level_y = 0):
    
    if rewrite:
        level = open(level_path, "w", encoding = "utf-8")
        ind = 0
        level.write("0;1;1;808080FF;15;;;;;\n")
    else:
        level = open(level_path, "r+", encoding = "utf-8")
        lastline = level.readlines()[-1]
        lastlinearray = lastline.split(";")
        ind = int(lastlinearray[1]) + 1    
    
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
        print(f"67;{ind};{x};{y};{skin_size};{skin_size};;¶;00000000;00000000;0;{skin};¶;C;FFFFFFFF;{layer};C;", file=level)
        ind += 1
    
    level.close()
