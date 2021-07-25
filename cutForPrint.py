import PIL
from PIL import Image

PIL.Image.MAX_IMAGE_PIXELS = 12331200000


def cut(im, w, h, outputFolder="png"):
    imgwidth, imgheight = im.size
    iw = imgwidth // w
    ih = imgheight // h
    c = 0
    for i in range(h):
        for j in range(w):
            area = (iw * j, ih * i, iw * (j + 1), ih * (i + 1))
            o = im.crop(area)
            o.save(f"{outputFolder}/{c:03}.png")
            c += 1


if __name__ == "__main__":
    im = PIL.Image.open("resultmap.png")
    cut(im, 6, 5)
