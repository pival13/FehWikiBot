#!/usr/bin/env python3

from sys import argv
from PIL import Image
import re
import json
from xml.etree import cElementTree

def _parseXml(xml):
    if xml.tag == 'dict':
        return {xml[i*2].text: _parseXml(xml[i*2+1]) for i in range(int(len(xml) / 2))}
    elif xml.tag in ['true','false']:
        return xml.tag == 'true'
    elif xml.tag == 'string' and xml.text[0] == '{' and xml.text[-1] == '}':
        return json.loads(xml.text.replace('{','[').replace('}',']'))
    else:
        return xml.text

def parseXml(file):
    return _parseXml(cElementTree.parse(file).getroot()[0])

def extractImage(image, data):
    newImage = image.crop((
        data['textureRect'][0][0],
        data['textureRect'][0][1],
        data['textureRect'][0][0] + data['textureRect'][1][0 if not data['textureRotated'] else 1],
        data['textureRect'][0][1] + data['textureRect'][1][1 if not data['textureRotated'] else 0]))
    if data['textureRotated']:
        newImage = newImage.transpose(Image.ROTATE_90)
    return newImage

if __name__ == '__main__':
    for filename in argv[1:]:
        xml = parseXml(filename)
        img = Image.open(re.sub(r'\.plist$', '.png', filename))
        for subImage in xml['frames']:
            extractImage(img, xml['frames'][subImage]).save("./Cropped/"+subImage)
