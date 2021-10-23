from PIL import Image

def Convert(img, levelPath, pixSize = 1, layer = 0, rewrite = True, levelX = 0, levelY = 0):
    offset = 1 - pixSize
    
    #img = Image.open(imagePath).convert('RGBA')
    pixels = img.load()
    
    if rewrite:
        level = open(levelPath, "w", encoding = "utf-8")
        lastObj = 0
        level.write("0;1;1;808080FF;15;;;;;\n")
    else:
        level = open(levelPath, "r+", encoding = "utf-8")
        lastline = level.readlines()[-1]
        lastlinearray = lastline.split(";")
        lastObj = int(lastlinearray[1]) + 1
        
    try:
        img.mode = "RGBA"
        isPng = True
    except:
        isPng = False
        
    i = 0
    for y in range(0, img.size[1]):
        for x in range(0, img.size[0]):
            
            red = pixels[x, img.size[1] - 1 - y][0]
            green = pixels[x, img.size[1] - 1 - y][1]
            blue = pixels[x, img.size[1] - 1 - y][2]
            
            if isPng:
                alpha = pixels[x, img.size[1] - 1 - y][3]
            else:
                alpha = 255

            if alpha < 20:
                continue
            
            color = ('%02x%02x%02x%02x' % (red, green, blue, alpha)).upper()
            
            level.write("20;" + str(lastObj + 1 + i) + ";" + str(levelX + x - (x * offset)).replace(".", ",") + ";" + str(levelY + y + 1 - img.size[1] * pixSize- (y * offset)).replace(".", ",") + ";" + str(pixSize).replace(".", ",") + ";" + str(pixSize).replace(".", ",") + ";;C;" + color + ";" + str(layer) + ";C;\n")
            lastObj += 1

def pictureToText(img, levelPath, size, levelX = 0, levelY = 0, rewrite = False):
    imgData = img.load()
    if rewrite:
        level = open(levelPath, "w")
        lastObj = 0
        level.write("0;1;1;808080FF;15;;;;;\n")
    else:
        level = open(levelPath, "r+")
        lastObj = int(level.readlines()[-1].split(";")[1])
    #дико извиняюсь.
    string = "<size=0>made by gstroin"
    string += "<size=" + str(size) + ">"
    for y in range(0, img.size[1]):
        for x in range (0, img.size[0]):
            red = imgData[x, y][0]
            green = imgData[x, y][1]
            blue = imgData[x, y][2]
            alpha = imgData[x, y][3]
            hexColor = "%02x%02x%02x%02x" % (red, green, blue, alpha)
            string += "<color=#" + hexColor + "><mark=#" + hexColor + ">q<sub>q</sub>"
        string += "<br>"
    level.write("17;" + str(lastObj + 1) + ";" + str(levelX) + ";" + str(levelY) + ";1;1;;¶;" + string + ";¶;\n")
    lastObj += 1
    return string
