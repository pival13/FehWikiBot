#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parsePortrait(data):
    result = []
    nbGroup = util.getLong(data, 0x00, 0x00)
    for iGr in range(1):
        offGr = util.getLong(data, 0x08) + 0xF8*iGr
        result += [{
            'id_tag': util.getString(data, offGr+0x00, util.PORTRAIT_XORKEY),
            'id_tag2': util.getString(data, offGr+0x08, util.PORTRAIT_XORKEY),
            'title': util.getString(data, offGr+0x10, util.PORTRAIT_XORKEY),
            'original_id_tag': util.getString(data, offGr+0x18, util.PORTRAIT_XORKEY),
            'heartsPath': util.getString(data, offGr+0x20, util.PORTRAIT_XORKEY),
            'units': [util.getString(data, util.getLong(data, offGr+0x28)+0x08*i, util.PORTRAIT_XORKEY) for i in range(4)],
            'unknow1': [util.getLong(data, util.getLong(data, offGr+0x30)+0x08*i, 0x88DBEFAC) for i in range(util.getInt(data, offGr+0xBC, 0xECA8A241))],
            'stages': [{
                'base_point': util.getInt(data, util.getLong(data, offGr+0x38)+0x10*i, 0x615CDAF3),
                'unknow1': util.getInt(data, util.getLong(data, offGr+0x38)+0x10*i+0x04, 0x09B40F9D),
                'difficulty': util.getShort(data, util.getLong(data, offGr+0x38)+0x10*i+0x08, 0x5B22),
                'rarity': util.getShort(data, util.getLong(data, offGr+0x38)+0x10*i+0x0A, 0x471D),
                'delta_level': util.getSShort(data, util.getLong(data, offGr+0x38)+0x10*i+0x0C, 0xA671),
                'unknow2': util.getShort(data, util.getShort(data, offGr+0x38)+0x10*i+0x0E, 0xD84B),
            } for i in range(util.getInt(data, offGr+0xC0, 0xE8559E6C))],
            'unknow3': {
                'unknwo1': hex(util.getLong(data, util.getLong(data, offGr+0x40), 0xE649FB65D07C8FB9)),
                'unknwo2': hex(util.getInt(data, util.getLong(data, offGr+0x40)+0x08, 0x377815DC)),
                'unknow3': [{
                    #TODO percentage rate of time mult?
                    'unknow1': hex(util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x40)+0x10)+0x08*i, 0x2E833190)),
                    'unknow2': hex(util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x40)+0x10)+0x08*i+0x04, 0x51220200)),
                } for i in range(3)],
            },
            'bonus_units': [util.getLong(data, util.getLong(data, offGr+0x48)+0x08*i, 0x5B08CD8C) for i in range(util.getInt(data, offGr+0xC8, 0x52974491))],
            'score_mult': [{
                'drops': util.getInt(data, util.getLong(data, offGr+0x50)+0x08*i, 0x5F1684B1),
                'mult': util.getInt(data, util.getLong(data, offGr+0x50)+0x08*i+0x04, 0x9225CDF9)
            } for i in range(util.getInt(data, offGr+0xCC, 0x07C5C47C))],
            'unknow5': [util.getInt(data, util.getLong(data, offGr+0x58)+0x08*i, 0xD07D040F) for i in range(util.getInt(data, offGr+0xD0, 0x66A383C2))],
            'bonus_accessories': [util.getString(data, util.getLong(data, offGr+0x60)+0x08*i, util.PORTRAIT_XORKEY) for i in range(util.getInt(data, offGr+0xD4, 0x54236634))],
            'hero_rewards': [{
                'unit': util.getLong(data, util.getLong(data, offGr+0x68)+0x28*i+0x00, 0x0100) >> 3,
                'score': util.getInt(data, util.getLong(data, offGr+0x68)+0x28*i+0x08, 0x37CB7986),
                'payload_size': util.getInt(data, util.getLong(data, offGr+0x68)+0X28*i+0x0C, 0x3B9EB0D7),
                'reward': util.getReward(data, util.getLong(data, offGr+0x68)+0x28*i+0x10, util.getInt(data, util.getLong(data, offGr+0x68)+0X28*i+0x0C, 0x3B9EB0D7)),
                'id_tag': util.getString(data, util.getLong(data, offGr+0x68)+0x28*i+0x18, util.PORTRAIT_XORKEY),
                'id_tag2': util.getString(data, util.getLong(data, offGr+0x68)+0x28*i+0x20, util.PORTRAIT_XORKEY),
            } for i in range(util.getInt(data, offGr+0xD8, 0x7AA1F6C2)*util.getInt(data, offGr+0xB8, 0xBA6E2D66))],
            'daily_rewards': [{
                #Unknow 0x14
                'day': util.getInt(data, util.getLong(data, offGr+0x70)+0x30*i+0x14, 0xA3F0477C),
                'reward': util.getReward(data, util.getLong(data, offGr+0x70)+0x30*i+0x18, 72),
                'id_tag': util.getString(data, util.getLong(data, offGr+0x70)+0x30*i+0x20, util.PORTRAIT_XORKEY),
                'id_tag2': util.getString(data, util.getLong(data, offGr+0x70)+0x30*i+0x28, util.PORTRAIT_XORKEY),
            } for i in range(util.getInt(data, offGr+0xDC, 0xDD5F9DF4))],
            'unknow6': [],#x4
            'unknow7': [],#x4
            'unknow8': [],#x?
            'event_avail': util.getAvail(data, offGr+0x90),
            'units_count': util.getInt(data, offGr+0xB8, 0xBA6E2D66),
            'unknow1_count': util.getInt(data, offGr+0xBC, 0xECA8A241),
            'stages_count': util.getInt(data, offGr+0xC0, 0xE8559E6C),
            'unknow3_count': util.getInt(data, offGr+0xC4, 0x6F889C0C),#TODO
            'bonus_count': util.getInt(data, offGr+0xC8, 0x52974491),
            'score_mult_count': util.getInt(data, offGr+0xCC, 0x07C5C47C),
            'unknow5_count': util.getInt(data, offGr+0xD0, 0x66A383C2),
            'accessory_count': util.getInt(data, offGr+0xD4, 0x54236634),
            'hero_reward_count': util.getInt(data, offGr+0xD8, 0x7AA1F6C2),
            'daily_reward_count': util.getInt(data, offGr+0xDC, 0xDD5F9DF4),

            #D2 44 A9 89  64 98 A1 55  76 EA B2 CA 6B 58 31 5B 3D 9D 0B BB F4 BD D0 FF
            #D2 44 A9 89  64 98 A1 55  76 EA B2 CA 6B 58 31 5B 3D 9D 0B BB F4 BD D0 FF
            #D2 44 A9 89  64 98 A1 55  77 EA B2 CA 6B 58 31 5B 3D 9D 0B BB F4 BD D0 FF
        }]
    return result

def reverseForgingBonds(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Portrait/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parsePortrait(data[0x20:])


from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reverseForgingBonds(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))