#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseField(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x1D90083CCADFBC58)
    for i in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x30*i
        result += [{
            "map_id": util.getString(data, offGr+0x00),
            "wall": {"kind": util.getString(data, util.getLong(data, offGr+0x08)), "filename": util.getString(data, util.getLong(data, offGr+0x08)+0x08, util.NONE_XORKEY)},
            "backdrop": {"kind": util.getString(data, util.getLong(data, offGr+0x10)), "filename": util.getString(data, util.getLong(data, offGr+0x10)+0x08, util.NONE_XORKEY)},
            "overlay": [{"kind": util.getString(data, util.getLong(data, offGr+0x18+0x08*i)), "filename": util.getString(data, util.getLong(data, offGr+0x18+0x08*i)+0x08, util.NONE_XORKEY)} for i in range(2)],
            "anim": util.getString(data, offGr+0x28, util.NONE_XORKEY),
        }]
    return result

def parseSRPGMap(data):
    result = {
        #unknow 0x04
        "highest_score": util.getInt(data, 0x04, 0xA9E250B1),
        "field": {
            "id": util.getString(data, util.getLong(data, 0x08)),
            "width": util.getInt(data, util.getLong(data, 0x08)+0x08, 0x6B7CD75F),
            "height": util.getInt(data, util.getLong(data, 0x08)+0x0C, 0x2BAA12D5),
            "base_terrain": util.getByte(data, util.getLong(data, 0x08)+0x10, 0x41),
            #padding 0x07
            "terrain": [[util.getByte(data, util.getLong(data, 0x08)+0x18+0x01*x+0x01*util.getInt(data, util.getLong(data, 0x08)+0x08, 0x6B7CD75F)*y, 0xA1)
                for x in range(util.getInt(data, util.getLong(data, 0x08)+0x08, 0x6B7CD75F))] for y in range(util.getInt(data, util.getLong(data, 0x08)+0x0C, 0x2BAA12D5))],
        },
        "player_pos": [{
            "x": util.getShort(data, util.getLong(data, 0x10)+0x08*i, 0xB332),
            "y": util.getShort(data, util.getLong(data, 0x10)+0x02+0x08*i, 0x28B2),
            #padding 0x04
        } for i in range(util.getInt(data, 0x20, 0x9D63C79A))],
        "units": [],#0x18
        "player_count": util.getInt(data, 0x20, 0x9D63C79A),
        "unit_count": util.getInt(data, 0x24, 0xAC6710EE),
        "turns_to_win": util.getByte(data, 0x28, 0xFD),
        "last_enemy_phase": util.getBool(data, 0x29, 0xC7),
        "turns_to_defend": util.getByte(data, 0x2A, 0xEC),
    }
    for iUnit in range(result["unit_count"]):
        off = util.getLong(data, 0x18)+0x78*iUnit
        result["units"] += [{
            "id_tag": util.getString(data, off+0x00),
            "skills": [util.getString(data, off+0x08+0x08*i) for i in range(7)],
            "accessory": util.getString(data, off+0x40),
            "pos": {
                "x": util.getShort(data, off+0x48, 0xB332),
                "y": util.getShort(data, off+0x4A, 0x28B2),
            },
            "rarity": util.getByte(data, off+0x4C, 0x61),
            "lv": util.getByte(data, off+0x4D, 0x2A),
            "cooldown_count": util.getSByte(data, off+0x4E, 0x1E),
            "max_cooldown_count": util.getSByte(data, off+0x4F, 0x9B),
            "stats": util.getStat(data, off+0x50),
            "start_turn": util.getSByte(data, off+0x60, 0xCF),
            "movement_group": util.getSByte(data, off+0x61, 0xF4),
            "movement_delay": util.getSByte(data, off+0x62, 0x95),
            "break_terrain": util.getBool(data, off+0x63, 0x71),
            "tether": util.getBool(data, off+0x64, 0xB8),
            "true_lv": util.getByte(data, off+0x65, 0x85),
            "is_enemy": util.getBool(data, off+0x66, 0xD0),
            #padding 0x01
            "spawn_check": util.getString(data, off+0x68),
            "spawn_count": util.getSByte(data, off+0x70, 0x0A),
            "spawn_turns": util.getSByte(data, off+0x71, 0x0A),
            "spawn_target_remain": util.getSByte(data, off+0x72, 0x2D),
            "spawn_target_kills": util.getSByte(data, off+0x73, 0x5B),
            #padding 0x04
        }]
    return result

def parseStage(data, off):
    return {
        'id_tag': util.getString(data, off),
        'base_id': util.getString(data, off+0x08),
        'prerequisites': [util.getString(data, util.getLong(data, off+0x10)+0x08*i) for i in range(util.getInt(data, off+0x18, 0x092DFD01))],
        'prereq_count': util.getInt(data, off+0x18, 0x092DFD01),
        #padding 0x04
        'honor_id': util.getString(data, off+0x20),
        'name_id': util.getString(data, off+0x28),
        '_unknown1': util.getString(data, off+0x30),
        'reward': util.getReward(data, off+0x38, util.getInt(data, off+0x40, 0x64645EE2)),
        'payload_size': util.getInt(data, off+0x40, 0x64645EE2),
        'origins': bin(util.getInt(data, off+0x44, 0x67080B02)) if util.getInt(data, off+0x44, 0x67080B02) != 0 else 0,
        'stamina': util.getShort(data, off+0x48, 0xBB22),
        '_unknown2': util.getShort(data, off+0x4A, 0x2335),
        'difficulty': util.getShort(data, off+0x4C, 0xC074),
        #'unknow': hex(util.getLong(data, off+0x4E)),
        'survives': util.getSShort(data, off+0x56, 0x4FCB),
        'no_lights_blessing': util.getShort(data, off+0x58, 0x3030),
        'turns_to_win': util.getShort(data, off+0x5A, 0xA743),
        'turns_to_defend': util.getShort(data, off+0x5C, 0x8091),
        'stars': util.getShort(data, off+0x5E, 0xCBB6),
        'lv': util.getShort(data, off+0x60, 0x14BA),
        'true_lv': util.getShort(data, off+0x62, 0xD953),
        'reinforcements': util.getShort(data, off+0x64, 0x6399),
        'last_enemy_phase': util.getShort(data, off+0x66, 0x6C4A),
        'max_refreshers': util.getSShort(data, off+0x68, 0x295B),
        'rd_level': util.getSShort(data, off+0x6A, 0x7C4E),
        #padding 0x04
        'enemy_weps': [util.getSByte(data, off+0x70+i*0x01, 0x97) for i in range(8)]
    }

def parseStageScenario(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x575328d11a57cb1D)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00)+0xB8*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "avail": util.getAvail(data, offGr+0x08),
            #unknow: 0x08
            #"sort_id": hex(util.getInt(data, offGr+0x30)),
            "sort_id": util.getInt(data, offGr+0x34, 0xb8884244),
            "is_paralogue": util.getByte(data, offGr+0x38, 0xB6),
            #"unknow": hex(util.getInt(data, offGr+0x39)),
            "book": util.getByte(data, offGr+0x3E, 0x29),
            #padding 0x01
            "maps": [],
        }]
        for iDiff in range(3):
            offDiff = offGr + 0x40 + 0x28*iDiff
            result[iGr]["maps"] += [{
                "prerequisites": [util.getString(data, util.getLong(data, offDiff+0x00)+0x08*i) for i in range(util.getInt(data, offDiff+0x08, 0x092DFD01))],
                "prereq_count": util.getInt(data, offDiff+0x08, 0x092DFD01),
                "scenarios": [parseStage(data, util.getLong(data, offDiff+0x10)+0x78*i) for i in range(util.getInt(data, offDiff+0x20, 0x2f416dff))],
                "flags": [util.getSByte(data, util.getLong(data,offDiff+0x18), 0x2E) for i in range(util.getInt(data, offDiff+0x20, 0x2f416dff))],
                "scenario_count": util.getInt(data, offDiff+0x20, 0x2f416dff),
                "is_paralogue": util.getBool(data, offDiff+0x24, 0xC4)
            }]
    return result

def parseStageEvent(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0xC84AFFA7BB739117)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00)+0x68*iGr
        result += [{
            "id_tag": util.getString(data, offGr),
            "banner_id": util.getString(data, offGr+0x08),
            "rd_tag": util.getString(data, offGr+0x10),
            "rd_bonus": util.getString(data, offGr+0x18),
            "_unknown1": util.getString(data, offGr+0x20),
            "avail": util.getAvail(data, offGr+0x28),
            #"unknow": util.getLong(data, offGr+0x48),
            "sort_id1": util.getInt(data, offGr+0x50, 0xA2BDF0B7),
            "sort_id2": util.getInt(data, offGr+0x54, 0xFE6EF6B7),
            "scenarios": [],#util.getLong(data, offGr+0x58),
            "scenario_count": util.getInt(data, offGr+0x60, 0xFDBFB266),
            #"unknow": util.getByte(data, offGr+0x64))
            "rival_domains": util.getBool(data, offGr+0x65, 0x34)
        }]
        for iDiff in range(result[iGr]["scenario_count"]):
            offDiff = util.getLong(data, offGr+0x58)+0x78*iDiff
            result[iGr]["scenarios"] += [parseStage(data, offDiff)]
    return result

def parseStagePuzzle(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x07c8525a8f13c8558)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00)+0x48*iGr
        result += [{
            "id_tag": util.getString(data, offGr),
            "avail": util.getAvail(data, offGr+0x08),
            #padding 0x08
            "sort_id1": util.getInt(data, offGr+0x30, 0xBF35E827),
            "sort_id2": util.getInt(data, offGr+0x34, 0xf6336eb6),
            "difficulty": util.getInt(data, offGr+0x38, 0xf2103821),
            "scenario": parseStage(data, util.getLong(data, offGr+0x40)),
        }]
    return result
