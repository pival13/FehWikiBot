#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseTrip(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0xBBC1712B8390494C)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x90*iGr
        result += [{
            'id_tag': util.getString(data, offGr+0x00),
            'avail': util.getAvail(data, offGr+0x08),
            # util.getLong(data, offGr+0x40), #0x34
            # scoutRewardCount
            'isSpoil': util.getBool(data, offGr+0x64, 0xEC),
            '_unknow1': util.getInt(data, offGr+0x68),
            'rewardCount': util.getInt(data, offGr+0x6C, 0x6CC6FEB1),
            'entryCount': util.getInt(data, offGr+0x70, 0x9F08D577),
            'mapCount': util.getInt(data, offGr+0x74, 0xC5DBCC7B),
            'loreRewards': [{
                "reward": util.getReward(data, util.getLong(data, offGr+0x78)+0x10*i, util.getInt(data, util.getLong(data, offGr+0x78)+0x10*i+0x08, 0x83E17EF2)),
                "payload": util.getInt(data, util.getLong(data, offGr+0x78)+0x10*i+0x08, 0x83E17EF2),
                "lines": util.getInt(data, util.getLong(data, offGr+0x78)+0x10*i+0x0C, 0x37c353d3)
            } for i in range(util.getInt(data, offGr+0x6C, 0x6CC6FEB1))],
            'bonusEntry': [util.getByte(data, util.getLong(data, offGr+0x80)+i, 0x14) if util.getByte(data, util.getLong(data, offGr+0x80)+i) != 0x09 else -1 for i in range(8)],
            'maps': [{
                "id_tag": util.getString(data, util.getLong(data, offGr+0x88)+0x48*i+0x00),
                "backgroundPath": util.getString(data, util.getLong(data, offGr+0x88)+0x48*i+0x08),
                "_unknow1": util.getString(data, util.getLong(data, offGr+0x88)+0x48*i+0x10),
                "_unknowPtr": util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x18),
                "clearReward": util.getReward(data, util.getLong(data, offGr+0x88)+0x48*i+0x20, util.getInt(data, util.getLong(data, offGr+0x88)+0x48*i+0x28, 0x356ebeca)),
                "payload": util.getInt(data, util.getLong(data, offGr+0x88)+0x48*i+0x28, 0x356ebeca),
                "lines": util.getInt(data, util.getLong(data, offGr+0x88)+0x48*i+0x2C, 0x97e16af8),
                "required": [{
                    "map_idx": util.getSByte(data, util.getLong(data, offGr+0x88)+0x48*i+0x30+0x2*j, 0x1D),
                    "unknow": util.getByte(data, util.getLong(data, offGr+0x88)+0x48*i+0x30+0x2*j+0x1, 0xF1)
                } for j in range(3)],
                "_unknow2": hex(util.getShort(data, util.getLong(data, offGr+0x88)+0x48*i+0x36)),
                "scoutReward": [{
                    "reward": util.getReward(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x38)+0x10*j, util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x38)+0x10*j+0x08, 0x941587cf)),
                    "payload": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x38)+0x10*j+0x08, 0x941587cf),
                    "proba": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x38)+0x10*j+0x0C, 0xA0DC749D),
                } for j in range(18)],
                "combatUnits": {
                    'id_tag': util.getString(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)),
                    '_unknow': hex(util.getLong(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x08)),
                    'units': [{
                        'facePath': util.getString(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x10+0x20*j),
                        'name_id': util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x18+0x20*j, 0xFF),
                        'rarity': util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x19+0x20*j, 0x3B),
                        'weapon': util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x1A+0x20*j, 0xA9),
                        'move': util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x1B+0x20*j, 0xE3),
                        'effectivness': util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x1C+0x20*j, 0x7583),
                        'HP': util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x1E+0x20*j),#TODO
                        'Atk': util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x20+0x20*j, 0xB2DF),
                        'Spd': util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x22+0x20*j, 0xAE7E),
                        'Def': util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x24+0x20*j, 0x71D6),
                        'Res': util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x26+0x20*j, 0x6C67),
                        '_unknow2': util.getLong(data, util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40)+0x28+0x20*j, 0x60599D5DE82F2ECF),
                    } for j in range(4)]
                } if util.getLong(data, util.getLong(data, offGr+0x88)+0x48*i+0x40) else None,
            } for i in range(5)],
        }]
    return result

def reverseLostLore(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Trip/Terms/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseTrip(data[0x20:])


from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reverseLostLore(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))