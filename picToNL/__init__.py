from PIL import Image

im = Image.open("img.png")
pix = im.load()
width = im.width
height = im.height
print(width)
print(height)
txt = []
for x in range(width):
    for y in range(height):
        pixel = pix[x, y][0] + pix[x, y][1] + pix[x, y][2]
        if pixel == 0:
            txt.append('■')
        else:
            txt.append('□')
    print(txt)
    txt = []