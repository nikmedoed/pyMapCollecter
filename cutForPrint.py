import PIL
from PIL import Image

PIL.Image.MAX_IMAGE_PIXELS = 12331200000

im = PIL.Image.open("resultmap.png")
imgwidth, imgheight = im.size

w, h = 6, 6 # how many parts
iw = imgwidth // w
ih = imgheight // h

c = 0
for i in range(h):
    for j in range(w):
        area = (iw * j, ih * i, iw *( j +1 ), ih *( i +1))
        o = im.crop(area)
        o.save(f"png/{c:03}.png")
        c +=1