#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseOccupation(data):
    result = []
    for iGr in range(util.getLong(data, 0x08, 0x0D570F0D1F9FBCFB)):
        offGr = util.getLong(data, 0x00) + 0x148*iGr
        result += [{
            'id_tag': util.getString(data, offGr+0x00),
            'pre_register_avail': util.getAvail(data, offGr+0x08),
            'event_avail': util.getAvail(data, offGr+0x30),
            'battles': [{
                'avail': util.getAvail(data, offGr+0x58+0x30*i),
                'world_id': util.getString(data, offGr+0x80+0x30*i)
            } for i in range(3)],
            # 0x18
            'leaders': [util.getString(data, offGr+0x100+0x08*i) for i in range(3)],
            'str1': util.getString(data, offGr+0x118),
            'str2': util.getString(data, offGr+0x120),
            'rewards': [{
                'type': util.getInt(data, util.getLong(data, offGr+0x128)+0x08+0x38*i+0x00, 0xeb2a77ac),
                'round': util.getSInt(data, util.getLong(data, offGr+0x128)+0x08+0x38*i+0x04, 0xe972c5cf),
                'reward_ids': [util.getString(data, util.getLong(data, offGr+0x128)+0x08+0x38*i+0x08+0x08*j) for j in range(3)],
                'lower_bound': util.getSInt(data, util.getLong(data, offGr+0x128)+0x08+0x38*i+0x20, 0x9f826f19),
                'upper_bound': util.getSInt(data, util.getLong(data, offGr+0x128)+0x08+0x38*i+0x24, 0xb0cad1b4),
                'unknow5': hex(util.getInt(data, util.getLong(data, offGr+0x128)+0x08+0x38*i+0x28, 0xba8363bb)),
                'payload': util.getInt(data, util.getLong(data, offGr+0x128)+0x08+0x38*i+0x2C, 0xA42C6D66),
                'reward': util.getReward(data, util.getLong(data, offGr+0x128)+0x08+0x38*i+0x30, util.getInt(data, util.getLong(data, offGr+0x128)+0x08+0x38*i+0x2C, 0xA42C6D66))
            } for i in range(util.getLong(data, util.getLong(data, offGr+0x128)+0x00, 0xd807ab12a683f229))],
            'tiers': [{
                'tier': util.getInt(data, util.getLong(data, offGr+0x130)+0x08+0x10*i+0x00, 0xF42E5E1F),
                'required_exp': util.getInt(data, util.getLong(data, offGr+0x130)+0x08+0x10*i+0x04, 0xFE92BD91),
                'bonus': util.getInt(data, util.getLong(data, offGr+0x130)+0x08+0x10*i+0x08, 0x10ED732F),
                '_unknow': util.getInt(data, util.getLong(data, offGr+0x130)+0x08+0x10*i+0x0C, 0x0599CB0B)
            } for i in range(util.getLong(data, util.getLong(data, offGr+0x130)+0x00, 0x34e1996887fd831d))],
            'random_drop': [{
                'proba': util.getInt(data, util.getLong(data, offGr+0x138)+0x08+0x10*i+0x00, 0x80EEA211),
                'payload': util.getInt(data, util.getLong(data, offGr+0x138)+0x08+0x10*i+0x04, 0x97E9A4BF),
                'reward': util.getReward(data, util.getLong(data, offGr+0x138)+0x08+0x10*i+0x08, 72)
            } for i in range(util.getLong(data, util.getLong(data, offGr+0x138)+0x00, 0xb1f0f893541e9ff8))],
            'area_controlled_bonus': [{
                'min_area': util.getInt(data, util.getLong(data, offGr+0x140)+0x08+0x10*i+0x00, 0xefc80164),
                'max_area': util.getSInt(data, util.getLong(data, offGr+0x140)+0x08+0x10*i+0x04, 0x9628f35f),
                'point': util.getInt(data, util.getLong(data, offGr+0x140)+0x08+0x10*i+0x08, 0x654f4e76),
                '_unknow1': util.getInt(data, util.getLong(data, offGr+0x140)+0x08+0x10*i+0x0c, 0x17e92754)
            } for i in range(util.getLong(data, util.getLong(data, offGr+0x140)+0x00, 0xa4fff24dc6150332))],
        }]
    return result

def reverseGrandConquests(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Occupation/Data/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseOccupation(data[0x20:])


from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reverseGrandConquests(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))