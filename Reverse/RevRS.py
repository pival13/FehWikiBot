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
            "pre_register_avail": util.getAvail(data, offGr+0x08),
            "event_avail": util.getAvail(data, offGr+0x30),
            "battle_avail": [util.getAvail(data, offGr+0x58+0x28*i) for i in range(3)],
            # 53 40 FA 58 EB 34 FA 58  63 1B FA 58 9D 1B DB 9F
            # 33 47 ED 10 8D B9 0D 6B  B0 BA 80 12 F5 49 68 CA
            "_unknow1": hex(util.getLong(data, offGr+0xD0)),
            "_unknow2": hex(util.getLong(data, offGr+0xD8)),
            "_unknow3": hex(util.getLong(data, offGr+0xE0)),
            "_unknow4": hex(util.getLong(data, offGr+0xE8)),
            # nbTurn/diff, maxScore/diff, boost/diff, boostIncr/diff
            # 78 B2 63 5F  D4 B2 63 5F  8C B3 63 5F
            # 48 43 CE E3  48 43 CE E3  48 43 CE E3
            # 0C CB 47 88  12 CB 47 88  2E CB 47 88
            "_unknow5": [hex(util.getInt(data, offGr+0xF0+i*0x04)) for i in range(3)],
            "_unknow6": [hex(util.getInt(data, offGr+0xFC+i*0x04)) for i in range(3)],
            "_unknow7": [hex(util.getInt(data, offGr+0x108+i*0x04)) for i in range(3)],
            # FB D8 04 B2
            "_unknow8": hex(util.getInt(data, offGr+0x114)),
            "_unknow9": [{
                # 77 7D 22 27 B0 D3 D4 A7  72 0B 5A 59 F4 0B F2 6C
                # 77 7D 22 27 B0 D3 D4 A7  72 0B 5A 59 F4 0B F2 6C
                # 77 7D 22 27 B0 D3 D4 A7  72 0B 5A 59 F2 0B F2 6C
                #0x10
                # nbReinforcement/diff
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
            "unit_data_common": [{
                "rarity": util.getInt(data, offGr+0x178+i*0x28+0x00, 0x5B24BB5A),
                "level": util.getInt(data, offGr+0x178+i*0x28+0x04, 0x60DFF76B),
                "stats": util.getStat(data, offGr+0x178+i*0x28+0x08),
                "special": util.getString(data, offGr+0x178+i*0x28+0x18),
                "seal": util.getString(data, offGr+0x178+i*0x28+0x20),
            } for i in range(3)],
            # 29 39 F9 94 08 3E C3 06  5B BA 3D 72 08 3F 4F 5C
            "_unknow11": hex(util.getLong(data, offGr+0x1F0)),
            "_unknow12": hex(util.getLong(data, offGr+0x1F8)),
            "units": [[{
                "id_tag": util.getString(data, util.getLong(data, offGr+0x200)+0x00+0x30*iUni+0x120*iDiff),
                "stat_modifier": {
                    "atk": util.getShort(data, util.getLong(data, offGr+0x200)+0x08+0x30*iUni+0x120*iDiff, 0x860F),
                    "spd": util.getShort(data, util.getLong(data, offGr+0x200)+0x0a+0x30*iUni+0x120*iDiff, 0xD5A9),
                    "def": util.getShort(data, util.getLong(data, offGr+0x200)+0x0c+0x30*iUni+0x120*iDiff, 0x79B7),
                    "res": util.getShort(data, util.getLong(data, offGr+0x200)+0x0e+0x30*iUni+0x120*iDiff, 0x4E34),
                },
                "assist": util.getString(data, util.getLong(data, offGr+0x200)+0x10+0x30*iUni+0x120*iDiff),
                "a": util.getString(data, util.getLong(data, offGr+0x200)+0x18+0x30*iUni+0x120*iDiff),
                "b": util.getString(data, util.getLong(data, offGr+0x200)+0x20+0x30*iUni+0x120*iDiff),
                "c": util.getString(data, util.getLong(data, offGr+0x200)+0x28+0x30*iUni+0x120*iDiff),
            } for iUni in range(6)] for iDiff in range(3)],
            "_unknow13": [{
                # 89 75 8C 76 2F B0 BB 55  C9 29 5B EB A0 5A 90 7A  13 51 57 64 1A 29 59 05
                # 8E 75 8C 76 3B B0 BB 55  32 D6 5B EB A0 5A 90 7A  13 51 57 64 1A 29 59 05
                # 8F 75 8C 76 0D B0 BB 55  32 D6 5B EB A0 5A 90 7A  13 51 57 64 1A 29 59 05
                #0x18,
            } for i in range(3)],
        }]

    # modG  20 20 20 20  20 20 20 20  20 20 20 20  20 20 20 20
    # base3  8  5  8  4   8  4  5  5   9  5  7  6  10  3  9  6
    # grow  60 40 60 45  55 40 50 55  70 35 60 55  60 30 70 70
    # mod    3  4  0  0   3  3  0  0   0  0  0  0   0  0  0  0
    #       30 28 27 24  29 27 25 26  28 24 26 26  27 23 28 27

    #  2 25 -> 0 1 2
    #  2 30 -> 0 2 3
    #  2 35 -> 1 2 3
    #  3 30 -> 1 2 3
    #  3 35 -> 1 2 3
    #  3 40 -> 1 3 4
    #  3 50 -> 1 3 5
    #  4 30 -> 1 2 3
    #  4 35 -> 1 2 4
    #  4 40 -> 1 3 4
    #  4 45 -> 1 3 4
    #  4 50 -> 1 3 5
    #  4 55 -> 1 4 5
    #  5 30 -> 1 2 3
    #  5 35 -> 1 3 4
    #  5 40 -> 1 3 4
    #  5 45 -> 1 3 5
    #  5 50 -> 1 4 5
    #  5 55 -> 1 4 6
    #  5 60 -> 2 4 6
    #  6 50 -> 2 4 5
    #  6 55 -> 2 4 6
    #  6 60 -> 2 4 6
    #  6 65 -> 2 5 7
    #  6 70 -> 2 5 7
    #  7 50 -> 2 4 6
    #  7 55 -> 2 4 6
    #  7 60 -> 2 5 6
    #  7 65 -> 2 5 7
    #  7 70 -> 2 5 7
    #  7 75 -> 2 6 8
    #  8 50 -> 2 4 6
    #  8 55 -> 2 5 6
    #  8 60 -> 2 5 7
    #  8 65 -> 2 5 7
    #  9 65 -> 2 6 7
    #  9 70 -> 3 6 8
    # 10 60 -> 3 5 7
    # 10 65 -> 3 6 7
    # 10 70 -> 3 6 8

    #  3 30 -> 1 2 3
    #  4 30 -> 1 2 3
    #  5 30 -> 1 2 3
    #  3 35 -> 1 2 3
    #  5 35 -> 1 3 4
    #  4 40 -> 1 3 4
    #  5 40 -> 1 3 4
    #  4 45 -> 1 3 4
    #  5 45 -> 1 3 5
    #  4 50 -> 1 3 5
    #  5 50 -> 1 4 5
    #  6 50 -> 2 4 5
    #  7 50 -> 2 4 6
    #  5 55 -> 1 4 6
    #  6 55 -> 2 4 6
    #  7 55 -> 2 4 6
    #  8 55 -> 2 5 6
    #  5 60 -> 2 4 6
    #  6 60 -> 2 4 6
    #  7 60 -> 2 5 6
    #  8 60 -> 2 5 7
    # 10 60 -> 3 5 7
    #  6 65 -> 2 5 7
    #  7 65 -> 2 5 7
    #  6 70 -> 2 5 7
    #  9 70 -> 3 6 8

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