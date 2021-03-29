#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

getString = lambda data, off: util.getString(data, off, util.TOURNAMENT_XORKEY)

def parseTournament(data):
    result = []
    nbGroup = util.getLong(data, 0x08)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x10+0x08*iGr)
        # Old content
        #result += [{
        #    'units': [getString(data, offGr+0x08*i) for i in range(8)],
        #    'reward_count': util.getInt(data, offGr+0x40),
        #    'flag_multiplier_count': util.getInt(data, offGr+0x44),
        #    '_unknow1': util.getInt(data, offGr+0x48),
        #    '_unknow2': util.getInt(data, offGr+0x4C),
        #    'rewards': [{
        #        'kind': util.getInt(data, util.getLong(data, offGr+0x50)+0x28*iR),
        #        'round': util.getSInt(data, util.getLong(data, offGr+0x50)+0x28*iR+0x04),
        #        'army': util.getSInt(data, util.getLong(data, offGr+0x50)+0x28*iR+0x08),
        #        'rank_lo': util.getSInt(data, util.getLong(data, offGr+0x50)+0x28*iR+0x0C),
        #        'rank_hi': util.getSInt(data, util.getLong(data, offGr+0x50)+0x28*iR+0x10),
        #        'payload': util.getInt(data, util.getLong(data, offGr+0x50)+0x28*iR+0x18),
        #        'reward': util.getReward(data, util.getLong(data, offGr+0x50)+0x28*iR+0x20, util.getInt(data, util.getLong(data, offGr+0x50)+0x28*iR+0x18)),
        #    } for iR in range(util.getInt(data, offGr+0x40))],#3 + 8(nbArmy) * 8(nbReward) * 3(nbRound)
        #    'flags_multiplier': [{
        #        'flags': util.getInt(data, util.getLong(data, offGr+0x58)+0x08*i),
        #        'multiplier': util.getInt(data, util.getLong(data, offGr+0x58)+0x08*i+0x04),
        #    } for i in range(util.getInt(data, offGr+0x44))],
        #}]
        result += [{
            'id_tag': getString(data, offGr+0x00),
            'units': [getString(data, offGr+0x08+0x08*i) for i in range(8)],
            'reward_count': util.getInt(data, offGr+0x48),
            'flag_multiplier_count': util.getInt(data, offGr+0x4C),
            '_unknow1': util.getInt(data, offGr+0x50),
            '_unknow2': util.getInt(data, offGr+0x54),
            '_unknow3': util.getInt(data, offGr+0x58),
            '_unknow4': util.getInt(data, offGr+0x5C),
            'event_avail': util.getAvail(data, offGr+0x60),
            'rounds_avail': [util.getAvail(data, offGr+0x88+0x28*i) for i in range(3)],
            #unknow 0x10
            'rewards': [{
                'kind': util.getInt(data, util.getLong(data, offGr+0x110)+0x28*iR),
                'round': util.getSInt(data, util.getLong(data, offGr+0x110)+0x28*iR+0x04),
                'army': util.getSInt(data, util.getLong(data, offGr+0x110)+0x28*iR+0x08),
                'rank_lo': util.getSInt(data, util.getLong(data, offGr+0x110)+0x28*iR+0x0C),
                'rank_hi': util.getSInt(data, util.getLong(data, offGr+0x110)+0x28*iR+0x10),
                'payload': util.getInt(data, util.getLong(data, offGr+0X110)+0x28*iR+0x18),
                'reward': util.getReward(data, util.getLong(data, offGr+0X110)+0x28*iR+0x20, util.getInt(data, util.getLong(data, offGr+0X110)+0x28*iR+0x18)),
            } for iR in range(util.getInt(data, offGr+0x48))],
            'flags_multiplier': [{
                'flags': util.getInt(data, util.getLong(data, offGr+0x118)+0x08*i),
                'multiplier': util.getInt(data, util.getLong(data, offGr+0x118)+0x08*i+0x04),
            } for i in range(util.getInt(data, offGr+0x4C))],
        }]
    return result

def reverseVotingGauntlet():
    tag = "04_spring01"
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Tournament/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseTournament(data[0x20:])


from sys import argv

if __name__ == "__main__":
    s = reverseVotingGauntlet()
    if s:
        print(json.dumps(s, indent=2, ensure_ascii=False))