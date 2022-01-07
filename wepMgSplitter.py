#!/usr/bin/env python3

from sys import argv
from PIL import Image

for filename in argv[1:]:
    imgName = filename
    name = imgName[imgName.rindex('/') or 0:]

    img = Image.open(imgName)

    newImage = img.crop((0, 0, 56, 64))
    newImage.save("./Cropped/"+name[:-4]+"_1.png")
    newImage = img.crop((48, 0, 128, 64))
    newImage.save("./Cropped/"+name[:-4]+"_2.png")
