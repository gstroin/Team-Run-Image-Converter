import base64
import zlib
from PIL import Image, ImageColor, ImageDraw

def toPNG(compressedSkin):
    compressed = base64.b64decode(compressedSkin.replace("trSkin1", ""))
    decompressed = str(zlib.decompress(compressed, -zlib.MAX_WBITS).decode())

    img = Image.new("RGBA",(20, 18), (0,0,0,0))

    draw = ImageDraw.Draw(img)

    width = img.size[0]
    height = img.size[1]


    hexColorsList = decompressed.split(";")
    colorList = []

    for color in hexColorsList:
        try:
            colorList.append(ImageColor.getcolor("#" + color, "RGBA"))
        except ValueError:
            break
    x = 0
    y = 0
    for color in colorList:
        xTimes = 0
        yTimes = 0
        if x == width:
            y += 1
            x = 0         
        draw.point((x, y), color)
        x += 1
    return img

def toTR(image):
    image = image.convert('RGBA')
    
    size = (20, 18)

    image.thumbnail(size)

    background = Image.new('RGBA', size, (255, 255, 255, 0))
    background.paste(image, (int((background.size[0] - image.size[0]) / 2), int((background.size[1] - image.size[1]) / 2 + 1)))

    image = background
    
    pix = image.load()
    colorList = []
    hexColorList = []
    for y in range(0, image.size[1]):
        for x in range (0, image.size[0]):
            red = pix[x,y][0]
            green = pix[x,y][1]
            blue = pix[x, y][2]
            alpha = pix[x, y][3]
            colorList.append((red,green,blue,alpha))
    for color in colorList:
        hexColorList.append("%02x%02x%02x%02x" % color)
    hexColorList = [x.upper() for x in hexColorList]
    decompressed = ";".join(hexColorList)
    decompressed += ";"
    deflate_compress = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    compressed = deflate_compress.compress(decompressed.encode('utf-8')) + deflate_compress.flush()
    encrypted = base64.b64encode(compressed)
    return "trSkin1" + encrypted.decode()


                     





