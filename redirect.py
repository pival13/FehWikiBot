#! /usr/bin/env python3

from sys import argv
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
        "token": util.getToken(S),
        "format": "json"
    }).json()
    if 'error' in result and result['error']['code'] == 'articleexists':
        print(f"Redirect already exist: {redirect}")
    elif 'edit' in result and result['edit']['result'] == 'Success':
        print(f"Redirect {name} to {redirect}")
    else:
        print(json.dumps(result, indent=2))
        exit(0)

def main():
    if len(argv) != 2:
        print("Enter a start time")
        exit(1)

    try:
        result = requests.get(url=URL, params={
            "action": "query",
            "list": "allimages",
            "aisort": "timestamp",
            "aistart": argv[1],
            "aiprop": "",
            "ailimit": "max",
            "format": "json"
        }).json()

        S = util.fehBotLogin()

        for image in result['query']['allimages']:
            if re.compile(r"Map[_ ][A-Z]\w\d{3}\.webp").match(image['name']):
                redirect(S, image['title'])
            elif re.compile(r"TT[_ ]\d{6}(\s\d{2}|)\.webp").match(image['name']):
                print(TODO + "TT banner: " + image['title'])
            elif re.compile(r"Wep[_ ][a-z]{2}\d{3}([_ ]up|)\.webp").match(image['name']):
                wp = getWeaponName(image['name'])
                if wp and re.compile(r"Wep[_ ]\w{2}\d{3}[_ ]up\.webp").match(image['name']) or re.compile(r"Wep[_ ]mg\d{3}\.webp").match(image['name']):
                    print(TODO + image['name'] + " to " + wp)
                elif wp:
                    redirect(S, image['title'], wp)
                else:
                    print(TODO + "Weapon with unknow name: " + image['title'])
            elif re.compile(r"Acc[_ ][1-4][_ ]\d{4}[_ ]\d\.webp").match(image['name']):
                acc = getAccessoryName(image['name'])
                if acc:
                    redirect(S, image['title'], acc)
                else:
                    print(TODO + "Accessory with unknow name: " + image['title'])
            elif re.compile(r"\w*[_ ](Btl|)Face[_ ]?(FC|C|D|)\.webp").match(image['name']):
                redirect(S, image['title'])
            elif re.compile(r"GC[_ ]\d{6}([_ ]\d{2}|)\.webp").match(image['name']):
                print(TODO + "Grand conquest map: " + image['title'])
            elif re.compile(r".*\.webp").match(image['name']):
                print("Other webp file: " + image['title'])

    except util.LoginError:
        print("Error during login")
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout):
        print("Timeout")
    except requests.exceptions.ConnectionError:
        print("Error during connection")


if __name__ == "__main__":
    main()
