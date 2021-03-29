#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseMjolnir(data):
    result = []
    nbGroup = util.getLong(data,0x08)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x10+0x08*iGr)
        result += [{
            "id_tag": util.getString(data, offGr),
            "bonus_structure": util.getString(data, offGr+0x08),
            "bonus_structure_next": util.getString(data, offGr+0x10),
            "unit_id": util.getString(data, offGr+0x18),
            "map_id": util.getString(data, offGr+0x20),
            "rewards": [{
                "kind": util.getInt(data, util.getLong(data, offGr+0x28)+0x28*i+0x00, 0xb78d759e),
                "tier_hi": util.getInt(data, util.getLong(data, offGr+0x28)+0x28*i+0x04, 0x55d7f567),
                "tier_lo": util.getInt(data, util.getLong(data, offGr+0x28)+0x28*i+0x08, 0xf77f40bc),
                "payload_size": util.getInt(data, util.getLong(data, offGr+0x28)+0x28*i+0x0C, 0x487e08),
                "reward": util.getReward(data, util.getLong(data, offGr+0x28)+0x28*i+0x10, util.getInt(data, util.getLong(data, offGr+0x28)+0x28*i+0x0C, 0x487e08)),
                "reward_id": util.getString(data, util.getLong(data, offGr+0x28)+0x28*i+0x18),
            } for i in range(util.getInt(data, offGr+0xd8, 0xd5a73af1))],
            "tiers": [{
                "score_multiplier": util.getShort(data, util.getLong(data, offGr+0x30)+0x08*i, 0xddd9) / 100.,
                "tier": util.getShort(data, util.getLong(data, offGr+0x30)+0x08*i+0x02, 0x3472),
                "percent_down": util.getSByte(data, util.getLong(data, offGr+0x30)+0x08*i+0x04, 0x66),
                "percent_up": util.getSByte(data, util.getLong(data, offGr+0x30)+0x08*i+0x05, 0xe7),
                "percent_2up": util.getSByte(data, util.getLong(data, offGr+0x30)+0x08*i+0x06, 0x39),
                "percent_3up": util.getSByte(data, util.getLong(data, offGr+0x30)+0x08*i+0x07, 0x4e),
            } for i in range(21)],
            "_unknow1": [hex(util.getLong(data, util.getLong(data, offGr+0x38)+0x08*i)) for i in range(5)],
            "combat_stats": [{
                "unknow": hex(util.getShort(data, util.getLong(data, offGr+0x40)+0x08*i, 0x00)),
                "beginner_hp": util.getByte(data, util.getLong(data, offGr+0x40)+0x08*i+0x02, 0x76),
                "intermediate_hp": util.getByte(data, util.getLong(data, offGr+0x40)+0x08*i+0x03, 0xbe),
                "advanced_hp": util.getByte(data, util.getLong(data, offGr+0x40)+0x08*i+0x04, 0xa3),
                "score_bonus": util.getByte(data, util.getLong(data, offGr+0x40)+0x08*i+0x05, 0xb5),
            } for i in range(util.getInt(data, offGr+0xe4, 0xfc7d0e75))],
            "event_avail": util.getAvail(data, offGr+0x48),
            "shield_avail": util.getAvail(data, offGr+0x70),
            "counter_avail": util.getAvail(data, offGr+0x98),
            #"_unknow5": hex(util.getLong(data, offGr+0xc0)),#0x10
            "origins": bin(util.getInt(data, offGr+0xd0, 0xc8f81eca)),
            #"_unknow6": hex(util.getInt(data, offGr+0xd4)),#0x04
            "nb_rewards": util.getInt(data, offGr+0xd8, 0xd5a73af1),
            #"_unknow7": hex(util.getLong(data, offGr+0xdc)),#0x08
            "nb_combat_stats": util.getInt(data, offGr+0xe4, 0xfc7d0e75),
            #"_unknow8": hex(util.getShort(data, offGr+0xe8)),#0x02
            "unknow": hex(util.getShort(data, offGr+0xea)),
            #"_unknow9": hex(util.getLong(data, offGr+0xec)),#0x09
            "season": util.getByte(data, offGr+0xf5, 0x1c),
            #"_unknow10": hex(util.getLong(data, ofGr+0xf6)),#0x0c
            #padding 0x08
        }]
    return result

def reverseMjolnirsStrike(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Mjolnir/BattleData/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseMjolnir(data[0x20:])


from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reverseMjolnirsStrike(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))