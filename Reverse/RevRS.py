#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseShadow(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x53feef9d361c5771)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00)+0x250*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "pre_registr_avail": util.getAvail(data, offGr+0x08),
            "event_avail": util.getAvail(data, offGr+0x30),
            "battle_avail": [util.getAvail(data, offGr+0x58+0x28*i) for i in range(3)],
            "_unknow1": hex(util.getLong(data, offGr+0xD0)),
            "_unknow2": hex(util.getLong(data, offGr+0xD8)),
            "_unknow3": hex(util.getLong(data, offGr+0xE0)),
            "_unknow4": hex(util.getLong(data, offGr+0xE8)),
            "_unknow5": [hex(util.getInt(data, offGr+0xF0+i*0x04)) for i in range(3)],
            "_unknow6": [hex(util.getInt(data, offGr+0xFC+i*0x04)) for i in range(3)],
            "_unknow7": [hex(util.getInt(data, offGr+0x108+i*0x04)) for i in range(3)],
            "_unknow8": hex(util.getInt(data, offGr+0x114)),
            "_unknow9": [{
                #0x10
            } for i in range(3)],
            "rewards": [{
                "type": util.getInt(data, util.getLong(data, offGr+0x150)+0x40*i+0x00, 0x98b554be),
                "battle": util.getInt(data, util.getLong(data, offGr+0x150)+0x40*i+0x04, 0xe43e1b61),
                "tag_orb": util.getString(data, util.getLong(data, offGr+0x150)+0x40*i+0x08),
                "tag_item": util.getString(data, util.getLong(data, offGr+0x150)+0x40*i+0x10),
                "tag_havoc_axe": util.getString(data, util.getLong(data, offGr+0x150)+0x40*i+0x18),
                "score_rank_hi": util.getLong(data, util.getLong(data, offGr+0x150)+0x40*i+0x20, 0xc835ea30ba958b17),
                "score_rank_lo": util.getSLong(data, util.getLong(data, offGr+0x150)+0x40*i+0x28, 0xbee2934ad6f7f636),
                "payload": util.getLong(data, util.getLong(data, offGr+0x150)+0x40*i+0x30, 0xfd59a22c415d8a52),
                "reward": util.getReward(data, util.getLong(data, offGr+0x150)+0x40*i+0x38, util.getLong(data, util.getLong(data, offGr+0x150)+0x40*i+0x30, 0xfd59a22c415d8a52)),
            } for i in range(util.getLong(data, offGr+0x148, 0xe0d8e36a09cf32d2))],
            "defeat_rewards": [{
                "proba": util.getInt(data, util.getLong(data, offGr+0x160)+0x10*i+0x00, 0xB4647120),
                "reward": util.getReward(data, util.getLong(data, offGr+0x160)+0x10*i+0x08, util.getInt(data, util.getLong(data, offGr+0x160)+0x10*i+0x04, 0xe4a3284f))
            } for i in range(util.getLong(data, offGr+0x158, 0xc41e80960fcf107c))],
            "rokkr_damage_rewards": [{
                "id": util.getInt(data, util.getLong(data, offGr+0x170)+0x18*i+0x00, 0xe18f41e3),
                "score": util.getInt(data, util.getLong(data, offGr+0x170)+0x18*i+0x04, 0x2c2e4996),
                "battle": util.getInt(data, util.getLong(data, offGr+0x170)+0x18*i+0x08, 0x70301efe),
                "payload": util.getInt(data, util.getLong(data, offGr+0x170)+0x18*i+0x0c, 0x6d1bf3e5),
                "reward": util.getReward(data, util.getLong(data, offGr+0x170)+0x18*i+0x10, util.getInt(data, util.getLong(data, offGr+0x170)+0x18*i+0x0c, 0x6d1bf3e5))
            } for i in range(util.getLong(data, offGr+0x168, 0x112adfc44ee716bc))],
            "_unknow10": [{
                "": "",#0x18
                "special": util.getString(data, offGr+0x178+i*0x28+0x18),
                "seal": util.getString(data, offGr+0x178+i*0x28+0x20),
            } for i in range(3)],
            "_unknow11": hex(util.getLong(data, offGr+0x1F0)),
            "_unknow12": hex(util.getLong(data, offGr+0x1F8)),
            "units": [[{
                "id_tag": util.getString(data, util.getLong(data, offGr+0x200)+0x30*iUni+0x120*iDiff),
                "assist": util.getString(data, util.getLong(data, offGr+0x200)+0x10+0x30*iUni+0x120*iDiff),
                "a": util.getString(data, util.getLong(data, offGr+0x200)+0x18+0x30*iUni+0x120*iDiff),
                "b": util.getString(data, util.getLong(data, offGr+0x200)+0x20+0x30*iUni+0x120*iDiff),
                "c": util.getString(data, util.getLong(data, offGr+0x200)+0x28+0x30*iUni+0x120*iDiff),
            } for iUni in range(6)] for iDiff in range(3)],
            "_unknow13": [{
                #0x18,
            } for i in range(3)],
        }]
        #for i in range(2):
        #    off = util.getLong(data, offGr+0x150)
        #    result[iGr]["a"] = {
        #        "a": hex(util.getLong(data, off+0x00+0x40*i)),
        #        "b": util.getString(data, off+0x08+0x40*i),
        #        #"c": hex(util.getLong(data, off+0x10)), # == 0
        #        "d": util.getString(data, off+0x18+0x40*i),
        #        "h": util.getReward(data, off+0x38+0x40*i, 72),
        #        "i": hex(util.getLong(data, off+0x40)),
        #        "j": hex(util.getLong(data, off+0x48)),
        #        "k": hex(util.getLong(data, off+0x50)),
        #    }
    return result

def reverseRokkrSieges(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Shadow/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseShadow(data[0x20:])


from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reverseRokkrSieges(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))