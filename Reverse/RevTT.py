#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseSequentialMap(data):
    result = []
    nbGroup = util.getLong(data, 0x08, 0x37cfee6c5195437)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x00*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "banner_id": util.getString(data, offGr+0x08),
            "id_tag2": util.getString(data, offGr+0x10),
            "full_id_tag": util.getString(data, offGr+0x18),
            "avail": util.getAvail(data, offGr+0x20),
            "bonus_units1": {
                "units": [util.getString(data, util.getLong(data, util.getLong(data, offGr+0x48)) + 0x08*i)
                    for i in range(util.getInt(data, util.getLong(data, offGr+0x48)+0x08, 0xf3470912))],
                "bonus": util.getInt(data, util.getLong(data, offGr+0x48)+0x0c, 0x88f82c4b),
            },
            "bonus_units2": {
                "units": [util.getString(data, util.getLong(data, util.getLong(data, offGr+0x50)) + 0x08*i)
                    for i in range(util.getInt(data, util.getLong(data, offGr+0x50)+0x08, 0xf3470912))],
                "bonus": util.getInt(data, util.getLong(data, offGr+0x50)+0x0c, 0x88f82c4b),
            },
            "survival_bonus": [{
                "rank": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x58))+0x10*i+0x00),
                "team_lost": util.getSInt(data, util.getLong(data, util.getLong(data, offGr+0x58))+0x10*i+0x08, 0x88F494D0),
                "mult": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x58))+0x10*i+0x0C, 0x608B1F2C)
            } for i in range(util.getInt(data, util.getLong(data, offGr+0x58)+0x08, 0xA8F24510))],
            "speed_bonus": [{
                "rank": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x10*i+0x00),
                "extra_turns": util.getSInt(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x10*i+0x08, 0x88F494D0),
                "mult": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x10*i+0x0C, 0x608B1F2C)
            } for i in range(util.getInt(data, util.getLong(data, offGr+0x60)+0x08, 0xA8F24510))],
            "_unknow1": {
                "_unknow2": hex(util.getLong(data, util.getLong(data, offGr+0x68))),
            },
            "score_rewards": [{
                "rewards": util.getReward(data, util.getLong(data, util.getLong(data, offGr+0x70))+i*0x20, util.getLong(data, util.getLong(data, util.getLong(data, offGr+0x70))+i*0x20 + 0x08, 0x5a029dec)),
                "payload_size": util.getLong(data, util.getLong(data, util.getLong(data, offGr+0x70))+i*0x20 + 0x08, 0x5a029dec),
                "reward_id": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x70))+i*0x20 + 0x10),
                "score": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x70))+i*0x20 + 0x18, 0xf342cbbd),
            } for i in range(util.getLong(data, util.getLong(data, offGr+0x70)+0x08, 0x629988e0))],
            "rank_rewards": [{
                "rewards": util.getReward(data, util.getLong(data, util.getLong(data, offGr+0x78))+i*0x20, util.getLong(data, util.getLong(data, util.getLong(data, offGr+0x78))+i*0x20 + 0x08, 0x4db73c78)),
                "payload_size": util.getLong(data, util.getLong(data, util.getLong(data, offGr+0x78))+i*0x20 + 0x08, 0x4db73c78),
                "reward_id": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x78))+i*0x20 + 0x10),
                "rank_hi": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x78))+i*0x20 + 0x18, 0xc1805a3c),
                "rank_lo": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x78))+i*0x20 + 0x1c, 0xd5f99032),
            } for i in range(util.getLong(data, util.getLong(data, offGr+0x78)+0x08, 0xd5f99032))],
            "target_bonus": [{
                "target": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x80))+0x08*i+0x00, 0x4e2d3d06),
                "bonus": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x80))+0x08*i+0x04, 0xb48ec15a),
            } for i in range(util.getLong(data, util.getLong(data, offGr+0x80)+0x08, 0xEAF41B8B))],#0x25E8 b48e020a
            "sets": []
        }]
        for iSet in range(util.getLong(data, offGr+0x90, 0xc33b272f)):
            offSet = util.getLong(data, util.getLong(data, offGr+0x88)+0x08*iSet)
            result[iGr]['sets'] += [{
                "set_id": util.getString(data, offSet),
                "battles": [{
                    "maps": [util.getString(data, util.getLong(data, util.getLong(data, offSet+0x08)+0x20*iBa)+0x08*i) for i in range(util.getLong(data, util.getLong(data, offSet+0x08)+0x20*iBa+0x08, 0x2031150d))],
                    "foe_count": util.getByte(data, util.getLong(data, offSet+0x08)+0x20*iBa+0x10, 0x4f),
                    "rarity": util.getByte(data, util.getLong(data, offSet+0x08)+0x20*iBa+0x12, 0x56),
                    "level": util.getByte(data, util.getLong(data, offSet+0x08)+0x20*iBa+0x13, 0x28),
                    "hp_factor": util.getShort(data, util.getLong(data, offSet+0x08)+0x20*iBa+0x14, 0x4555),
                    "use_random_assist": util.getBool(data, util.getLong(data, offSet+0x08)+0x20*iBa+0x18, 0x51),
                    "use_random_passive": util.getBool(data, util.getLong(data, offSet+0x08)+0x20*iBa+0x19, 0x9e),
                } for iBa in range(util.getInt(data, offSet+0x18, 0x1d2b72cb))],
                "enemies": [util.getString(data, util.getLong(data, offSet+0x10)+i*0x08) for i in range(util.getInt(data, offSet+0x1c, 0x5ee8f0c4))],
                "battle_count": util.getInt(data, offSet+0x18, 0x1d2b72cb),
                "enemy_count": util.getInt(data, offSet+0x1c, 0x5ee8f0c4),
                "difficulty": util.getInt(data, offSet+0x20, 0xc28919b6),
                "stamina": util.getInt(data, offSet+0x24, 0x7ad1f34),
                "base_score": util.getInt(data, offSet+0x28, 0x65fb2a5e),
                "team_count": util.getInt(data, offSet+0x2c, 0xd4eaabad),
                "turn_limit": util.getInt(data, offSet+0x30, 0x0DC968F3),
            }]
    return result

def reverseTempestTrial(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/SRPG/SequentialMap/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseSequentialMap(data[0x20:])

from sys import argv, stderr, exc_info

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reverseTempestTrial(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))