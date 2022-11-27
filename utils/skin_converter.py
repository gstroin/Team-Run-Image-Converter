from base64 import b64encode, b64decode
from zlib import decompress, compressobj, MAX_WBITS, DEFLATED
from PIL import Image, ImageColor, ImageDraw

def to_image(compressed_skin: str):
    compressed = b64decode(compressed_skin.removeprefix("trSkin1"))
    decompressed = str(decompress(compressed, -MAX_WBITS).decode())

    img = Image.new("RGBA",(20, 18), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)

    width = img.size[0]

    hex_colors = decompressed.split(";")
    colors = []

    for color in hex_colors:
        try:
            colors.append(ImageColor.getcolor("#" + color, "RGBA"))
        except ValueError:
            break
    x = 0
    y = 0
    for color in colors:
        if x == width:
            y += 1
            x = 0         
        draw.point((x, y), color)
        x += 1
    return img

def to_skin(image: Image):
    image = image.convert('RGBA')
    
    size = (20, 18)

    image.thumbnail(size)

    background = Image.new('RGBA', size, (255, 255, 255, 0))
    background.paste(image, (int((background.size[0] - image.size[0]) / 2), int((background.size[1] - image.size[1]) / 2 + 1)))

    image = background
    
    pix = image.load()
    colors = []
    hex_colors = []
    for y in range(0, image.size[1]):
        for x in range (0, image.size[0]):
            red = pix[x,y][0]
            green = pix[x,y][1]
            blue = pix[x, y][2]
            alpha = pix[x, y][3]
            colors.append((red, green, blue, alpha))
    for color in colors:
        hex_colors.append("%02x%02x%02x%02x" % color)
    hex_colors = [x.upper() for x in hex_colors]
    decompressed = ";".join(hex_colors)
    decompressed += ";"
    deflate_compress = compressobj(9, DEFLATED, -MAX_WBITS)
    compressed = deflate_compress.compress(decompressed.encode('utf-8')) + deflate_compress.flush()
    encrypted = b64encode(compressed)
    return "trSkin1" + encrypted.decode()