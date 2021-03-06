#! /usr/bin/env python3

import re

import util
from mapUtil import InOtherLanguage

ACCESSORY_TYPE = ['', 'hat', 'mask', 'hair', 'tiara']

def AccessoryInfobox(data: object):
    return "{{Accessory Infobox\n" + \
        f"|tagid={data['id_tag']}\n" + \
        f"|sort={data['sort_id']}\n" + \
        f"|type={ACCESSORY_TYPE[int(data['sprite'][4])]}\n" + \
        (f"|isSummoner=1\n" if data['summoner'] else "") + \
        "|description=" + util.DATA['M'+data['id_tag'].replace('_', '_H_', 1)].replace('\n', ' ') + "\n" + \
        "}}\n"

def AccessoryObtention(tagid: str):
    shops = util.fetchFehData('Common/DressAccessory/ShopData')
    s = "==Obtained from==\n"
    if util.getName(tagid).find('Gold ') != -1:
        s += '{{Gold accessory}}\n'
    elif tagid[-2:] == '・極' or ('M'+tagid+'・極') in util.DATA:
        s += '{{Forging Bonds accessory}}\n'
    elif "their journeys together" in util.DATA['M'+tagid.replace('_', '_H_', 1)]:
        s += '{{Heroes Journey accessory}}\n'
    #{{Rokkr Sieges accessory}}
    #{{Tap Battle accessory}}
    else:
        r = util.askFor(intro=f"How is obtain accessory {util.getName(tagid)} (except from shop) ?")
        if r: s += ('' if r[0] == '{' or r[0] == '*' else '* ') + r + "\n"
    if tagid in shops:
        s += '{{Shop accessory|' + str(shops[tagid]['price']) + '}}\n'
    return s

def Accessory(sprite: str):
    data = util.fetchFehData('Common/DressAccessory/Data', 'sprite')[sprite.replace(' ', '_')]

    s = AccessoryInfobox(data)
    s += AccessoryObtention(data['id_tag'])
    s += InOtherLanguage('M'+data['id_tag'])
    s += '{{Accessories Navbox}}'
    return {util.getName(data['id_tag']): s}

def AccessoryOf(tag_update: str):
    datas = util.readFehData(f'Common/DressAccessory/Data/{tag_update}.json')
    ret = {}
    for data in datas:
        try:
            ret.update(Accessory(data['sprite']))
        except:
            print(util.ERROR + f"Accessory {util.getName(data['id_tag'])} ({data['sprite']})")
    return ret

from sys import argv, stderr

if __name__ == '__main__':
    for arg in argv[1:]:
        if re.match(r'^\d+_\w+|v\d{4}[a-e]_\w+$', arg):
            acc = AccessoryOf(arg)
        elif re.match(r'^(Acc[_ ])?\d[_ ]\d{4}[_ ]\d$', arg):
            acc = Accessory(('Acc_' if arg[:4] != 'Acc_' else '') + arg)
        else:
            print("Invalid argument for accessory createion: expected a tag update or a sprite name, but got: " + arg, file=stderr)
        for ac in acc:
            print(ac, acc[ac])