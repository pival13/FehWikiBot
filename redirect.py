#! /usr/bin/env python3

from sys import argv
from datetime import datetime
import requests
import json
import re

from util import URL, TODO, DATA
import util

SKILL_DATA = util.fetchFehData("Common/SRPG/Skill", False)
ACCESSORY_DATA = util.fetchFehData("Common/DressAccessory/Data", False)

def getWeaponName(sprite: str):
    nameId = None
    for skill in SKILL_DATA:
        if nameId:
            break
        for s in skill['sprites']:
            if s and s.lower() + ".webp" == sprite.lower():
                nameId = skill['name_id']
    if nameId and nameId in DATA:
        return "File:Weapon " + util.cleanStr(DATA[nameId]) + (sprite.count("ar") and " V2" or "") + ".png"

def getAccessoryName(sprite: str):
    nameId = None
    for skill in ACCESSORY_DATA:
        if nameId:
            break
        if skill['sprite'].lower() + ".webp" == sprite.lower():
            nameId = skill['id_tag']
    if nameId and "M" + nameId in DATA:
        return "File:Accessory " + util.cleanStr(DATA["M" + nameId]) + ".png"

def redirect(S: requests.session, name: str, redirect: str=None):
    redirect = redirect or name.replace(".webp", ".png")
    result = S.post(url=URL, data={
        "action": "edit",
        "title": redirect,
        "text": "#REDIRECT [[" + name + "]]",
        "createonly": True,
        "bot": True,
        "tags": "automated",
        "watchlist": "nochange",
        "token": util.getToken(),
        "format": "json"
    }).json()
    if 'error' in result and result['error']['code'] == 'articleexists':
        print(f"Redirect already exist: {redirect}")
    elif 'edit' in result and result['edit']['result'] == 'Success':
        print(f"Redirect {name} to {redirect}")
    else:
        print(json.dumps(result, indent=2))
        exit(0)

def main(start=None):
    try:
        result = requests.get(url=URL, params={
            "action": "query",
            "list": "allimages",
            "aisort": "timestamp",
            "aistart": start if start else datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z'),
            "aiprop": "",
            "ailimit": "max",
            "format": "json"
        }).json()

        S = util.fehBotLogin()

        for image in result['query']['allimages']:
            if re.match(r"Map[_ ][A-Z]\w\d{3}\.webp", image['name']):
                redirect(S, image['title'])
            elif re.match(r"TT[_ ]\d{6}(\s\d{2})?\.webp", image['name']):
                if 'MID_SEQUENTIAL_MAP_TERM_' + image['name'][3:-5] in DATA:
                    redirect(S, image['title'], "File:Banner " + util.cleanStr(DATA['MID_SEQUENTIAL_MAP_TERM_' + image['name'][3:-5]]) + ".png")
                else:
                    print(TODO + "TT banner: " + image['title'] + ('MID_SEQUENTIAL_MAP_TERM_' + image['name'][3:-5] in DATA and (" to " + DATA['MID_SEQUENTIAL_MAP_TERM_' + image['name'][3:-5]]) or ''))
            elif re.match(r"Wep[_ ][a-z]{2}\d{3}([_ ]up)?\.webp", image['name']):
                #if not re.match(r"Wep[ _](bw|ar|mg).+\.webp", image['name']):
                #    continue
                wp = getWeaponName(image['name'])
                if wp and re.match(r"Wep[_ ]\w{2}\d{3}[_ ]up\.webp", image['name']) or re.match(r"Wep[_ ]mg\d{3}\.webp", image['name']):
                    print(TODO + image['name'] + " to " + str(wp))
                elif wp:
                    redirect(S, image['title'], wp)
                else:
                    print(TODO + "Weapon with unknow name: " + image['title'])
            elif re.match(r"Acc[_ ][1-4][_ ]\d{4}[_ ]\d\.webp", image['name']):
                acc = getAccessoryName(image['name'])
                if acc:
                    redirect(S, image['title'], acc)
                else:
                    print(TODO + "Accessory with unknow name: " + image['title'])
            elif re.match(r".*[_ ](Btl)?Face[_ ]?(FC|C|D|Smile|Pain|Cool|Anger|Cry)?\d?\.webp", image['name']):
                redirect(S, image['title'])
            elif re.match(r"GC[_ ]\d{6}([_ ]\d{2})?\.webp", image['name']):
                print(TODO + "Grand conquest map: " + image['title'])
            elif re.match(r"Talk[_ ].+\.webp", image['name']):
                redirect(S, image['title'])
            elif re.match(r"EvBg[_ ].+\.webp", image['name']):
                redirect(S, image['title'], "File:Talk " + image['name'].replace(".webp", ".png"))
            elif image['name'][-5:] == '.webp':
                print("Other webp file: " + image['title'])

    except util.LoginError:
        print("Error during login")
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout):
        print("Timeout")
    except requests.exceptions.ConnectionError:
        print("Error during connection")


if __name__ == "__main__":
    main(argv[1] if len(argv) == 2 else None)
