#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseJourney(data):
    result = []
    nbGroup = util.getInt(data, 0x00, 0x00)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x08) + 0x68*iGr
        result += [{
            'id_tag': util.getString(data, offGr+0x00, util.JOURNEY_XORKEY),
            'stages': [{
                'base_memento': util.getInt(data, util.getLong(data, offGr+0x08)+0x38*i+0x00, 0x409A5DE6),
                'stamina': util.getShort(data, util.getLong(data, offGr+0x08)+0x38*i+0x04, 0x43B8),
                'difficulty': util.getShort(data, util.getLong(data, offGr+0x08)+0x38*i+0x06, 0x4AD8),
                'rarity': util.getShort(data, util.getLong(data, offGr+0x08)+0x38*i+0x08, 0x978E),
                'level': util.getSShort(data, util.getLong(data, offGr+0x08)+0x38*i+0x0A, 0x61CA),
                'nb_enemy': util.getShort(data, util.getLong(data, offGr+0x08)+0x38*i+0x0C, 0x3AE3),
                'requirement': util.getShort(data, util.getLong(data, offGr+0x08)+0x38*i+0x0E, 0xA1D1),
                'useHeroicOrdeals': util.getInt(data, util.getLong(data, offGr+0x08)+0x38*i+0x0E, 0x3552B9A6),
                #0x04 B4 4F C7 08 (B5 for stage 4)
                'payload': util.getInt(data, util.getLong(data, offGr+0x08)+0x38*i+0x18, 0xB6FBEEDD),
                'reward': util.getReward(data, util.getLong(data, offGr+0x08)+0x38*i+0x20, util.getInt(data, util.getLong(data, offGr+0x08)+0x38*i+0x18, 0xB6FBEEDD)),
                'str': util.getString(data, util.getLong(data, offGr+0x08)+0x38*i+0x28, util.JOURNEY_XORKEY),
                'str2': util.getString(data, util.getLong(data, offGr+0x08)+0x38*i+0x30, util.JOURNEY_XORKEY),
            } for i in range(util.getInt(data, offGr+0x58, 0x148AE2CB))],
            'memento_mulptiplier': [{
                'drop': util.getInt(data, util.getLong(data, offGr+0x10)+0x08*i, 0x5ACB4499),
                'mult': util.getInt(data, util.getLong(data, offGr+0x10)+0x08*i+0x04, 0xB4CF8F08),
            } for i in range(util.getInt(data, offGr+0x5C, 0xA9124C19))],
            'rewards': [{
                'points': util.getInt(data, util.getLong(data, offGr+0x18)+0x20*i+0x00, 0xB5898082),
                'payload': util.getInt(data, util.getLong(data, offGr+0x18)+0x20*i+0x04, 0x0F1649E1),
                'reward': util.getReward(data, util.getLong(data, offGr+0x18)+0x20*i+0x08, util.getInt(data, util.getLong(data, offGr+0x18)+0x20*i+0x04, 0x0F1649E1)),
                'str': util.getString(data, util.getLong(data, offGr+0x18)+0x20*i+0x10, util.JOURNEY_XORKEY),
                'str2': util.getString(data, util.getLong(data, offGr+0x18)+0x20*i+0x18, util.JOURNEY_XORKEY),
            } for i in range(util.getInt(data, offGr+0x60, 0x87071ACC))],
            'memento_event': [{
                'id_tag': util.getString(data, util.getLong(data, offGr+0x20)+0x10*i+0x00, util.JOURNEY_XORKEY),
                # 34 4E 65 BE
                # 34/36/37
                'unknow1': util.getInt(data, util.getLong(data, offGr+0x20)+0x10*i+0x08, 0xBE654E36),
                'padding': util.getInt(data, util.getLong(data, offGr+0x20)+0x10*i+0x0C),
            } for i in range(util.getInt(data, offGr+0x64, 0x338F7D50))],
            'unknow1': {
                #0x20
                # C3 8A 7E 37 A1 61 37 97 F6 47 E0 8A 3F 01 81 AE 86 90 79 E9 15 3F 71 DB 5C F2 8C 81 EC 43 58 22
            },
            'avail': util.getAvail(data, offGr+0x30),
            'stage_count': util.getInt(data, offGr+0x58, 0x148AE2CB),
            'multiplier_count': util.getInt(data, offGr+0x5C, 0xA9124C19),
            'reward_count': util.getInt(data, offGr+0x60, 0x87071ACC),
            'memento_count': util.getInt(data, offGr+0x64, 0x338F7D50),
        }]
    return result
    
def reverseHeroesJourney(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Journey/Terms/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseJourney(data[0x20:])


from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reverseHeroesJourney(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))