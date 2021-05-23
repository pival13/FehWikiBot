#!/usr/bin/env python3

from datetime import datetime

import REutil as util

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

def parseSubscriptionCostume(data):
    result = []
    nbGroup = util.getInt(data, 0x08, 0x17E55C54)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, 0x00) + 0x20*iGr
        result += [{
            "id": util.getLong(data, offGr+0x00, 0xBFC98CB0CFDCD2D1),
            #"num": 
            "avail_start": datetime.utcfromtimestamp(util.getLong(data, offGr+0x08, 0x91f9ebb0b4a90f77)).isoformat() + "Z" if util.getLong(data, offGr+0x08) ^ 0x91f9ebb0b4a90f77 != 0xFFFFFFFFFFFFFFFF else None,
            "avail_finish": datetime.utcfromtimestamp(util.getLong(data, offGr+0x10, 0x75dc9cc8b9ece87f)).isoformat() + "Z" if util.getLong(data, offGr+0x10) ^ 0x75dc9cc8b9ece87f != 0xFFFFFFFFFFFFFFFF else None,
            "hero_id": util.getString(data, offGr+0x18)
        }]
    return result