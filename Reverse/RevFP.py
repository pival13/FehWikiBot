#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseEncourage(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x28d64acc)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x80*iGr
        result += [{
            "id_tag": util.getString(data, offGr),
            "avail": util.getAvail(data, offGr+0x08),
            #"": util.getLong(data, offGr+0x30), #0x10 + 5*0x04
            "heroes": [util.getString(data, util.getLong(data, offGr+0x58)+i*0x08) for i in range(4)],
            "bosses": [util.getString(data, util.getLong(data, offGr+0x60)+i*0x08) for i in range(3)],
            "rank_rewards": [{
                "rewards": util.getReward(data, util.getLong(data, offGr+0x68)+i*0x18, util.getLong(data, util.getLong(data, offGr+0x68)+i*0x18+0x08, 0x30df0759)),
                "payload_size": util.getLong(data, util.getLong(data, offGr+0x68)+i*0x18+0x08, 0x30df0759),
                "rank_hi": util.getInt(data, util.getInt(data, offGr+0x68)+i*0x18+0x10, 0x7e434e0f),
                "rank_lo": util.getSInt(data, util.getInt(data, offGr+0x68)+i*0x18+0x14, 0x994dfb6c),
            } for i in range(9)],
            "boss_rewards": [{
                "rewards": util.getReward(data, util.getLong(data, offGr+0x70)+i*0x10, util.getLong(data, util.getLong(data, offGr+0x70)+i*0x10+0x08, 0x30df0759)),
                "payload_size": util.getLong(data, util.getLong(data, offGr+0x70)+i*0x10+0x08, 0x30df0759),
            } for i in range(3)],
            "daily_rewards": [{
                "rewards": util.getReward(data, util.getLong(data, offGr+0x78)+i*0x10, util.getLong(data, util.getLong(data, offGr+0x78)+i*0x10+0x08, 0x30df0759)),
                "payload_size": util.getLong(data, util.getLong(data, offGr+0x78)+i*0x10+0x08, 0x30df0759),
            } for i in range(5)]
        }]
    return result
    
#FP1   #27 F5 07 17  8D 71 BB 75  01 FC 60 0D  8C 80 E2 9F  52 96 47 C9  AC 74 5B A2     02 03 84 12 4D 8F 91 3C  25 DC 9B 12 00 00 00 00
#FP2   #27 F5 07 17  8D 71 BB 75  01 FC 60 0D  8C 80 E2 9F  52 96 47 C9  AC 74 5B A2     B2 01 84 12 4D 8F 91 3C  25 DC 9B 12 00 00 00 00
#FP3   #27 F5 07 17  8D 71 BB 75  01 FC 60 0D  8C 80 E2 9F  52 96 47 C9  AC 74 5B A2     42 05 84 12 4D 8F 91 3C  25 DC 9B 12 00 00 00 00

def reverseFrontlinePhalanx(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Encourage/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseEncourage(data[0x20:])


from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reverseFrontlinePhalanx(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))