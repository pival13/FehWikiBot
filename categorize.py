#! /usr/bin/env python3

import re

import util

from util import cargoQuery
from wikiUtil import getPageContent, exportPage, waitSec
from os.path import exists
from globals import WEAPONS

lastWeaponID = 160600

def categorizeWeapon(name: str, content: str, wepType: int, exclusive: bool):
    openCloseTome = False if re.match(r'File:Wep mg', name) else True
    desc = 'Bot: categorize'
    add = ""

    if re.match(r'File:Wep \w{5}( up)?.webp', name) and content.find('{{Source|') == -1:
        add = ('\n' if content[-1] != '\n' else '') + '{{Source|assets=/assets/Common/Wep/' + name[5:-4].replace(' ', '_').lower() + 'png}}\n'
        desc = 'Bot: add source and categorize'
    elif content[-2:] == "}}": add = "\n"
    if content.find('[[Category:Weapon sprites]]') == -1: add += '[[Category:Weapon sprites]]'
    
    if wepType >= 0b100000000000 and wepType <= 0b111100000000000:
        if (re.match(r'File:Weapon .+ V[34]\.png', name) or re.match(r'File:Wep \w{5} up\.webp', name)) and content.find('[[Category:Upgrade Weapon sprites]]') == -1: add += '[[Category:Upgrade Weapon sprites]]'
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

    if not re.search(r" V\d\.png", name) and name.find(' up.webp') == -1 and name.find('File:Wep ar') == -1 and (not re.search(r"File:Wep mg", name) or exists(util.WEBP_ASSETS_DIR_PATH+'Common/Wep/'+name[5:-5].replace(' ', '_')+'.ssbp')):
        if exclusive and content.find('[[Category:Exclusive Weapon sprites]]') == -1: add += '[[Category:Exclusive Weapon sprites]]'
        if not exclusive and content.find('[[Category:Inheritable Weapon sprites]]') == -1: add += '[[Category:Inheritable Weapon sprites]]'

    if len(add) != 0:
        waitSec(10)
        exportPage(name, content + add, desc, minor=True, create=False)

def categorizeWeapons():
    pagesName = [m['Page'] for m in cargoQuery('_pageData', where=f'(_pageName LIKE "File:Weapon %" OR _pageName LIKE "File:Wep %") AND _pageID > {lastWeaponID}', order='_pageID')]
    wikiPages = getPageContent(pagesName)
    wikiPages = {name: wikiPages[name] for name in wikiPages if wikiPages[name].find('REDIRECT') == -1}
    if len(wikiPages) == 0: return
    newID = cargoQuery('_pageData', fields='_pageID=ID', where=f'_pageName="{pagesName[-1]}"', limit=1)[0]['ID']
    pagesName = list(wikiPages.keys())

    WEP_SPRITES = {weapon['sprites'][0]: weapon for weapon in WEAPONS.values() if weapon['sprites'][0]}
    WEP_SPRITES.update({weapon['sprites'][1]: weapon for weapon in WEAPONS.values() if weapon['sprites'][1]})
    WEP_NAMES = {util.cleanStr(util.getName(wepTag)): WEAPONS[wepTag] for wepTag in WEAPONS}

    regWebp = re.compile(r'File:Wep (\w{5}(?: up)?)\.webp')
    regPng = re.compile(r'File:Weapon (.*?)(?: V\d+)?\.png')
    for weapon in pagesName:
        res1 = regWebp.match(weapon)
        res2 = regPng.match(weapon)
        if res1:
            wobject = WEP_SPRITES[f"wep_{res1[1].lower().replace(' ', '_')}"]
        elif res2 and res2[1] in WEP_NAMES:
            wobject = WEP_NAMES[res2[1]]
        else:
            print(util.TODO, f'Cannot categorize {weapon}')
            continue

        categorizeWeapon(weapon, wikiPages[weapon], wobject["wep_equip"], wobject["exclusive"])

    if util.askAgreed(f"Do you want to replace the current lastWeaponID ({lastWeaponID}) with the new one ({newID})?", defaultTrue=True, defaultFalse=False):
        with open(__file__, 'r') as f: content = f.read()
        with open(__file__, 'w') as f: f.write(content.replace(f'lastWeaponID = {lastWeaponID}', f'lastWeaponID = {newID}'))

if __name__ == '__main__':
    categorizeWeapons()