#! /usr/bin/env python3

import re

import util

from util import cargoQuery
from wikiUtil import getPageContent, exportPage
from mapUtil import WEAPONS

lastWeaponID = 139527

def categorizeWeapon(name: str, content: str, wepType: int, exclusive: bool, openCloseTome: bool=True):
    desc = 'Bot: categorize'
    add = ""

    if re.match(r'File:Wep \w{5}( up)?.webp', name) and content.find('{{Source|') == -1:
        add = ('\n' if content[-1] != '\n' else '') + '{{Source|assets=/assets/Common/Wep/' + name[5:-4].replace(' ', '_').lower() + 'png}}\n'
        desc = 'Bot: add source and categorize'
    else content[-2:] == "}}": add = "\n"
    if content.find('[[Category:Weapon sprites]]') == -1: add += '[[Category:Weapon sprites]]'
    
    if wepType >= 0b100000000000 and wepType <= 0b111100000000000:
        if re.match(r'File:Weapon .+ V[34]\.png', name) and content.find('[[Category:Upgrade Weapon sprites]]') == -1: add += '[[Category:Upgrade Weapon sprites]]'
    elif (re.match(r'File:Weapon .+ V2\.png', name) or re.match(r'File:Wep \w{5} up\.webp', name)) and content.find('[[Category:Upgrade Weapon sprites]]') == -1: add += '[[Category:Upgrade Weapon sprites]]'

    if wepType == 0b1 and content.find('[[Category:Red Sword sprites]]') == -1: add += '[[Category:Red Sword sprites]]'
    if wepType == 0b10 and content.find('[[Category:Blue Lance sprites]]') == -1: add += '[[Category:Blue Lance sprites]]'
    if wepType == 0b100 and content.find('[[Category:Green Axe sprites]]') == -1: add += '[[Category:Green Axe sprites]]'
    if wepType == 0b1000000000000000 and content.find('[[Category:Colorless Staff sprites]]') == -1: add += '[[Category:Colorless Staff sprites]]'
    if wepType == 0b11110000000 and content.find('[[Category:Dagger sprites]]') == -1: add += '[[Category:Dagger sprites]]'
    if wepType == 0b11110000000000000000 and content.find('[[Category:Breath sprites]]') == -1: add += '[[Category:Breath sprites]]'
    if wepType == 0b111100000000000000000000 and content.find('[[Category:Beast Weapon sprites]]') == -1: add += '[[Category:Beast Weapon sprites]]'

    if wepType == 0b1111000:
        if re.match(r'File:Weapon .+ V[24]\.png', name) or re.match(r'File:Wep ar\d{3}( up)?\.webp', name):
            if content.find('[[Category:Arrow sprites]]') == -1: add += '[[Category:Arrow sprites]]'
        else:
            if content.find('[[Category:Bow sprites]]') == -1: add += '[[Category:Bow sprites]]'

    if wepType >= 0b100000000000 and wepType <= 0b111100000000000:
        if content.find('[[Category:Tome sprites]]') == -1: add += '[[Category:Tome sprites]]'
        if openCloseTome and re.match(r'File:Weapon .+ V[24]\.png', name):
            if content.find('[[Category:Open Tome sprites]]') == -1: add += '[[Category:Open Tome sprites]]'
        elif openCloseTome and re.match(r'File:Weapon .+\.png', name) and content.find('[[Category:Closed Tome sprites]]') == -1: add += '[[Category:Closed Tome sprites]]'
    if wepType == 0b100000000000:
        if content.find('[[Category:Red Tome sprites]]') == -1: add += '[[Category:Red Tome sprites]]'
        if openCloseTome and (add.find('Open Tome') != -1 or content.find('Open Tome') != -1) and content.find('[[Category:Open Red Tome sprites]]') == -1: add += '[[Category:Open Red Tome sprites]]'
        if openCloseTome and (add.find('Closed Tome') != -1 or content.find('Closed Tome') != -1) and content.find('[[Category:Closed Red Tome sprites]]') == -1: add += '[[Category:Closed Red Tome sprites]]'
    if wepType == 0b1000000000000:
        if content.find('[[Category:Blue Tome sprites]]') == -1: add += '[[Category:Blue Tome sprites]]'
        if openCloseTome and (add.find('Open Tome') != -1 or content.find('Open Tome') != -1) and content.find('[[Category:Open Blue Tome sprites]]') == -1: add += '[[Category:Open Blue Tome sprites]]'
        if openCloseTome and (add.find('Closed Tome') != -1 or content.find('Closed Tome') != -1) and content.find('[[Category:Closed Blue Tome sprites]]') == -1: add += '[[Category:Closed Blue Tome sprites]]'
    if wepType == 0b10000000000000:
        if content.find('[[Category:Green Tome sprites]]') == -1: add += '[[Category:Green Tome sprites]]'
        if openCloseTome and (add.find('Open Tome') != -1 or content.find('Open Tome') != -1) and content.find('[[Category:Open Green Tome sprites]]') == -1: add += '[[Category:Open Green Tome sprites]]'
        if openCloseTome and (add.find('Closed Tome') != -1 or content.find('Closed Tome') != -1) and content.find('[[Category:Closed Green Tome sprites]]') == -1: add += '[[Category:Closed Green Tome sprites]]'
    if wepType == 0b100000000000000:
        if content.find('[[Category:Colorless Tome sprites]]') == -1: add += '[[Category:Colorless Tome sprites]]'
        if openCloseTome and (add.find('Open Tome') != -1 or content.find('Open Tome') != -1) and content.find('[[Category:Open Colorless Tome sprites]]') == -1: add += '[[Category:Open Colorless Tome sprites]]'
        if openCloseTome and (add.find('Closed Tome') != -1 or content.find('Closed Tome') != -1) and content.find('[[Category:Closed Colorless Tome sprites]]') == -1: add += '[[Category:Closed Colorless Tome sprites]]'

    if not re.search(r" V\d\.png", name) and name.find(' up.webp') == -1 and name.find('File:Wep ar') == -1 and (not re.search(r"File:Wep mg", name) or not openCloseTome):
        if exclusive and content.find('[[Category:Exclusive Weapon sprites]]') == -1: add += '[[Category:Exclusive Weapon sprites]]'
        if not exclusive and content.find('[[Category:Inheritable Weapon sprites]]') == -1: add += '[[Category:Inheritable Weapon sprites]]'

    if len(add) != 0:
        waitSec(10)
        exportPage(name, content + add, desc, minor=True, create=False)

def categorizeWeapons():
    pagesName = [m['Page'] for m in cargoQuery('_pageData', where=f'(_pageName LIKE "File:Weapon %" OR _pageName LIKE "File:Wep %") AND _pageID > {lastWeaponID}', order='_pageID')]
    wikiPages = getPageContent(pagesName)
    wikiPages = {name: wikiPages[name] for name in wikiPages if wikiPages[name].find('REDIRECT') == -1}
    newID = cargoQuery('_pageData', fields='_pageID=ID', where=f'_pageName="{pagesName[-1]}"', limit=1)[0]['ID']
    pagesName = list(wikiPages.keys())
    print(f"Previous lastWeaponID: {lastWeaponID}. New lastWeaponID: {newID}")

    for wepTag in WEAPONS:
        if WEAPONS[wepTag]["refine_sort_id"] != 0 or wepTag[-1] == '＋' or (not WEAPONS[wepTag]['sprites'][0] and not WEAPONS[wepTag]['sprites'][1]): continue
        searchPage = 'File:' + (WEAPONS[wepTag]['sprites'][0] if WEAPONS[wepTag]['sprites'][0] else WEAPONS[wepTag]['sprites'][1]).capitalize().replace('_', ' ') + '.webp'
        if not searchPage in wikiPages:
            searchPage = 'File:Weapon ' + util.cleanStr(util.getName(wepTag)) + '.png'
        if not searchPage in wikiPages: continue
        elif searchPage in pagesName: pagesName.remove(searchPage)

        if WEAPONS[wepTag]["wep_equip"] == 0b1111000:#Bow
            searchPage = 'File:' + WEAPONS[wepTag]['sprites'][0].capitalize().replace('_', ' ') + '.webp'
            if not searchPage in wikiPages:
                searchPage = 'File:Weapon ' + util.cleanStr(util.getName(wepTag)) + '.png'
            categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"])
            if re.match(r'File:Weapon .+\.png', searchPage):
                searchPage = re.sub(r'\.png', ' V2.png', searchPage)
                if searchPage in wikiPages: categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(searchPage)
                searchPage = re.sub('V2', 'V3', searchPage)
                if searchPage in wikiPages: categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(searchPage)
                searchPage = re.sub('V3', 'V4', searchPage)
                if searchPage in wikiPages: categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(searchPage)
            elif re.match(r'File:Wep bw\d{3}\.webp', searchPage):
                sId = searchPage[11:14]
                if f'File:Wep ar{sId}.webp' in wikiPages: categorizeWeapon(f'File:Wep ar{sId}.webp', wikiPages[f'File:Wep ar{sId}.webp'], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(f'File:Wep ar{sId}.webp')
                if f'File:Wep bw{sId} up.webp' in wikiPages: categorizeWeapon(f'File:Wep bw{sId} up.webp', wikiPages[f'File:Wep bw{sId} up.webp'], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(f'File:Wep bw{sId} up.webp')
                if f'File:Wep ar{sId} up.webp' in wikiPages: categorizeWeapon(f'File:Wep ar{sId} up.webp', wikiPages[f'File:Wep ar{sId} up.webp'], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(f'File:Wep ar{sId} up.webp')
        elif WEAPONS[wepTag]["wep_equip"] >= 0b100000000000 and WEAPONS[wepTag]["wep_equip"] <= 0b111100000000000:#Tome
            searchPage = re.sub(' V2', '', searchPage)
            categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"], (re.match(r'File:Weapon .+\.png', searchPage) and re.sub(r'\.png', ' V2.png', searchPage) in wikiPages) or (re.match(r'File:Wep mg.+\.webp', searchPage) and ('File:Weapon ' + util.cleanStr(util.getName(wepTag)) + '.png') in wikiPages))
            if re.match(r'File:Wep mg\d{3}\.webp', searchPage):
                searchPage = re.sub(r'\.webp', ' up.webp', searchPage)
                if searchPage in wikiPages: categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(searchPage)
            if not re.match(r'File:Weapon .+\.png', searchPage):
                searchPage = 'File:Weapon ' + util.cleanStr(util.getName(wepTag)) + '.png'
                if searchPage in wikiPages: categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(searchPage)
            searchPage = re.sub(r'\.png', ' V2.png', searchPage)
            if searchPage in wikiPages: categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(searchPage)
            searchPage = re.sub('V2', 'V3', searchPage)
            if searchPage in wikiPages: categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(searchPage)
            searchPage = re.sub('V3', 'V4', searchPage)
            if searchPage in wikiPages: categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(searchPage)
        else:
            categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"])
            if re.match(r'File:Weapon .+\.png', searchPage):
                searchPage = re.sub(r'\.png', ' V2.png', searchPage)
                if searchPage in wikiPages: categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(searchPage)
            elif re.match(r'File:Wep \w{5}\.webp', searchPage):
                searchPage = re.sub(r'\.webp', ' up.webp', searchPage)
                if searchPage in wikiPages: categorizeWeapon(searchPage, wikiPages[searchPage], WEAPONS[wepTag]["wep_equip"], WEAPONS[wepTag]["exclusive"]) or pagesName.remove(searchPage)

    with open(__file__, 'r') as f: content = f.read()
    with open(__file__, 'w') as f: f.write(content.replace(f'lastWeaponID = {lastWeaponID}', f'lastWeaponID = {newID}'))

if __name__ == '__main__':
    categorizeWeapons()