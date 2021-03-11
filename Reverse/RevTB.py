#!/usr/bin/env python3

import json
from os.path import isfile
from datetime import datetime

import REutil as util

def parseTapActionStage(data, off):
    return {
        "id_tag": util.getString(data, off+0x00),
        "stage_id": util.getString(data, off+0x08),
        "bgm": util.getString(data, off+0x10),
        "bgm_id": util.getString(data, off+0x18),
        "bgm_origin": util.getString(data, off+0x20),
        "boss_id": util.getString(data, off+0x28),
        "boss_anim": util.getString(data, off+0x30),
        #next_stage
        "boss_stage": [],
        "rewards": util.getReward(data, off+0x48, util.getInt(data, off+0x50, 0x34bc2a3b)),
        "payload_size": util.getInt(data, off+0x50, 0x34bc2a3b),
        "BPM": util.getInt(data, off+0x54, 0xdb931ce5),
        "_unknow6": hex(util.getShort(data, off+0x58)),
        "begining_floor": util.getShort(data, off+0x5a, 0x3174),
        "life": util.getShort(data, off+0x5c, 0xe792),
        "score": util.getInt(data, off+0x5e, 0x75d3d502),
        "difficulty": util.getByte(data, off+0x62, 0xd6),
        "_id": util.getShort(data, off+0x63, 0xf582),
        "_no_foe_": util.getBool(data, off+0x65, 0xca),
        "show_spa": util.getBool(data, off+0x66, 0xe9),
        "extra": util.getBool(data, off+0x67, 0xb1),
        "start": datetime.utcfromtimestamp(util.getLong(data, off+0x68, 0x3e5fff5dc44147fa)).isoformat() + "Z",
        "finish": datetime.utcfromtimestamp(util.getLong(data, off+0x70, 0x538a348f7440e43b)).isoformat() + "Z",
    }, util.getLong(data, off+0x38), util.getLong(data, off+0x40)

def parseTapAction(data):
    #9E 1C 93 DB  54 42 75 31 91 E7 16 D5  D3 75 D7 82 F5 CA E9 B1  #Hard Floor 1-5
    #9E 1C 93 DB  54 42 72 31 91 E7 23 D5  D3 75 D7 83 F5 CA E9 B1  #Hard Floor 5-10
    #9E 1C 93 DB  54 42 7F 31 91 E7 2B D5  D3 75 D7 80 F5 CA E9 B1  #Hard Floor 10-15
    #9E 1C 93 DB  54 42 64 31 96 E7 31 D5  D3 75 D7 81 F5 CA E9 B1  #Hard Floor 15-20
    #67 1C 93 DB  54 42 60 31 96 E7 11 D5  D3 75 D7 86 F5 CA E9 B1  #Hard Boss Floor 20

    #9E 1C 93 DB  54 42 75 31 91 E7 05 D5  D3 75 D6 82 F5 CA E9 B1  #Normal Floor 1-5
    #9E 1C 93 DB  54 42 72 31 91 E7 0E D5  D3 75 D6 83 F5 CA E9 B1  #Normal Floor 5-10
    #9E 1C 93 DB  54 42 7F 31 91 E7 12 D5  D3 75 D6 80 F5 CA E9 B1  #Normal Floor 10-15
    #9E 1C 93 DB  54 42 64 31 96 E7 17 D5  D3 75 D6 81 F5 CA E9 B1  #Normal Floot 15-20
    #67 1C 93 DB  54 42 60 31 96 E7 08 D5  D3 75 D6 86 F5 CA E9 B1  #Normal Boss Floor 20
    #63 1C 93 DB  54 42 5D 31 97 E7 0C D5  D3 75 D6 8A F5 CA E9 B1  #Normal Floor 45-50
    result = {
        "id_tag": util.getString(data, 0x00),
        "name": util.getString(data, 0x08),
        "scenario_name": util.getString(data, 0x10),
        "backdrop": util.getString(data, 0x18),
        "bgm_spa": util.getString(data, 0x20),
        "_unknow": util.getString(data, 0x28),
        "_unknow2": util.getString(data, 0x30),
        "desc_spa_id": util.getString(data, 0x38),
        "stages": [[], []],
        "extras": [[], []],
        "foes": [{
            "id_tag": util.getString(data, util.getLong(data, 0x50)+i*0x10+0x00),
            "_unknow1": hex(util.getByte(data, util.getLong(data, 0x50)+i*0x10+0x08, 0xb7)),
            "movetype": util.getByte(data, util.getLong(data, 0x50)+i*0x10+0x09, 0xd7),
            "_unknow2": hex(util.getShort(data, util.getLong(data, 0x50)+i*0x10+0x0a)),
            "_unknow3": hex(util.getInt(data, util.getLong(data, 0x50)+i*0x10+0x0c)),
            #"_unknow4": hex(util.getShort(data, util.getLong(data, 0x50)+i*0x10+0x0e)),
        } for i in range(util.getShort(data, 0x5E, 0x02B7))],
        #"level_off": util.getLong(data, 0x40),
        #"extra_off": util.getLong(data, 0x48),
        #"foe_off": util.getLong(data, 0x50),
        #"level_size": util.getByte(data, 0x58, 0x09),
        #"extra_size": util.getByte(data, 0x59, 0x1b),
        #"_unknow3": hex(util.getInt(data, 0x5A)),
        #"foe_size": util.getShort(data, 0x5E, 0x02B7),
        "start": datetime.utcfromtimestamp(util.getLong(data, 0x60, 0x71FF2C1E8B6EF875)).isoformat() + "Z",
        "finish": datetime.utcfromtimestamp(util.getLong(data, 0x68, 0x126029ADCA1E3937)).isoformat() + "Z",
        "encore": util.getBool(data, 0x70, 0x9a)
    }
    stageOff = util.getLong(data, 0x40)
    while stageOff and util.getByte(data, 0x58, 0x09) != 0:
        stage, stageOff, bossOff = parseTapActionStage(data, stageOff)
        result["stages"][0] += [stage]
        while bossOff:
            stage, other, bossOff = parseTapActionStage(data, bossOff)
            result["stages"][0][-1]["boss_stage"] += [stage]
            if other:
                print("next_stage value on a boss stage", file=stderr)
    stageOff = util.getLong(data, 0x40) + 0x78*util.getByte(data, 0x58, 0x09)
    while stageOff and util.getByte(data, 0x58, 0x09) != 0:
        stage, stageOff, bossOff = parseTapActionStage(data, stageOff)
        result["stages"][1] += [stage]
        while bossOff:
            stage, other, bossOff = parseTapActionStage(data, bossOff)
            result["stages"][1][-1]["boss_stage"] += [stage]
            if other:
                print("next_stage value on a boss stage", file=stderr)
    stageOff = util.getLong(data, 0x48)
    while stageOff and util.getByte(data, 0x59, 0x1b) != 0:
        stage, stageOff, bossOff = parseTapActionStage(data, stageOff)
        result["extras"][0] += [stage]
        while bossOff:
            stage, other, bossOff = parseTapActionStage(data, bossOff)
            result["extras"][0][-1]["boss_stage"] += [stage]
            if other:
                print("next_stage value on a boss stage", file=stderr)
    stageOff = util.getLong(data, 0x48) + 0x78*util.getByte(data, 0x59, 0x1b)
    while stageOff and util.getByte(data, 0x59, 0x1b) != 0:
        stage, stageOff, bossOff = parseTapActionStage(data, stageOff)
        result["extras"][1] += [stage]
        while bossOff:
            stage, other, bossOff = parseTapActionStage(data, bossOff)
            result["extras"][1][-1]["boss_stage"] += [stage]
            if other:
                print("next_stage value on a boss stage", file=stderr)
    #json.dump(data, open('a', 'w'), indent=2)
    return result

def reverseTapBattle(nb: int, revival: bool=False):
    fpath = util.BINLZ_ASSETS_DIR_PATH + f"/Common/TapAction/TapBattleData/TDID_{id:04}{'_01' if revival else ''}.bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseTapAction(data[0x20:])


import re
from sys import argv
if __name__ == "__main__":
    for arg in argv[1:]:
        if re.match(r"^\d+\+$", arg):
            s = reverseTapBattle(int(arg[:-1]), True)
        else:
            s = reverseTapBattle(int(arg))
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))