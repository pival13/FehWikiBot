#!/usr/bin/env python3

import re
import subprocess
from os import remove, rmdir, listdir
import os.path

import globals
import util
import wikiUtil
from uploadImage import exportImage

def getName(folderName):
    if folderName in globals.UNIT_IMAGE and 'name' in globals.UNIT_IMAGE[folderName]:
        name = globals.UNIT_IMAGE[folderName]['name']
    else:
        append = ""
        if folderName[-4:] == "EX01":
            append += "_Resplendent"; folderName = folderName[:-4]
        if folderName[-7:] == "airMain":
            append = "_Main"+append; folderName = folderName[:-4]
        elif folderName[-6:] == "airSub":
            append = "_Sub"+append; folderName = folderName[:-3]
        elif folderName[-8:] == "TransMap":
            append = "_TransformMap"+append; folderName = folderName[:-9]
        elif folderName[-11:] == "TransBattle":
            append = "_Transform"+append; folderName = folderName[:-12]
        elif folderName[-6:] == "Dragon":
            append = "_Transform"+append
            if folderName[:-6] in globals.UNIT_IMAGE: folderName = folderName[:-6]
            elif folderName[:-7] in globals.UNIT_IMAGE: folderName = folderName[:-7]
            elif folderName[:-6]+"Normal" in globals.UNIT_IMAGE: folderName = folderName[:-6]+'Normal'
            elif folderName[:-11] in globals.UNIT_IMAGE: folderName = folderName[:-11]
            #elif folderName[:-10]+"Legend01" in globals.UNIT_IMAGE: pass
            else:
                print(util.ERROR + "Unknow name for " + folderName)
                raise NameError(folderName)
        elif folderName[-5:] == "_blow":
            append = "_sword"+append; folderName = folderName[:-5]
        elif folderName[-3:] == "_lc":
            append = "_lance"+append; folderName = folderName[:-3]
        elif folderName[-3:] == "_ax":
            append = "_axe"+append; folderName = folderName[:-3]
        elif folderName[-3:] == "_mg":
            append = "_magic"+append; folderName = folderName[:-3]
        if folderName in globals.UNIT_IMAGE:
            return util.getName(globals.UNIT_IMAGE[folderName]['id_tag']) + append
        else:
            raise NameError(folderName, append)

def getFiles(unit):
    """Regular: Idle, Start, Ok, Ready, Jump, Attack1, Attack2, Damage
    Human Transformable: Idle, Start, Ok, Damage, Transform
    PairSub: Idle, Start, Ok, Attack1, Damage
    TransMap: Idle, Start

    Magic / Dragon += Attack1_Loop, Attack2_Loop
    Legendary / Mythic += AttackF(_Loop)
    Refresher += Cheer
    Duo += Pairpose
    Transformed += Transform
                -= Ok
    Dragon -= Attack2"""
    name = util.getName(unit['id_tag'])
    files = ['Idle', 'Ok', 'Ready', 'Jump', 'Attack1', 'Attack2', 'Damage']
    extra = []
    if ('is_boss' in unit and unit['is_boss']) or ('legendary' in unit and unit['legendary'] and unit['legendary']['kind'] == 1):
        files.insert(files.index('Attack2')+1, 'AttackF')
    if (1 << unit['weapon_type']) & (globals.WEAPON_MASK['Beast'] | globals.WEAPON_MASK['Dragonstone']) != 0:
        files.remove('Ok')
        extra = ['Transform Transform'] + ['Transform ' + f for f in files]
        if (1 << unit['weapon_type']) & globals.WEAPON_MASK['Beast']:
            extra = ['TransformMap Idle'] + extra
        else:
            extra.remove('Transform Attack2')
        files = ['Idle', 'Ok', 'Damage', 'Transform']
    if unit['refresher']:
        files.insert(files.index('Damage')+1, 'Cheer')
    if 'legendary' in unit and unit['legendary'] and unit['legendary']['element'] == 0:
        extra = ['Main ' + f for f in ['Idle No Wep']+files] + ['Sub Idle No Wep' 'Sub Idle', 'Sub Ok', 'Sub Attack1', 'Sub Damage'] + extra
        files.insert(files.index('Ok')+1, 'Pairpose')
    if ((1 << unit['weapon_type']) & globals.WEAPON_MASK['Beast']) == 0:
        files.insert(files.index('Idle'), 'Idle No Wep')
    if unit['id_tag'] in globals.RESPLENDENTS:
        extra = ['Resplendent ' + f for f in files] + extra
    files = [f'File:{util.cleanStr(name)} Mini Unit {f}.png' for f in files] + [f"File:{util.cleanStr(name)} {f[:f.index(' ')]} Mini Unit {f[f.index(' ')+1:]}.png" for f in extra]
    return files

def getSpriteSheets(unit):
    n = unit['face_name2']
    name = util.cleanStr(util.getName(unit['id_tag']))
    dir = util.WEBP_ASSETS_DIR_PATH + 'Common/Unit/'
    files = [f"File:{name} {d.replace('.png','.webp')}" for d in listdir(dir + n + '/tex/')]
    if (1 << unit['weapon_type']) & globals.WEAPON_MASK['Beast']:
        if os.path.exists(dir + n + '_TransMap'):
            files += [f"File:{name} TransformMap {d.replace('.png','.webp')}" for d in listdir(dir + n + '_TransMap/tex/')]
            files += [f"File:{name} Transform {d.replace('.png','.webp')}" for d in listdir(dir + n + '_TransBattle/tex/')]
        else:
            for i in range(len(n), 1, -1):
                if os.path.exists(dir + n[:i] + 'TransMap'):
                    files += [f"File:{name} TransformMap {d.replace('.png','.webp')}" for d in listdir(dir + n[:i] + 'TransMap/tex/')]
                    files += [f"File:{name} Transform {d.replace('.png','.webp')}" for d in listdir(dir + n[:i] + 'TransBattle/tex/')]
                    break
    elif (1 << unit['weapon_type']) & globals.WEAPON_MASK['Dragonstone']:
        if os.path.exists(dir + n + '_Dragon'):
            files += [f"File:{name} Transform {d.replace('.png','.webp')}" for d in listdir(dir + n + '_Dragon/tex/')]
        else:
            for i in range(len(n), 1, -1):
                if os.path.exists(dir + n[:i] + 'Dragon'):
                    files += [f"File:{name} Transform {d.replace('.png','.webp')}" for d in listdir(dir + n[:i] + 'Dragon/tex/')]
                    break
    return files

def spriteSaverCommand(unit):
    commands = []
    wepR = wepL = None
    names = [unit['face_name2']]
    if unit['id_tag'] in globals.RESPLENDENTS:
        names += [unit['face_name2']+'EX01']
    if re.match('_[Pp]air', unit['face_name2'][-5:]):
        names += [unit['face_name2']+'Main', unit['face_name2']+'Sub']
    if (1 << unit['weapon_type']) & globals.WEAPON_MASK['Beast']:
        if os.path.exists(util.WEBP_ASSETS_DIR_PATH + 'Common/Unit/' + unit['face_name2'] + '_TransMap'):
            names += [unit['face_name2'] + '_TransMap', unit['face_name2'] + '_TransBattle']
        else:
            for i in range(len(unit['face_name2']), 1, -1):
                if os.path.exists(util.WEBP_ASSETS_DIR_PATH + 'Common/Unit/' + unit['face_name2'][:i] + 'TransMap'):
                    names += [unit['face_name2'][:i] + 'TransMap', unit['face_name2'][:i] + 'TransBattle']; break
    elif (1 << unit['weapon_type']) & globals.WEAPON_MASK['Dragonstone']:
        if os.path.exists(util.WEBP_ASSETS_DIR_PATH + 'Common/Unit/' + unit['face_name2'] + '_Dragon'):
            names += [unit['face_name2'] + '_Dragon']
        else:
            for i in range(len(unit['face_name2']), 1, -1):
                if os.path.exists(util.WEBP_ASSETS_DIR_PATH + 'Common/Unit/' + unit['face_name2'][:i] + 'Dragon'):
                    names += [unit['face_name2'][:i] + 'Dragon']; break

    #My summoner PRFs
    if unit['face_name2'] == "ch00_00_Eclat_X_Normal": wepR = 'wep_ex'
    elif unit['face_name2'][-5:] == "_blow":           wepR = 'wep_sw114'
    elif unit['face_name2'][-3:] == "_lc":             wepR = 'wep_lc100'
    elif unit['face_name2'][-3:] == "_ax":             wepR = 'wep_ax087'
    elif unit['face_name2'][-3:] == "_mg":             wepR = 'wep_mg306'
    else:
        wep = unit['top_weapon'] if 'top_weapon' in unit else None
        if not wep:
            for skill in unit['skills'][-1][::-1]:
                if skill and globals.SKILLS[skill]['might'] != 0:
                    wep = skill
                    break
        if wep:
            if wep+'_ATK' in globals.SKILLS:
                wep = wep+'_ATK'
            elif not wep in globals.SKILLS:
                print(util.ERROR + f"Failed to retrieve weapon \"{wep}\"")
                return
            wepL = globals.SKILLS[wep]['sprites'][0]
            wepR = globals.SKILLS[wep]['sprites'][1]

    wepFolder = os.path.realpath(util.WEBP_ASSETS_DIR_PATH + 'Common/Wep')
    for name in names:
        s = os.path.realpath(util.WEBP_ASSETS_DIR_PATH + f"Common/Unit/{name}/{name}.ssbp")
        if not re.search(r'(Dragon|TransBattle|TransMap|Sub)$', name):
            if wepR:
                if os.path.exists(wepFolder + '/' + wepR + '.ssbp'):
                    s += f" -b Wep_BaseR:{wepFolder}/{wepR}.ssbp:{wepR}/Wep_Normal -b Wep_BaseR_Add:{wepR}:{wepR}/Wep_Normal"
                else:
                    s += f" -b Wep_BaseR:{wepFolder}/{wepR}.png -b Wep_BaseR_Add:{wepFolder}/{wepR}.png"
            if wepL:
                if os.path.exists(wepFolder + '/' + wepL + '.ssbp'):
                    s += f" -b Wep_BaseL:{wepFolder}/{wepL}.ssbp:{wepL}/Wep_Normal -b Wep_BaseL_Add:{wepL}:{wepL}/Wep_Normal"
                else:
                    s += f" -b Wep_BaseL:{wepFolder}/{wepL}.png -b Wep_BaseL_Add:{wepFolder}/{wepL}.png"
        if re.search(r"_[Pp]air$", name):
            s += ' -w 1000 -h 1500'
        elif re.search(r"Dragon|TransBattle", name):
            s += ' -w 1500 -h 1500'
        commands += [re.sub(r'\B/mnt/(\w)/', '\\1:/', s)]
    return '\n'.join(commands) + '\n'

def createMiniUnit(id_tag):
    unit = globals.UNITS[id_tag]
    n = unit['face_name2']
    subprocess.run('./spriteSaver.exe', input=spriteSaverCommand(unit).encode())

def uploadMiniUnit():
    dir = "./Screenshots/"
    for c in listdir(dir):
        try:
            name = getName(c)
            print("> ", c, " ==> ", name)
            for f in listdir(dir + c):
                wikiUtil.waitSec(10)
                if f == 'Idle_no_wep.png':
                    exportImage(util.cleanStr(name) + "_Mini_Unit_Idle_No_Wep.png", open(dir + c + "/" + f, "rb"),
                        f"[[Category:Mini unit sprites]][[Category:Mini unit Idle sprites]][[Category:Mini unit no weapon sprites]]",
                        f"Bot: Mini unit", True)
                else:
                    anim = re.match(r"^(.+)_\d+\.png$", f)[1]
                    exportImage(util.cleanStr(name) + "_Mini_Unit_" + anim + ".png", open(dir + c + "/" + f, "rb"),
                        f"[[Category:Mini unit sprites]][[Category:Mini unit {anim.replace('_',' ')} sprites]]",
                        f"Bot: Mini unit", True)
                try:
                    remove(dir + c + "/" + f)
                except:
                    print("Failed to remove file " + f)
            try:
                rmdir(dir + c)
            except:
                print("Failed to remove dir " + c)
        except:
            print(util.ERROR + "Error with " + c)

def useMiniUnit(id_tags):
    for id_tag in id_tags:
        unit = globals.UNITS[id_tag]
        name = util.getName(unit['id_tag'])
        files = getFiles(unit)
        spritesheets = getSpriteSheets(unit)
        try:
            page = wikiUtil.getPageContent(name + '/Misc')[name + '/Misc']
            if not re.search(r'===\s*Sprites?\s*===', page):
                page = re.sub('(</gallery>)', '\\1\n===Sprite===\n<gallery>\n</gallery>', page, 1)
            prev = r'Sprite.*\n<gallery>.*'
            for f in files:
                if not re.search(f.replace(' ', '_').replace('_','[_ ]').replace('File:',''), page):
                    page = re.sub('('+prev+')', '\\1\n'+f, page, 1)
                prev = f.replace(' ', '_').replace('_','[_ ]').replace('File:','') + '.*'
            for f in spritesheets:
                if not re.search(f.replace(' ', '_').replace('_','[_ ]').replace('File:',''), page):
                    page = re.sub(f"({f[:f.rindex(' ')]} Mini Unit)", f+'\n\\1', page, 1)
            wikiUtil.exportPage(name + '/Misc', page, 'Bot: Add Mini unit', minor=True)
        except:
            print('Error with ' + name)

def MiniUnit(id_tag):
    createMiniUnit(id_tag)
    uploadMiniUnit()
    useMiniUnit([id_tag])

def MiniUnitsFrom(update_tag):
    person = util.readFehData('Common/SRPG/Person/' + update_tag + '.json')
    person += util.readFehData('Common/SRPG/Enemy/' + update_tag + '.json')
    for p in person:
        createMiniUnit(p['id_tag'])
    uploadMiniUnit()
    useMiniUnit([p['id_tag'] for p in person])

from sys import argv
if __name__ == '__main__':
    for arg in argv[1:]:
        MiniUnit(arg)