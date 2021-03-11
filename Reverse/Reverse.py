#!/usr/bin/env python3

from subprocess import Popen, PIPE, STDOUT
import json

import REutil as util

"""
BIN.LZ Header:
TotalSize: 0x04
CorpseSize: 0x04
PtrTableSize: 0x04
StringTableSize: 0x04 (0x08 each : idx (0x04), tblStringIdx (0x04))
XXX: 0x04
XXX: 0x04
"""

from RevData  import parseMsg, parseStageBGM
from RevMap   import parseField, parseSRPGMap, parseStageScenario, parseStageEvent, parseStagePuzzle
from RevUnit  import parsePerson, parseEnemy
from RevQuest import parseQuests

from RevVG  import parseTournament
from RevTT  import parseSequentialMap
from RevTB  import parseTapAction
from RevGC  import parseOccupation
from RevFB  import parsePortrait
from RevRS  import parseShadow
from RevLL  import parseTrip
from RevHoF import parseIdolTower
from RevMS  import parseMjolnir
from RevFP  import parseEncourage
from RevPoL import parseBoardGame

def parseAccessory(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x0de4c6f0ab07e0e13)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x20*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "sprite": util.getString(data, offGr+0x08),
        }]
    return result

def parseSkill(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x7fecc7074adee9ad)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x148*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "refine_base": util.getString(data, offGr+0x08),
            "name_id": util.getString(data, offGr+0x10),
            "desc_id": util.getString(data, offGr+0x18),
            "refine_id": util.getString(data, offGr+0x20),
            "beast_effect_id": util.getString(data, offGr+0x28),
            #"prerequisites": [util.getString(data, offGr+0x30+0x08*i) for i in range(2)],
            "next_skill": util.getString(data, offGr+0x40),
            "sprites": [util.getString(data, offGr+0x48+0x08*i, util.NONE_XORKEY) for i in range(4)],
            "might": util.getByte(data, offGr+0xD5, 0xD2),
        }]
    return result

def parseFriendDouble(data):#Allegiance Battle
    result = []
    nbGroup = util.getLong(data,0x08, 0xc0f4be0d2ed1f055)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0xB0 * iGr
        result += [{
            "season_id": util.getString(data, offGr+0x00),
            "unit_id": util.getString(data, offGr+0x08),
            "map_id": util.getString(data, offGr+0x10),
            "a": hex(util.getLong(data, offGr+0x18)),
            #"avail": util.getAvail(data, offGr+0x20),
            #unknow 0x01
            #padding 0x07
            "origins": hex(util.getLong(data, offGr+0x48)),
            "origins1": hex(util.getLong(data, offGr+0x50)),
            "origins2": hex(util.getLong(data, offGr+0x58)),
            "origins3": hex(util.getLong(data, offGr+0x60)),
            "origins4": hex(util.getLong(data, offGr+0x68)),
            "origins5": hex(util.getLong(data, offGr+0x70)),
            "origins6": hex(util.getLong(data, offGr+0x78)),
            "origins7": hex(util.getLong(data, offGr+0x80)),
            "origins8": hex(util.getLong(data, offGr+0x88)),#ptr
            "origins9": hex(util.getLong(data, util.getLong(data, offGr+0x90)+0x04)),
            #"score_rewards": hex(util.getLong(data, offGr+0x98)),#tbl cellsize:0x18
            #"rank_rewards": hex(util.getLong(data, offGr+0xA0)),#tbl cellsize:0x18
            "origins12": hex(util.getLong(data, offGr+0xA8)),
        }]
    return result#data f13f93d09e0f5af7

def parseLoginBonus(data):
    result = []
    result += [util.getString(data, 0x00, util.LOGIN_XORKEY)]
    
    result += [util.xorString(data[0x40:], util.NONE_XORKEY)]
    return result

def reverseFile(file: str):
    initS = util.decompress(file)
    s = initS[0x20:]

    if file.find("/Message/") != -1:
        return parseMsg(s)
    elif file.find("/Mission/") != -1:
        return parseQuests(s)
    elif file.find("/LoginBonus/") != -1:
        print(json.dumps(parseLoginBonus(s), indent=2, ensure_ascii=False))
        return
    elif file.find("/DressAccessory/Data/") != -1:
        print(json.dumps(parseAccessory(s), indent=2, ensure_ascii=False))
        return
    elif file.find("/SRPG/Skill/") != -1:
        print(json.dumps(parseSkill(s), indent=2, ensure_ascii=False))
        return
    elif file.find("/SRPG/Person/") != -1:
        return parsePerson(s)
    elif file.find("/SRPG/Enemy/") != -1:
        return parseEnemy(s)

    elif file.find("/SRPG/Field/") != -1:
        return parseField(s)
    elif file.find("/SRPG/StageBgm/") != -1:
        return parseStageBGM(s, initS[:0x20])
    elif file.find("/SRPG/StageScenario/") != -1:
        return parseStageScenario(s)
    elif file.find("/SRPG/StageEvent/") != -1:
        return parseStageEvent(s)
    elif file.find("/SRPG/StagePuzzle/") != -1:
        return parseStagePuzzle(s)
    elif file.find("/SRPGMap/") != -1:
        return parseSRPGMap(s)

    elif file.find("/SRPG/SequentialMap/") != -1:
        return parseSequentialMap(s)
    elif file.find("/TapAction/TapBattleData/") != -1:
        return parseTapAction(s)
    elif file.find("/Portrait/") != -1:
        return parsePortrait(s)
    elif file.find("/Shadow/") != -1:
        return parseShadow(s)
    elif file.find("/Trip/Terms/") != -1:
        return parseTrip(s)
    elif file.find("/SRPG/IdolTower/") != -1:
        return parseIdolTower(s)
    elif file.find("/Mjolnir/BattleData/") != -1:
        return parseMjolnir(s)
    elif file.find("/Encourage/") != -1:
        return parseEncourage(s)
    elif file.find("/SRPG/BoardGame/") != -1:
        return parseBoardGame(s)
    else:
        print(file + ": Unknow reversal method")
        return

def parseDir(path: str, updateName: str):
    for d in listdir(path):
        if search(updateName + r'\.bin\.lz$', d):
            s = reverseFile(path + '/' + d)
            if s:
                try:
                    newFile = path.replace(BINLZ_ASSETS_DIR_PATH, JSON_ASSETS_DIR_PATH).replace('/files/assets/', '/extras/') + '/' + d.replace('.bin.lz', '.json')
                    json.dump(s, open(newFile, 'x'), indent=2, ensure_ascii=False)
                    print("File " + newFile + " create")
                except FileExistsError:
                    print("File already exist")
        elif isdir(path + '/' + d):
            parseDir(path + '/' + d, argv[1])

from sys import argv
from re import search
from os import listdir
from os.path import isfile, isdir, dirname, realpath

exec(open(dirname(dirname(realpath(__file__)))+'/PersonalData.py', 'r').read())
if __name__ == "__main__":
    if len(argv) == 2 and search(r'^\d+_\w+$', argv[1]):
        parseDir(BINLZ_ASSETS_DIR_PATH, argv[1])
    else:
        for i in range(1, len(argv)):
            s = reverseFile(argv[i])
            if s:
                print(json.dumps(s, indent=2, ensure_ascii=False))
