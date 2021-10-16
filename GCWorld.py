#! /usr/bin/env python3

import util
from PIL import Image
from plistSplitter import parseXml, extractImage

GCData = parseXml(util.WEBP_ASSETS_DIR_PATH + 'Common/UI/Occupation.plist')['frames']
GCAssets = Image.open(util.WEBP_ASSETS_DIR_PATH + 'Common/UI/Occupation.png')
Font = extractImage(Image.open(util.APK_ASSETS_DIR_PATH + 'Common/UI/Font.png'), parseXml(util.APK_ASSETS_DIR_PATH + 'Common/UI/Font.plist')['frames']['Font_StatusS.png'])#['Font_Status.png'])
FontSize = (28,34) # (34,42)

def GCDefaultWorld(tag: str, world_id: str):
    GCWorld = Image.open(util.WEBP_ASSETS_DIR_PATH + 'Common/Occupation/BG/' + tag + '.png').convert('RGBA')
    GCArea = extractImage(GCAssets, GCData['AreaRed.0.png']) #'AreaBlue.0.png'
    GCArea = GCArea.resize((int(GCArea.width * 0.44), int(GCArea.height * 0.44))).convert('LA').convert('RGBA')
    areas = util.readFehData('Common/Occupation/World/'+world_id+'.json')['areas']
    for area in areas:
        GCWorld.alpha_composite(GCArea, (area['x']-int(GCArea.width/2),area['y']-int(GCArea.height/2)))
        nb1 = int(area['area_no'] / 10)
        nb2 = Font.crop(((area['area_no'] % 10) * FontSize[0], FontSize[1], (area['area_no'] % 10 + 1) * FontSize[0], FontSize[1]*2)).convert('RGBA')
        if nb1 == 0:
            GCWorld.alpha_composite(nb2, (area['x']-int(FontSize[0]/2),area['y']-int(FontSize[1]/2)-5))
        else:
            nb1 = Font.crop((nb1 * FontSize[0], FontSize[1], (nb1+1) * FontSize[0], FontSize[1]*2)).convert('RGBA')
            GCWorld.alpha_composite(nb1, (area['x']-FontSize[0]+1,area['y']-int(FontSize[1]/2)-5))
            GCWorld.alpha_composite(nb2, (area['x']-4,area['y']-int(FontSize[1]/2)-5))
    return GCWorld

from sys import argv
from Reverse import reverseGrandConquests
if __name__ == '__main__':
    for arg in argv[1:]:
        datas = reverseGrandConquests(arg)
        for data in datas:
            GCDefaultWorld(data['str1'], data['battles'][0]['world_id']).save(data['str1'] + '.png')