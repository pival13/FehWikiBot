#!/usr/bin/env python3

from subprocess import Popen, PIPE, STDOUT
import json
from datetime import datetime
from math import ceil

import REutil as util

def parseMsg(data):
    numberElem = util.getLong(data, 0)
    result = []
    for i in range(numberElem):
        result += [{
            "key": util.xorString(data[util.getLong(data,i*16+8):], util.MSG_XORKEY),
            "value": util.xorString(data[util.getLong(data,i*16+16):], util.MSG_XORKEY)
        }]
    return result

def parseQuests(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x034E1E0B704C545B)
    for iGr in range(nbGroup):
        offGr = util.getLong(data,0)+0x50*iGr
        result += [{
            "id_tag": util.getString(data, offGr, util.ID_XORKEY),
            "title": util.getString(data, offGr+0x08, util.ID_XORKEY),
            "lists": [],
            "avail": util.getAvail(data, offGr+0x18),
            #"_unknow": util.getInt(data, offGr+0x38),
            "difficulties": util.getInt(data, offGr+0x40, 0xEEB24E54),
            "sort_id": util.getInt(data, offGr+0x44, 0x7A394CFC),
            "id_num": util.getInt(data, offGr+0x48, 0x7E92AD65),
            "feh_pass_only": util.getBool(data, offGr+0x4C),
        }]
        for iDiff in range(result[iGr]["difficulties"]):
            offDiff = util.getLong(data, offGr+0x10)+0x18*iDiff
            result[iGr]["lists"] += [{
                "difficulty": util.getString(data, offDiff, util.ID_XORKEY),
                "quests": [],
                "quest_count": util.getInt(data, offDiff+0x10, 0xE7B75ABF)
            }]
            for iQu in range(result[iGr]["lists"][iDiff]["quest_count"]):
                offQu = util.getLong(data, offDiff+0x08)+0x98*iQu
                result[iGr]["lists"][iDiff]["quests"] += [{
                    "quest_id": util.getString(data, offQu),
                    "common_id": util.getString(data, offQu+0x08),
                    "times": util.getInt(data, offQu+0x10, 0x2CF17A0D),
                    "trigger": util.getInt(data, offQu+0x14, 0xE33348DF),
                    "map_group": util.getString(data, offQu+0x18),
                    "game_mode": util.getInt(data, offQu+0x20, 0x1C0CC0BA),
                    "difficulty": util.getSInt(data, offQu+0x24, 0xF30584BB),
                    "max_allies": util.getSInt(data, offQu+0x28, 0xABD9C6CA),
                    "survive": util.getSInt(data, offQu+0x2C, 0xC2B141DE),
                    #"_unknow": util.getLong(data, offQu+0x30),
                    "game_mode2": util.getInt(data, offQu+0x38, 0x418E19A9),
                    # padding 0x08
                    "map_id": util.getString(data, offQu+0x40),
                    "unit_reqs": None,
                    "foe_reqs": None,
                    "reward": [],
                    "payload_size": util.getInt(data, offQu+0x90, 0x745AD662),
                }]
                result[iGr]["lists"][iDiff]["quests"][iQu]["reward"] = util.getReward(data, offQu+0x88, result[iGr]["lists"][iDiff]["quests"][iQu]["payload_size"])
                for key, off in (["unit_reqs",0x48],["foe_reqs",0x68]):
                    result[iGr]["lists"][iDiff]["quests"][iQu][key] = {
                        "hero_id": util.getString(data, offQu+off),
                        "color": util.getSInt(data, offQu+off+0x08, 0x4D72AD65),
                        "wep_type": util.getSInt(data, offQu+off+0x0C, 0x66435BAC),
                        "mov_type": util.getSInt(data, offQu+off+0x10, 0xE629436F),
                        "lv": util.getSShort(data, offQu+off+0x14, 0x4F3F),
                        #"_unknow": util.getShort(data, offQu+off+0x16),
                        "blessing": util.getShort(data, offQu+off+0x18, 0x7DB4),
                        "blessed": util.getShort(data, offQu+off+0x1A, 0x76B2),
                        #Padding 0x04
                    }
    return result

def parseAccessory(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x0de4c6f0ab07e0e13)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x20*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "sprite": util.getString(data, offGr+0x08),
        }]
    return result

def parseSkill(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x7fecc7074adee9ad)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x140*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "refine_base": util.getString(data, offGr+0x08),
            "name_id": util.getString(data, offGr+0x10),
            "desc_id": util.getString(data, offGr+0x18),
            "refine_id": util.getString(data, offGr+0x20),
            "beast_effect_id": util.getString(data, offGr+0x28),
            #"prerequisites": [util.getString(data, offGr+0x30+0x08*i) for i in range(2)],
            "next_skill": util.getString(data, offGr+0x40),
            "sprites": [util.getString(data, offGr+0x48+0x08*i, util.NONE_XORKEY) for i in range(4)],

        }]
    return result

def parsePerson(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0xde51ab793c3ab9e1)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00)+0x2A0*iGr
        result += [{
            "id_tag": util.getString(data, offGr),
            "roman": util.getString(data, offGr+0x08),
            "face_name": util.getString(data, offGr+0x10),
            "face_name2": util.getString(data, offGr+0x18),
            "legendary": {},
            "dragonflower": {},
            "timestamp": (datetime.utcfromtimestamp(util.getLong(data, offGr+0x30, 0xBDC1E742E9B6489B)).isoformat() + "Z") if util.getLong(data, offGr+0x30, 0xBDC1E742E9B6489B) != 0xFFFFFFFFFFFFFFFF else None,
            "id_num": util.getInt(data, offGr+0x38, 0x5F6E4E18),
            "sort_value": util.getInt(data, offGr+0x3C, 0x2A80349B),
            "origins": hex(util.getInt(data, offGr+0x40, 0xe664b808)),
            "weapon_type": util.getByte(data, offGr+0x44, 0x06),
            "tome_class": util.getByte(data, offGr+0x45, 0x35),
            "move_type": util.getByte(data, offGr+0x46, 0x2A),
            "series": util.getByte(data, offGr+0x47, 0x43),
            "regular_hero": util.getBool(data, offGr+0x48, 0xA1),
            "permanent_hero": util.getBool(data, offGr+0x49, 0xC7),
            "base_vector_id": util.getByte(data, offGr+0x4A, 0x3D),
            "refresher": util.getBool(data, offGr+0x4B, 0xFF),
            #"dragonflowers": util.getByte(data, offGr+0x4C, 0xE4),
            #"unknow": util.getByte(data, offGr+0x4D),
            #padding 0x02
            "base_stats": util.getStat(data, offGr+0x50),
            "growth_rates": util.getStat(data, offGr+0x60),
            "skills": [[util.getString(data, offGr+0x70+0x08*skill+0x08*14*rarity) for skill in range(14)] for rarity in range(5)]
        }]
        offLeg = util.getLong(data, offGr+0x20)
        result[iGr]["legendary"] = {
            "duo_skill_id": util.getString(data, offLeg+0x00),
            "bonus_effect": util.getStat(data, offLeg+0x08),
            "kind": util.getByte(data, offLeg+0x18, 0x21),
            "element": util.getByte(data, offLeg+0x19, 0x05),
            "bst": util.getByte(data, offLeg+0x1A, 0x0F),
            "pair_up": util.getBool(data, offLeg+0x1B, 0x80),
            #padding 0x04
        } if offLeg != 0 else None
    return result

def parseEnemy(data):
    result = []
    nbGroup = util.getLong(data,0x08, 0x62ca95119cc5345c)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00)+0x78*iGr
        result += [{
            "id_tag": util.getString(data, offGr),
            "roman": util.getString(data, offGr+0x08),
            "face_name": util.getString(data, offGr+0x10),
            "face_name2": util.getString(data, offGr+0x18),
            "top_weapon": util.getString(data, offGr+0x20),
            "unique_assist1": util.getString(data, offGr+0x28),
            "unique_assist2": util.getString(data, offGr+0x30),
            "_unique_special": util.getString(data, offGr+0x38),
            "timestamp": (datetime.utcfromtimestamp(util.getLong(data, offGr+0x40, 0xBDC1E742E9B6489B)).isoformat() + "Z") if util.getLong(data, offGr+0x40, 0xBDC1E742E9B6489B) != 0xFFFFFFFFFFFFFFFF else None,
            "id_num": util.getInt(data, offGr+0x48, 0x422f41d4),
            "weapon_type": util.getByte(data, offGr+0x4C, 0xe4),
            "tome_class": util.getByte(data, offGr+0x4D, 0x81),
            "move_type": util.getByte(data, offGr+0x4E, 0x0d),
            "random_allowed": util.getByte(data, offGr+0x4F, 0xc4),
            "isBoss": util.getByte(data, offGr+0x50, 0x6b),
            #padding 0x02
            "base_stats": util.getStat(data, offGr+0x58),
            "growth_rates": util.getStat(data, offGr+0x69),
        }]
    return result

def parseFriendDouble(data):#Allegiance Battle
    result = []
    nbGroup = util.getLong(data,0x08, 0xc0f4be0d2ed1f055)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0xB0 * iGr
        result += [{
            "season_id": util.getString(data, offGr+0x00),
            "unit_id": util.getString(data, offGr+0x08),
            "map_id": util.getString(data, offGr+0x10),
            "a": hex(util.getLong(data, offGr+0x18)),
            #"avail": util.getAvail(data, offGr+0x20),
            #unknow 0x01
            #padding 0x07
            "origins": hex(util.getLong(data, offGr+0x48)),
            "origins1": hex(util.getLong(data, offGr+0x50)),
            "origins2": hex(util.getLong(data, offGr+0x58)),
            "origins3": hex(util.getLong(data, offGr+0x60)),
            "origins4": hex(util.getLong(data, offGr+0x68)),
            "origins5": hex(util.getLong(data, offGr+0x70)),
            "origins6": hex(util.getLong(data, offGr+0x78)),
            "origins7": hex(util.getLong(data, offGr+0x80)),
            "origins8": hex(util.getLong(data, offGr+0x88)),#ptr
            "origins9": hex(util.getLong(data, util.getLong(data, offGr+0x90)+0x04)),
            #"score_rewards": hex(util.getLong(data, offGr+0x98)),#tbl cellsize:0x18
            #"rank_rewards": hex(util.getLong(data, offGr+0xA0)),#tbl cellsize:0x18
            "origins12": hex(util.getLong(data, offGr+0xA8)),
        }]
    return result#data f13f93d09e0f5af7

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

def parseStageBGM(data):
    result = []
    for i in range(int(len(data)/8)):
        result += [util.getString(data, i*0x08, util.BGM_XORKEY)]
    for i in range(int(len(data)/6)):
        result += [util.xorString(data[i*0x06:], util.NONE_XORKEY)]
    #nbGroup = util.getLong(data,0x08, 0x0)
    #for iGr in range(1):
    #    offGr = util.getLong(data, 0x00) + 0x00*iGr
    #    result += [hex(util.getLong(data, 0x08*i)) for i in range(int((len(data))/8))]
    return result

def parseLoginBonus(data):
    result = []
    result += [util.getString(data, 0x00, util.LOGIN_XORKEY)]
    
    result += [util.xorString(data[0x40:], util.NONE_XORKEY)]
    return result

def parseScenario(data, off):
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
                "scenarios": [parseScenario(data, util.getLong(data, offDiff+0x10)+0x78*i) for i in range(util.getInt(data, offDiff+0x20, 0x2f416dff))],
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
            result[iGr]["scenarios"] += [parseScenario(data, offDiff)]
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
            "scenario": parseScenario(data, util.getLong(data, offGr+0x40)),
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

def parseShadow(data):#Rokkr Siege
    result = []
    nbGroup = util.getLong(data,0x08, 0x53feef9d361c5771)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00)+0x250*iGr
        result += [{
            "id_tag": util.getString(data, offGr+0x00),
            "pre_registr_avail": util.getAvail(data, offGr+0x08),
            "event_avail": util.getAvail(data, offGr+0x30),
            "battle_avail": [util.getAvail(data, offGr+0x58+0x28*i) for i in range(3)],
            #"a": hex(util.getLong(data, offGr+0xD0)),
            "a": {},
            #"g": [
            #    util.getReward(data, util.getLong(data, util.getLong(data, offGr+0x150)), 72)
            #for i in range(1)],#ptr
            #"h": hex(util.getLong(data, offGr+0x158)),
            #"i": hex(util.getLong(data, offGr+0x160)),#ptr
            #"j": hex(util.getLong(data, offGr+0x168)),
            #"k": hex(util.getLong(data, offGr+0x170)),#ptr
            #"l": hex(util.getLong(data, offGr+0x178)),
            "units": [[{
                "id_tag": util.getString(data, util.getLong(data, offGr+0x200)+0x30*iUni+0x120*iDiff),
                "assist": util.getString(data, util.getLong(data, offGr+0x200)+0x10+0x30*iUni+0x120*iDiff),
                "a": util.getString(data, util.getLong(data, offGr+0x200)+0x18+0x30*iUni+0x120*iDiff),
                "b": util.getString(data, util.getLong(data, offGr+0x200)+0x20+0x30*iUni+0x120*iDiff),
                "c": util.getString(data, util.getLong(data, offGr+0x200)+0x28+0x30*iUni+0x120*iDiff),
            } for iUni in range(6)] for iDiff in range(3)],#ptr
        }]
        for i in range(2):
            off = util.getLong(data, offGr+0x150)
            result[iGr]["a"] = {
                "a": hex(util.getLong(data, off+0x00+0x40*i)),
                "b": util.getString(data, off+0x08+0x40*i),
                #"c": hex(util.getLong(data, off+0x10)), # == 0
                "d": util.getString(data, off+0x18+0x40*i),
                "h": util.getReward(data, off+0x38+0x40*i, 72),
                "i": hex(util.getLong(data, off+0x40)),
                "j": hex(util.getLong(data, off+0x48)),
                "k": hex(util.getLong(data, off+0x50)),
            }
    for i in range(int(len(data)/8)):
        if util.getLong(data, i*0x08) == 0x2008:
    #    if util.getLong(data, i*0x08) == 0x160707001B9AD871:# or util.getLong(data, i*0x08) == 0x26b40:
    #    #if util.getByte(data, i, 0x81) == ord('P') and util.getByte(data, i+1, 0x00) == ord('I'):
            print(hex(i*8))
    return result

def parseTrip(data):#Lost Lore
    result = []
    nbGroup = util.getLong(data,0x08, 0xBBC1712B8390494C)
    for i in range(nbGroup):
        result += [{
            'id_tag': util.getString(data, 0x10),
            'avail': util.getAvail(data, 0x18),
            #ptr util.getLong(data, 0x38)
        }]
    for i in range(int(len(data)/8)):
        result += [util.xorString(data[i*0x08:], util.ID_XORKEY)]
    #print(data[0x40:])
    #0x003BA9E383750000DFB27EAED671676C
    return result

def parseMjolnir(data):#Mjölnir's Strike
    result = []
    nbGroup = util.getLong(data,0x08)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x19A0*iGr
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
        """for i in range(5):
            off = util.getLong(data, offGr+0x38)+0x08*i
            result[iGr]["_unknow3"] += [{
                "a": util.getByte(data, off, 0x89),
            }]"""
    return result

def reverseFile(file: str):
    ruby = Popen(['ruby', 'REdecompress.rb', file], stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    s = ruby.stdout.readline().decode('utf8')
    if s[0] != '[':
        print(s, end="" if s[-1] == '\n' else '\n')
        return

    s = [int(v.strip()) for v in s[1:-1].split(sep=',')]
    #print([hex(v)[2:] for v in s])
    #exit(0)
    s = s[0x20:]
    if file.find("/Message/") != -1:
        return parseMsg(s)
    elif file.find("/Mission/") != -1:
        return parseQuests(s)
    elif file.find("/LoginBonus/") != -1:
        print(json.dumps(parseLoginBonus(s), indent=2, ensure_ascii=False))
        return
    elif file.find("/DressAccessory/Data/") != -1:
        print(json.dumps(parseAccessory(s), indent=2, ensure_ascii=False))
        return
    elif file.find("/SRPG/Skill/") != -1:
        print(json.dumps(parseSkill(s), indent=2, ensure_ascii=False))
        return
    elif file.find("/SRPG/Person/") != -1:
        return parsePerson(s)
    elif file.find("/SRPG/Enemy/") != -1:
        return parseEnemy(s)

    elif file.find("/FriendDouble/") != -1:
        #return parseFriendDouble(s)
        #open('a','wb').write(bytes(s))
        #print(json.dumps(s, indent=2, ensure_ascii=False))
        print("File under discovery")
        return

    elif file.find("/SRPG/Field/") != -1:
        return parseField(s)
    elif file.find("/SRPG/StageBgm/") != -1:
        print(json.dumps(parseStageBGM(s), indent=2, ensure_ascii=False))
        return
    elif file.find("/SRPG/StageScenario/") != -1:
        return parseStageScenario(s)
    elif file.find("/SRPG/StageEvent/") != -1:
        return parseStageEvent(s)
    elif file.find("/SRPG/StagePuzzle/") != -1:
        return parseStagePuzzle(s)
    elif file.find("/SRPGMap/") != -1:
        return parseSRPGMap(s)

    elif file.find("/Shadow/") != -1:
        print(json.dumps(parseShadow(s), indent=2, ensure_ascii=False))
        return
    elif file.find("/Trip/Terms/") != -1:
        print(json.dumps(parseTrip(s), indent=2, ensure_ascii=False))
        return
    elif file.find("/Mjolnir/BattleData/") != -1:
        return parseMjolnir(s)
    else:
        #print([util.xorString(data[i], util.NONE_XORKEY) for i in range(len(data))])
        print("Unknow kind of file")
        return


from sys import argv

if __name__ == "__main__":
    for i in range(1, len(argv)):
        s = reverseFile(argv[i])
        if s:
            try:
                newFile = "../feh-assets-json/files/" + argv[i][argv[i].find("assets"):].replace(".bin.lz", ".json")
                json.dump(s, open(newFile, 'x'), indent=2, ensure_ascii=False)
                print("File " + newFile + " create")
            except FileExistsError:
                print("File already exist")


# MS 3
#                                                 8A 1E F8 C8 52 B3 AA B7 DF 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 71 0E 7D FC C2 88 BB 2F 68 BB CB 5D FA FA FB EE E4 1D D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 4
#                                                 C8 1E F8 C8 52 B3 AA B7 DF 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 71 0E 7D FC C2 88 BB 2F 68 BB CB 5D FA FA FB EE E4 1F D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 5
#                                                 C8 1E F8 C8 52 B3 AA B7 DF 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 70 0E 7D FC C2 88 BB 2F 68 BB CB 5D FA FA FB EE E4 1C D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 12
# 17 F5 86 B4 93 B4 E3 27 1A BA C7 79 7D 2F 01 99 CE 1E F8 C8 52 B3 AA B7 DF 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 70 0E 7D FC C2 88 BB 2F 68 BB CB 5D FA FA FB EE E4 1F D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 13
# 97 25 A3 B4 93 B4 E3 27 9A CB DB 79 7D 2F 01 99 4B 1E F8 C8 52 B3 AA B7 DF 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 70 0E 7D FC C2 88 BB 2F 68 BB CB 5D FA FA FB EE E4 1C D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 14
# 97 E3 59 B4 93 B4 E3 27 9A B1 26 79 7D 2F 01 99 D2 1E F8 C8 52 B3 AA B7 DF 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 70 0E 7D FC C2 88 BB 2F 68 BB CB 5D FA FA FB EE E4 1E D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 15
# 17 DE 48 B4 93 B4 E3 27 1A 55 35 79 7D 2F 01 99 CA 1D F8 C8 52 B3 AA B7 C2 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 70 0E 7D FC C2 88 63 2F 68 BB CB 5D FA FA FB EE E4 1D D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 31
# 17 40 ED B5 93 B4 E3 27 1A 2F 92 78 7D 2F 01 99 CE 1E F8 C8 52 B3 AA B7 C2 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 70 0E 7D FC C2 88 63 2F 68 BB CB 5D FA FA FB EE E4 1D D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 32
# 97 66 99 B5 93 B4 E3 27 9A 0A E6 78 7D 2F 01 99 CA 1A F8 C8 52 B3 AA B7 C2 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 70 0E 7D FC C2 88 63 2F 68 BB CB 5D FA FA FB EE E4 1F D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 33
# 97 FA 92 B5 93 B4 E3 27 9A B6 EB 78 7D 2F 01 99 CA 0E F8 C8 52 B3 AA B7 C2 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 70 0E 7D FC C2 88 63 2F 68 BB CB 5D FA FA FB EE E4 1C D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 34
# 97 13 8B B5 93 B4 E3 27 9A 81 F3 78 7D 2F 01 99 CA 0E F8 C8 52 B3 AA B7 C2 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 70 0E 7D FC C2 88 63 2F 68 BB CB 5D FA FA FB EE E4 1E D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
# MS 35
# 97 3D BB B5 93 B4 E3 27 9A F3 C3 78 7D 2F 01 99 C8 1E F8 C8 52 B3 AA B7 C2 3A A7 D5 3F 81 0D A0 AF B3 C8 F6 70 0E 7D FC C2 88 63 2F 68 BB CB 5D FA FA FB EE E4 1D D2 6F 02 F4 8A 6E 0F F5 42 6D F4 F5
