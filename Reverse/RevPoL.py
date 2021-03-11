#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseBoardGame(data):#TODO
    result = []
    for iGr in range(util.getLong(data, 0x08, 0x8C04448B9C6192D6)):
        offGr = util.getLong(data, 0x00)+iGr*0x90
        nbRound = util.getByte(data, offGr+0x78, 0xEF)
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "event_avail": util.getAvail(data, offGr+0x08),
            "round_avails": [util.getAvail(data, util.getLong(data, offGr+0x30)+0x28*i) for i in range(nbRound)],
            "rounds": [{
                "id": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x38)+0x08*i)),
                "_unknow1": util.getLong(data, util.getLong(data, util.getLong(data, offGr+0x38)+0x08*i)+0x08, 0xA384B52D),
                "weapons": bin(util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x38)+0x08*i)+0x10, 0x8175f760)),
                "weaponsShort": bin(util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x38)+0x08*i)+0x14, 0xFA3F)),
                "_unknow2": util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x38)+0x08*i)+0x16, 0x130C),
            } for i in range(nbRound)],
            "_unknow1": {
                #C8 F6 B3 00 00 00 00 00 C9 ED B2 00 00 00 00 00 CE E0 B5 00 00 00 00 00 CF E7 B4 00 00 00 00 00 CC DA B4 00 00 00 00 00 CD D1 B4 00 00 00 00 00 C2 D4 B4 00 00 00 00 00
                #DB D4 D9 1C 55 F9 00 00 DE 2B B0 E3 5F F8 00 00 B2 2B 6D E3 4A FF 00 00
                #52 CC 00 00 00 00 00 00 AD CF 00 00 00 00 00 00 AC C9 00 00 00 00 00 00

                #CC52 110001010010
                #CFAD 111110101101
                #C9AC 100110101100
                "_unknow1": {},
                "_unknow2": [hex(util.getLong(data, util.getLong(data, util.getLong(data, offGr+0x40)+0x08)+0x08*i)) for i in range(nbRound)],
                "_unknow3": {},
                "_unknow4": [(util.getLong(data, util.getLong(data, util.getLong(data, offGr+0x40)+0x18)+0x08*i, 0xCD00)) for i in range(nbRound)],
                #A6 34 6B 18 3E B4 57 33 C9 5B 2F E1 18 3C 8B 58 3B 9C 30 1E 2F EC 00 00
            },#"12F8->13B0" "CC8->D80"
            "bonusDefinition": [{
                "_unknow1": util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x10*i, 0xE5),
                "_unknow2": util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x10*i+0x01, 0xF7),
                "_unknow3": util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x10*i+0x02, 0x18),
                "_unknow4": util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x10*i+0x03, 0x6E),
                "_unknow5": util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x10*i+0x04, 0x75),
                "_unknow6": util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x10*i+0x05, 0x1C),
                "_unknow7": util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x10*i+0x06, 0x60),
                "weapons": bin(util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x10*i+0x08, 0x513D6037)),
            } for i in range(util.getInt(data, util.getLong(data, offGr+0x48)+0x08, 0xC87BBD8B))],
            "pveDefinition": [{
                "units": [util.getString(data, util.getLong(data, util.getLong(data, util.getLong(data, offGr+0x50))+0x10*i)+0x08*j) for j in range(2)],
                "series": bin(util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x50))+0x10*i+0x08, 0x4F8B)),
                "unknow1": hex(util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x50))+0x10*i+0x0A, 0x2AE846)),
            } for i in range(util.getInt(data, util.getLong(data, offGr+0x50)+0x08, 0xE237DACF))],
            "_unknow4": [{
                #15C0->1710
                # AF 4B F7 AA 56 F2 B5 51 FD B0 5C F8 BB 27 C3 86 22 CE 81 2D C9 8C 28 D4 97 33 DF 9D 39 A5
                # 22 27 28 2D 33 39 4B 51 56 5C 81 86 8C 97 9D A5 AA AF B0 B5 BB C3 CE C9 D4 DF F2 F7 F8 FD

                # AF 01 50 36 48 F0 2A AE
                # 4B 00 50 36 48 F0 2E 85
                # F7 00 50 36 48 F0 D2 D3
                # 69 00 00 00 00 00 00 00

                # AA 01 50 36 48 F0 2A AE
                # 56 00 50 36 48 F0 2E 85
                # F2 00 50 36 48 F0 D2 D3
                # 69 00 00 00 00 00 00 00

                # B5 01 50 36 48 F0 2A AE
                # 51 00 50 36 48 F0 2E 85
                # FD 00 50 36 48 F0 D2 D3
                # 69 00 00 00 00 00 00 00


                # B0 01 50 36 48 F0 2A AE
                # 5C 00 50 36 48 F0 2E 85
                # F8 00 50 36 48 F0 D2 D3
                # 6A 00 00 00 00 00 00 00

                # BB 01 50 36 48 F0 2A AE
                # 27 00 50 36 48 F0 2E 85
                # C3 00 50 36 48 F0 D2 D3
                # 6A 00 00 00 00 00 00 00

                # 86 01 50 36 48 F0 2A AE
                # 22 00 50 36 48 F0 2E 85
                # CE 00 50 36 48 F0 D2 D3
                # 6A 00 00 00 00 00 00 00



                # 81 01 50 36 48 F0 2A 85
                # 2D 00 50 36 48 F0 2E FC
                # C9 00 50 36 48 F0 D2 D3
                # 6B 00 00 00 00 00 00 00

                # 8C 01 50 36 48 F0 2A 85
                # 28 00 50 36 48 F0 2E FC
                # D4 00 50 36 48 F0 D2 D3
                # 6B 00 00 00 00 00 00 00


                # 97 01 50 36 48 F0 2A 85
                # 33 00 50 36 48 F0 2E FC
                # DF 00 50 36 48 F0 D2 D3
                # 6C 00 00 00 00 00 00 00

                # 9D 01 50 36 48 F0 2A 85
                # 39 00 50 36 48 F0 2E FC
                # A5 00 50 36 48 F0 D2 D3
                # 6C 00 00 00 00 00 00 00


                #util.getLong(data, util.getLong(data, offGr+0x58))+0x20*i
            } for i in range(util.getInt(data, util.getLong(data, offGr+0x58)+0x08, 0x84054BEC))],
            "score_rewards": [{
                "reward": util.getReward(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x28*i, util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x28*i+0x08, 0xcc34b2c1)),
                "payload": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x28*i+0x08, 0xcc34b2c1),
                "score": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x28*i+0x0C, 0x610A90e7),
                "reward_id": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x28*i+0x10),
                "reward_id2": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x28*i+0x18),
                "reward_id3": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x60))+0x28*i+0x20),
            } for i in range(util.getInt(data, util.getLong(data, offGr+0x60)+0x08, 0xdff84de4))],
            "tier_rewards": [{
                "reward": util.getReward(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i, util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i+0x08, 0x4b8f8fe)),
                "payload": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i+0x08, 0x4b8f8fe),
                "tier": util.getByte(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i+0x0C, 0x39),
                "reward_id1": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i+0x10),
                "reward_id2": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i+0x18),
                "reward_id3": util.getString(data, util.getLong(data, util.getLong(data, offGr+0x68))+0x28*i+0x20)
            } for i in range(util.getInt(data, util.getLong(data, offGr+0x68)+0x08, 0xEF13BB46))],
            "tiers": [{
                "moveCondition": [{
                    "newTier": util.getSShort(data, util.getLong(data, util.getLong(data, offGr+0x70))+0x28*+i+0x08*j, 0xE324),
                    "percentTo": util.getSShort(data, util.getLong(data, util.getLong(data, offGr+0x70))+0x28*+i+0x08*j+0x02, 0x6DA5),
                    "percentFrom": util.getSShort(data, util.getLong(data, util.getLong(data, offGr+0x70))+0x28*+i+0x08*j+0x04, 0x5C75),
                } for j in range(4)],
                "tier": util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x70))+0x28*+i+0x20, 0xC476),
            } for i in range(util.getLong(data, util.getLong(data, offGr+0x70)+0x08, 0x58902F22))],
            "nbRound": util.getByte(data, offGr+0x78, 0xEF),
            "": util.getByte(data, offGr+0x79),#F9
        }]
    return result

def reversePawnsOfLoki(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/SRPG/BoardGame/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseBoardGame(data[0x20:])


from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reversePawnsOfLoki(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))