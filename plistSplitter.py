#!/usr/bin/env python3

from sys import argv
from PIL import Image
import re
import json
from xml.etree import cElementTree

def parseXml(xml):
    if xml.tag == 'dict':
        return {xml[i*2].text: parseXml(xml[i*2+1]) for i in range(int(len(xml) / 2))}
    elif xml.tag in ['true','false']:
        return xml.tag == 'true'
    else:
        return xml.text

for filename in argv[1:]:
    imgName = re.sub(r'\.plist$', '.png', filename)

    xml = parseXml(cElementTree.parse(filename).getroot()[0])
    img = Image.open(imgName)

    for subImage in xml['frames']:
        coords = re.match(r"\{\{(\d+),(\d+)\},\{(\d+),(\d+)\}\}", xml['frames'][subImage]['textureRect'])
        coords = [int(coords[i]) for i in range(1,5)]
        rotated = xml['frames'][subImage]['textureRotated']

        newImage = img.crop((coords[0], coords[1], coords[0] + coords[2 if not rotated else 3], coords[1] + coords[3 if not rotated else 2]))
        if rotated:
            newImage = newImage.transpose(Image.ROTATE_90)
        newImage.save("../Cropped/"+subImage)
