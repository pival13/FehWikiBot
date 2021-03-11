#!/usr/bin/env python3

import REutil as util

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
