#! /usr/bin/env python3

import requests

from util import URL, DATA
import util
import mapUtil

SERIES_BGM = [
    ["bgm_map_Brave_02.ogg", "bgm_menu_theme01.ogg"],
    ["bgm_map_FE12_01.ogg", "bgm_battle_FE12_01.ogg"],
    ["bgm_map_FE15_01.ogg", "bgm_battle_FE15_01.ogg"],
    ["bgm_map_FE04_01.ogg", "bgm_battle_FE04_01.ogg"],
    ["bgm_map_FE05_01.ogg", "bgm_battle_FE05_01.ogg"],
    ["bgm_map_FE06_01.ogg", "bgm_battle_FE06_01.ogg"],
    ["bgm_map_FE07_01.ogg", "bgm_battle_FE07_01.ogg"],
    ["bgm_map_FE08_01.ogg", "bgm_battle_FE08_01.ogg"],
    ["bgm_map_FE09_01.ogg", "bgm_battle_FE09_01.ogg"],
    ["bgm_map_FE10_03.ogg", "bgm_battle_FE10_01.ogg"],
    ["bgm_map_FE13_04.ogg", "bgm_battle_FE13_01.ogg"],
    ["bgm_map_FE14_03.ogg", "bgm_battle_FE14_01.ogg"],
    ["bgm_map_FE16_01.ogg", "bgm_battle_FE16_01.ogg"],
    ["bgm_map_FEG_01.ogg", "bgm_menu_theme01.ogg"],
]

def getUnitRelease(heroID: int):
    try:
        result = requests.get(url=URL, params={
            "action": "cargoquery",
            "tables": "Units",
            "fields": "ReleaseDate",
            "where": "IntID=" + str(heroID),
            "limit": 1,
            "format": "json"
        }).json()
        return result['cargoquery'][0]['title']['ReleaseDate'] if 'cargoquery' in result and len(result['cargoquery']) else None

    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return getUnitRelease(heroID)

def HOmap(mapId: str):
    heroId = int(mapId[1:])
    hero = util.getHeroJson(heroId)
    SRPGMap = util.readFehData("Common/SRPGMap/" + mapId + ".json")
    diff = heroId < 191 and 'Normal' or heroId < 317 and 'Hard' or 'Lunatic'
    release = getUnitRelease(heroId)

    SRPGMap['field'].update({'player_pos': SRPGMap['player_pos']})

    content = "{{HeroPage Tabs/Heroic Ordeals}}"
    content += mapUtil.MapInfobox({
        'title': DATA["MID_STAGE_SELECT_HERO_TRIAL"],
        'name': DATA["M"+hero['id_tag']],
        'group': 'Heroic Ordeals',
        'map': SRPGMap['field'],
        'lvl': {diff: (heroId < 191 and 30 or heroId < 317 and 35 or 40)},
        'rarity': {diff: (heroId < 191 and 4 or 5)},
        'stam': {diff: 0},
        'reward': {diff: [{"kind": 30, "move_type": hero['move_type'], "count": (heroId < 191 and 2 or heroId < 317 and 8 or 40)}]},
        'requirement': "The ordeal challenger must<br>defeat at least 2 foes.<br>All allies must survive.<br>Turns to win: 20",
        'bgm': SERIES_BGM[hero['series']][0],
        'bgm2': SERIES_BGM[hero['series']][1]
    }) + "\n"
    content += mapUtil.MapAvailability({ 'start': ((release + 'T07:00:00Z') if release else None) })
    content += "==Unit data==\n{{#invoke:UnitData|main\n|" + diff + "=" + mapUtil.UnitData(SRPGMap) + "\n}}\n"
    content += mapUtil.InOtherLanguage(["MID_STAGE_SELECT_HERO_TRIAL", "M" + hero['id_tag']], "a", False)
    content += "{{Heroic Ordeals Navbox}}"

    return content

from sys import argv

if __name__ == "__main__":
    print(HOmap(argv[1]))