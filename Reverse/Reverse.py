#!/usr/bin/env python3

from subprocess import Popen, PIPE, STDOUT
import json

from datetime import datetime, date, timedelta
from os.path import dirname, realpath

import REutil as util

"""
BIN.LZ Header:
TotalSize: 0x04
CorpseSize: 0x04
PtrTableCount: 0x04 (0x08 each: adress of a pointer)
StringTableSize: 0x04 (0x08 each : corpseIdx (0x04), tblStringIdx (0x04))
XXX: 0x04
XXX: 0x04
"""

from RevData  import parseMsg
from RevSound import parseSound, parseStageBGM
from RevMap   import parseField, parseSRPGMap, parseStageScenario, parseStageEvent, parseStagePuzzle
from RevUnit  import parsePerson, parseEnemy, parseSubscriptionCostume
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
from RevHJ  import parseJourney

def parseAccessory(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x0de4c6f0ab07e0e13)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x20*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "sprite": util.getString(data, offGr+0x08),
            "id_num": util.getInt(data, offGr+0x10, 0xf765ad9c),
            "sort_id": util.getInt(data, offGr+0x14, 0x0159b21d),
            "acc_type": util.getInt(data, offGr+0x18, 0x8027f6f6),
            "summoner": util.getBool(data, offGr+0x1c, 0xB7)
        }]
    return result

def parseSkill(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x7fecc7074adee9ad)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x158*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "refine_base": util.getString(data, offGr+0x08),
            "name_id": util.getString(data, offGr+0x10),
            "desc_id": util.getString(data, offGr+0x18),
            "refine_id": util.getString(data, offGr+0x20),
            "beast_effect_id": util.getString(data, offGr+0x28),
            "prerequisites": [util.getString(data, offGr+0x30+0x08*i) for i in range(2)],
            "next_skill": util.getString(data, offGr+0x40),
            "sprites": [util.getString(data, offGr+0x48+0x08*i, util.NONE_XORKEY) for i in range(4)],
            "stats": util.getStat(data, offGr+0x68),
            "class_params": util.getStat(data, offGr+0x78),
            "combat_buffs": util.getStat(data, offGr+0x88),
            "skill_params": util.getStat(data, offGr+0x98),
            "skill_params2": util.getStat(data, offGr+0xA8),
            "refine_stats": util.getStat(data, offGr+0xB8),
            "id_num": util.getInt(data, offGr+0xC8, 0xc6a53a23),
            "sort_id": util.getInt(data, offGr+0xCC, 0x8DDBF8AC),
            "icon_id": util.getInt(data, offGr+0xD0, 0xC6DF2173),
            "wep_equip": util.getInt(data, offGr+0xD4, 0x35B99828),
            "mov_equip": util.getInt(data, offGr+0xD8, 0xAB2818EB),
            "sp_cost": util.getInt(data, offGr+0xDC, 0xC031F669),
            "category": util.getByte(data, offGr+0xE0, 0xBC),
            "tome_class": util.getByte(data, offGr+0xE1, 0xF1),
            "exclusive": util.getBool(data, offGr+0xE2, 0xCC),
            "enemy_only": util.getBool(data, offGr+0xE3, 0x4F),
            "range": util.getByte(data, offGr+0xE4, 0x56),
            "might": util.getByte(data, offGr+0xE5, 0xD2),
            "cooldown_count": util.getSByte(data, offGr+0xE6, 0x56),
            "assist_cd": util.getBool(data, offGr+0xE7, 0xF2),
            "healing": util.getBool(data, offGr+0xE8, 0x95),
            "skill_range": util.getByte(data, offGr+0xE9, 0x09),
            "score": util.getShort(data, offGr+0xEA, 0xA232),
            "promotion_tier": util.getByte(data, offGr+0xEC, 0xE0),
            "promotion_rarity": util.getByte(data, offGr+0xED, 0x75),
            "refined": util.getBool(data, offGr+0xEE, 0x02),
            "refine_sort_id": util.getByte(data, offGr+0xEF, 0xFC),
            "wep_effective": util.getInt(data, offGr+0xF0, 0x23BE3D43),
            "mov_effective": util.getInt(data, offGr+0xF4, 0x823FDAEB),
            "wep_shield": util.getInt(data, offGr+0xF8, 0xAABAB743),
            "mov_shield": util.getInt(data, offGr+0xFC, 0x0EBEF25B),
            "wep_weakness": util.getInt(data, offGr+0x100, 0x005A02AF),
            "mov_weakness": util.getInt(data, offGr+0x104, 0xB269B819),
            "wep_adaptive": util.getInt(data, offGr+0x108, 0x494E2629),
            "mov_adaptive": util.getInt(data, offGr+0x10C, 0xEE6CEF2E),
            "timing_id": util.getInt(data, offGr+0x110, 0x9C776648),
            "ability_id": util.getInt(data, offGr+0x114, 0x72B07325),
            "limits": [{
                "id": util.getInt(data, offGr+0x118+0x08*i, 0x0EBDB832),
                "params": [util.getSShort(data, offGr+0x118+0x08*i+0x04+0x02*j, 0xA590) for j in range(2)],
            } for i in range(2)],
            "target_wep": util.getInt(data, offGr+0x128, 0x409FC9D7),
            "target_mov": util.getInt(data, offGr+0x12C, 0x6C64D122),
            "passive_next": util.getString(data, offGr+0x130),
            "timestamp": util.getSLong(data, offGr+0x138, 0xED3F39F93BFE9F51),
            "random_allowed": util.getByte(data, offGr+0x140, 0x10),
            "min_lv": util.getByte(data, offGr+0x141, 0x90),
            "max_lv": util.getByte(data, offGr+0x142, 0x24),
            "tt_inherit_base": util.getBool(data, offGr+0x143, 0x19),
            "random_mode": util.getByte(data, offGr+0x144, 0xBE),
            "limit3_id": util.getInt(data, offGr+0x148, 0x0EBDB832),
            "limit3_params": [util.getSShort(data, offGr+0x148+0x04+0x02*j, 0xA590) for j in range(2)],
            "range_shape": util.getByte(data, offGr+0x150, 0x5C),
            "target_either": util.getByte(data, offGr+0x151, 0xA7),
            "distant_counter": util.getByte(data, offGr+0x152, 0xDB),
            "canto_range": util.getByte(data, offGr+0x153, 0x41),
            "pathfinder_range": util.getByte(data, offGr+0x154, 0xBE),
        }]
    return result

def parseWeaponRefine(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x45162C00432CFD73)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x20 * iGr
        result += [{
            'orig': util.getString(data, offGr+0x00),
            'refined': util.getString(data, offGr+0x08),
            'use': [{
                'res_type': util.getShort(data, offGr+0x10+i*0x04, 0x439C),
                'count': util.getShort(data, offGr+0x12+i*0x04, 0x7444),
            } for i in range(2)],
            'give': {
                'res_type': util.getShort(data, offGr+0x18, 0x439C),
                'count': util.getShort(data, offGr+0x1A, 0x7444),
            }
        }]
    return result

def parseSkillAccessoryCreatable(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x0605B9F01A117E27)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x08 * iGr
        result += [{
            'id_tag': util.getString(data, offGr+0x00)
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

def parseBattleAsset(data):
    #return util.getAllStringsOn(data, util.BATTLE_XORKEY)
    getString = lambda data, off: util.getString(data, off, util.BATTLE_XORKEY)
    offGr = [util.getLong(data, 0x00+0x10*i) for i in range(6)]
    return {
        "unitData": [{
            "id_tag": getString(data, offGr[0]+0x90*iGr+0x00),
            # 0x18,
            "shorts": [hex(util.getShort(data, offGr[0]+0x90*iGr+0x08+0x02*i, 0x3FD0)) for i in range(0x0C)],
            "name1": getString(data, offGr[0]+0x90*iGr+0x20),
            # 0x08
            "ptr1?": util.getLong(data, offGr[0]+0x90*iGr+0x30),
            "name2": getString(data, offGr[0]+0x90*iGr+0x38),
            "name22": getString(data, offGr[0]+0x90*iGr+0x40),
            "name3": getString(data, offGr[0]+0x90*iGr+0x48),
            "name4": getString(data, offGr[0]+0x90*iGr+0x50),
            # 0x08
            "name5": getString(data, offGr[0]+0x90*iGr+0x60),
            "name6": getString(data, offGr[0]+0x90*iGr+0x68),
            "name7": getString(data, offGr[0]+0x90*iGr+0x70),
            # 0x08
            "ptr8?": util.getLong(data, offGr[0]+0x90*iGr+0x80),
            "ptr9?": util.getLong(data, offGr[0]+0x90*iGr+0x88),
            # DF BA DF 07
        } for iGr in range(util.getInt(data, 0x08))],
        "magicData": [{
            # 1C B2 31 2C
        } for iGr in range(util.getInt(data, 0x18))],
        "data3": [{

        } for iGr in range(util.getInt(data, 0x28))],
        "data4": [{

        } for iGr in range(util.getInt(data, 0x38))],
        "specialData": [{

        } for iGr in range(util.getInt(data, 0x48))],
        "weaponData": [{
            # 27 8B 20 61
        } for iGr in range(util.getInt(data, 0x58))],
        "strings": util.getAllStringsOn(data, util.BATTLE_XORKEY)
    }

def parseBattleBg(data):
    TYPES = ['Normal', 'Inside', 'Desert', 'Forest', 'Sea', 'Lava', 'Bridge', 'NormalWall', 'ForestWall', 'InsideWall', 'Fortress', 'River']
    result = []
    nbGroup = util.getLong(data, 0x08, 0x3926EEACBF6214E0)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x10 * iGr
        result += [{
            'id_tag': util.getString(data, offGr+0x00, util.NONE_XORKEY),
            'backgrounds': [{
                '_type': TYPES[i],
                'name': util.getString(data, util.getLong(data, util.getLong(data, offGr+0x08)+0x08*i), util.NONE_XORKEY),
                'unknow': util.getString(data, util.getLong(data, util.getLong(data, offGr+0x08)+0x08*i)+0x08, util.NONE_XORKEY),
            } for i in range(12)]
        }]
    return result


def parseMjolnirFacility(data):
    result = []
    nbGroup = util.getInt(data, 0x08, 0xC6AC9C0F)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x80 * iGr
        result += [{
            'id_tag': util.getString(data, offGr+0x00),
            'sprite': util.getString(data, offGr+0x08),
            'broken_sprite': util.getString(data, offGr+0x10),
            '_unknow1': util.getString(data, offGr+0x18),
            'next': util.getString(data, offGr+0x20),
            'prev': util.getString(data, offGr+0x28),
            '_unknow2': util.getString(data, offGr+0x30),
            '_group_id': util.getString(data, offGr+0x38),
            '_struct_id': util.getInt(data, offGr+0x40, 0x11aa991a),
            '_struct_id2': util.getInt(data, offGr+0x44, 0x3251464d),
            'terrain_id': util.getInt(data, offGr+0x48, 0xe24a11af),
            '_unknow5': util.getInt(data, offGr+0x4C, 0x4a13cf66),
            '_unknow5-': util.getInt(data, offGr+0x50, 0x7856dae3),
            'level': util.getInt(data, offGr+0x54, 0xc54d1c6e),
            'cost': util.getInt(data, offGr+0x58, 0x85da15bc),
            '_unknow7': hex(util.getInt(data, offGr+0x5c, 0x35e586df)),
            '_unknow8': hex(util.getInt(data, offGr+0x60, 0x8de0beb1)),
            'a0': util.getInt(data, offGr+0x64, 0x69c452d9),
            '_unknow9': hex(util.getInt(data, offGr+0x68, 0x743af47c)),
            'range': util.getInt(data, offGr+0x6c, 0x84ca17f),# > 10 ? xy-range : range
            '_isGateway': util.getByte(data, offGr+0x70, 0x57),
            'effect_type': util.getByte(data, offGr+0x71, 0x70),
            'range_type': util.getSByte(data, offGr+0x72, 0x4e),
            '_unknow10': util.getByte(data, offGr+0x73, 0x85),
            'turns': util.getByte(data, offGr+0x74, 0x2d),
            'showPanelNewUpgradAvailable': util.getBool(data, offGr+0x75, 0x62),
            '_unknow11': util.getByte(data, offGr+0x76, 0x2a),
            '_unknow11-': util.getByte(data, offGr+0x77, 0x7c),
            '_isGateway2': util.getByte(data, offGr+0x78, 0x38),
            'isBase': util.getByte(data, offGr+0x79, 0xa6),
            'isSummoner': util.getBool(data, offGr+0x7a, 0x1c),
            'isSummoner2': util.getByte(data, offGr+0x7b, 0x1c),
            'isSummoner3': util.getByte(data, offGr+0x7c, 0x1c),
            'isSummoner4': util.getByte(data, offGr+0x7d, 0x1c),
            '_padding': util.getShort(data, offGr+0x7e),
        }]
    return result

def reverseFile(file: str):
    initS = util.decompress(file)
    if not initS:
        print("Failed to decompress: " + file.replace(util.BINLZ_ASSETS_DIR_PATH, '...'))
        return
    s = initS[0x20:]

    if file.find("/Message/") != -1:
        return parseMsg(s)
    elif file.find("/Mission/") != -1:
        return parseQuests(s)
    #elif file.find("/LoginBonus/") != -1:
    #    print(json.dumps(parseLoginBonus(s), indent=2, ensure_ascii=False))
    #    return
    elif file.find("/Sound/arc/") != -1:
        return parseSound(s)
    elif file.find("/DressAccessory/Data/") != -1:
        return parseAccessory(s)
    elif file.find("/SRPG/Skill/") != -1:
        return parseSkill(s)
    elif file.find("/SRPG/WeaponRefine/") != -1:
        return parseWeaponRefine(s)
    elif file.find("/SRPG/SkillAccessoryCreatable/") != -1:
        return parseSkillAccessoryCreatable(s)
    elif file.find("/SRPG/Person/") != -1:
        return parsePerson(s)
    elif file.find("/SRPG/Enemy/") != -1:
        return parseEnemy(s)
    elif file.find("/SubscriptionCostume/") != -1:
        return parseSubscriptionCostume(s)

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
    elif file.find("/Occupation/Data/") != -1:
        return parseOccupation(s)
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
    elif file.find("/Journey/Terms/") != -1:
        return parseJourney(s)
    
    elif file.find('/Battle/Asset/') != -1:
        return parseBattleAsset(s)
    elif file.find('/SRPG/BattleBg/') != -1:
        return parseBattleBg(s)
    elif file.find('/Mjolnir/FacilityData/') != -1:
        return parseMjolnirFacility(s)
    else:
        print("Unknow reversal method: " + file.replace(util.BINLZ_ASSETS_DIR_PATH, '...'))
        return

def parseDir(path: str, updateName: str):
    for d in listdir(path):
        if search(updateName + r'\.bin\.lz$', d):
            try:
                s = reverseFile(path + '/' + d)
                if s:
                    try:
                        newFile = path.replace(util.BINLZ_ASSETS_DIR_PATH, util.JSON_ASSETS_DIR_PATH) + '/' + d.replace('.bin.lz', '.json')
                        json.dump(s, open(newFile, 'x', encoding='utf-8'), indent=2, ensure_ascii=False)
                        print("File created: " + newFile.replace(util.BINLZ_ASSETS_DIR_PATH,'...'))
                    except FileExistsError:
                        print("File exist: " + path.replace(util.BINLZ_ASSETS_DIR_PATH, '...') + '/' + d.replace('.bin.lz','.json'))
            except KeyboardInterrupt:
                print('Ignored file ' + path.replace(util.BINLZ_ASSETS_DIR_PATH, '...') + '/' + d)
            except:
                print('Error with ' + path.replace(util.BINLZ_ASSETS_DIR_PATH, '...') + '/' + d)
        elif isdir(path + '/' + d):
            parseDir(path + '/' + d, argv[1])

def parseDirTime(path: str, time):
    for d in listdir(path)[::-1]:
        file = path + '/' + d
        s = stat(file)
        if S_ISDIR(s.st_mode):
            parseDirTime(file, time)
        elif d[-7:] != '.bin.lz':
            continue
        elif s.st_mtime > time and S_ISREG(s.st_mode):
            try:
                s = reverseFile(path + '/' + d)
                if s:
                    try:
                        newFile = file.replace(util.BINLZ_ASSETS_DIR_PATH, util.JSON_ASSETS_DIR_PATH).replace('.bin.lz', '.json')
                        json.dump(s, open(newFile, 'x', encoding='utf-8'), indent=2, ensure_ascii=False)
                        print("File created: " + newFile.replace(util.BINLZ_ASSETS_DIR_PATH,'...'))
                    except FileExistsError:
                        print("File exist: " + path.replace(util.BINLZ_ASSETS_DIR_PATH, '...') + '/' + d.replace('.bin.lz','.json'))
            except KeyboardInterrupt:
                print('Ignored file ' + path.replace(util.BINLZ_ASSETS_DIR_PATH, '...') + '/' + d)
            except:
                print('Error with ' + path.replace(util.BINLZ_ASSETS_DIR_PATH, '...') + '/' + d)


from sys import argv
from re import search
from os import listdir, stat
from os.path import isfile, isdir, dirname, realpath
from stat import S_ISDIR, S_ISREG

exec(open(dirname(dirname(realpath(__file__)))+'/PersonalData.py', 'r').read())
if __name__ == "__main__":
    if len(argv) == 2 and search(r'^\d+_\w+|v\d{4}[a-e]_\w+$', argv[1]):
        parseDir(util.BINLZ_ASSETS_DIR_PATH, argv[1])
    elif len(argv) == 1:
        parseDirTime(util.BINLZ_ASSETS_DIR_PATH, datetime.strptime(date.today().strftime("%Y-%m-%dT00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ").timestamp())
    else:
        for arg in argv[1:]:
            s = reverseFile(arg)
            if s:
                print(json.dumps(s, indent=2, ensure_ascii=False))
