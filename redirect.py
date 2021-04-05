#! /usr/bin/env python3

from sys import argv
from datetime import datetime
import json
import re

from util import URL, TODO, DATA
import util
from wikiUtil import _exportPage

SKILL_DATA = util.fetchFehData("Common/SRPG/Skill", False)
ACCESSORY_DATA = util.fetchFehData("Common/DressAccessory/Data", "sprite")

def getWeaponName(sprite: str):
    nameId = None
    for skill in SKILL_DATA:
        if nameId:
            break
        for s in skill['sprites']:
            if s and s == sprite[:-5].lower().replace(' ', '_'):
                nameId = skill['name_id']
    if nameId and nameId in DATA:
        return "File:Weapon " + util.cleanStr(DATA[nameId]) + (" V2" if sprite.find("ar") != -1 else "") + ".png"

def getAccessoryName(sprite: str):
    if sprite in ACCESSORY_DATA:
        return f"File:Accessory {util.cleanStr(util.getName(ACCESSORY_DATA[sprite]['id_tag']))}.png"

def redirect(name: str, redirect: str):
    result = _exportPage(redirect or name.replace(".webp", ".png"),
                        "#REDIRECT [[" + name + "]]", create=True)
    if 'error' in result and result['error']['code'] == 'articleexists':
        print(f"Redirect already exist: {redirect or name.replace('.webp', '.png')}")
    elif 'edit' in result and result['edit']['result'] == 'Success':
        print(f"Redirect {name} to {redirect or name.replace('.webp', '.png')}")
    else:
        print(json.dumps(result, indent=2))

def main(start=None):
    result = util.fehBotLogin().get(url=URL, params={
        "action": "query",
        "list": "allimages",
        "aisort": "timestamp",
        "aistart": start if start else datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z'),
        "aiprop": "",
        "ailimit": "max",
        "format": "json"
    }).json()

    for image in result['query']['allimages']:
        file = image['title']
        name = None
        if re.match(r"Map[_ ][A-Z]\w\d{3}\.webp", image['name']):
            name = file.replace(".webp", ".png")
        elif re.match(r"TT[_ ]\d{6}(\s\d{2})?\.webp", image['name']):
            if 'MID_SEQUENTIAL_MAP_TERM_' + image['name'][3:-5] in DATA:
                name = "File:Banner " + util.cleanStr(DATA['MID_SEQUENTIAL_MAP_TERM_' + image['name'][3:-5]]) + ".png"
            else:
                print(TODO + "TT banner: " + image['title'])
        elif re.match(r"Wep[_ ][a-z]{2}\d{3}([_ ]up)?\.webp", image['name']):
            wp = getWeaponName(image['name'])
            if wp and (image['name'].find("up") != -1 or image['name'].find("mg") != -1):
                #Do not automatically redirect refine weapon and tomes
                print(TODO + image['name'] + " to " + str(wp))
            elif wp:
                name = wp
            else:
                print(TODO + "Unknow weapon: " + image['title'])
        elif re.match(r"Acc[_ ][1-4][_ ]\d{4}[_ ]\d\.webp", image['name']):
            name = getAccessoryName(image['name'][:-5])
            if not name:
                print(TODO + "Unknow accessory: " + image['title'])
        elif re.search(r"[_ ](Btl)?Face[_ ]?(FC|C|D|Smile|Pain|Cool|Anger|Cry|Blush)?\d*\.webp$", image['name']):
            name = file.replace(".webp", ".png")
        elif re.match(r"GC[_ ]\d{6}([_ ]\d{2})?\.webp", image['name']):
            print(TODO + "Grand conquest map: " + image['title'])
        elif re.match(r"Talk[_ ].+\.webp", image['name']):
            name = file.replace(".webp", ".png")
        elif re.match(r"EvBg[_ ].+\.webp", image['name']):
            name = "File:Talk " + image['name'].replace(".webp", ".png")
        elif image['name'][-5:] == '.webp':
            print("Other webp file: " + image['title'])
        if name:
            redirect(file, name)


if __name__ == "__main__":
    main(argv[1] if len(argv) == 2 else None)
