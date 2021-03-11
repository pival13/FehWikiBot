#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseIdolTower(data):
    result = []
    for iGr in range(util.getLong(data, 0x08, 0x037CFEE6C5195437)):
        offGr = util.getLong(data, 0x00) + 0x00*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "avail": util.getAvail(data, offGr+0x08),
            "forma_soul_avail": util.getAvail(data, offGr+0x30),
            "forma": {
                "heroes": [util.getString(data, util.getLong(data, offGr+0x58)+0x08*i) for i in range(4)],
                "rarity": util.getByte(data, util.getLong(data, offGr+0x58)+0x20, 0x9E),
                "lv": util.getByte(data, util.getLong(data, offGr+0x58)+0x21, 0x2A),
            },
            "chambers": [{
                #util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i
                "id_tag": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x00),
                #"unknow": 0x06
                "id_num": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x10, 0xAC3AB736),
                "difficulty": util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x14, 0xCB),
                "rarity": util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x15, 0x69),
                "true_lv": util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x16, 0x6E),
                "hp_factor": util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x18, 0x1618),
                #"unknow": 0x06
                "generic_foes": util.getBool(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x20, 0xd3),
                "fixed_classes": util.getBool(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x21, 0x3B),
                "allow_refines": util.getBool(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x22, 0x7F),
                "reward": util.getReward(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x28, util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x30, 0xAE4D663F)),
                "payload": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x30, 0xAE4D663F),
                "reward_id_suffix": [util.getString(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x50*i+0x38+0x08*j) for j in range(3)],
            } for i in range(util.getInt(data, util.getLong(data, offGr+0x60)+0x08, 0x6AC1C456))],
            "daily_bonuses": [{
                "reward": util.getReward(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i, util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i+0x08, 0x33287F60)),
                "payload": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i+0x08, 0x33287F60),
                "reward_id_suffix": [util.getString(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i+0x10+0x08*j) for j in range(3)],
            } for i in range(util.getInt(data, util.getLong(data, offGr+0x68)+0x08, 0x35F7601A))],
            "unknown": hex(util.getLong(data, offGr+0x70)),
        }]
    return result

def reverseHallOfForms(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/SRPG/IdolTower/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseIdolTower(data[0x20:])


from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reverseHallOfForms(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))