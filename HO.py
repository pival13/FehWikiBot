#! /usr/bin/env python3

from datetime import datetime

import util
import mapUtil
from globals import DATA

SERIES_BGM = {
    0:  ["bgm_map_Brave_02.ogg", "bgm_menu_theme01.ogg"],
    1:  ["bgm_map_FE12_01.ogg", "bgm_battle_FE12_01.ogg"],
    2:  ["bgm_map_FE15_01.ogg", "bgm_battle_FE15_01.ogg"],
    3:  ["bgm_map_FE04_01.ogg", "bgm_battle_FE04_01.ogg"],
    4:  ["bgm_map_FE05_01.ogg", "bgm_battle_FE05_01.ogg"],
    5:  ["bgm_map_FE06_01.ogg", "bgm_battle_FE06_01.ogg"],
    6:  ["bgm_map_FE07_01.ogg", "bgm_battle_FE07_01.ogg"],
    7:  ["bgm_map_FE08_01.ogg", "bgm_battle_FE08_01.ogg"],
    8:  ["bgm_map_FE09_01.ogg", "bgm_battle_FE09_01.ogg"],
    9:  ["bgm_map_FE10_03.ogg", "bgm_battle_FE10_01.ogg"],
    10: ["bgm_map_FE13_04.ogg", "bgm_battle_FE13_01.ogg"],
    11: ["bgm_map_FE14_03.ogg", "bgm_battle_FE14_01.ogg"],
    12: ["bgm_map_FE16_01.ogg", "bgm_battle_FE16_01.ogg"],
    13: ["bgm_map_FEG_01.ogg", "bgm_menu_theme01.ogg"],
}

def getHeroJson(heroId: int):
    HERO = util.fetchFehData("Common/SRPG/Person", False)

    for hero in HERO:
        if hero['id_num'] == heroId:
            return hero
    return {}

def HeroicOrdeals(mapId: str):
    heroId = int(mapId[1:])
    hero = getHeroJson(heroId)
    SRPGMap = util.readFehData("Common/SRPGMap/" + mapId + ".json")
    diff = heroId < 191 and 'Normal' or heroId < 317 and 'Hard' or 'Lunatic'
    release = util.cargoQuery("Units", "ReleaseDate", "IntID="+str(heroId), limit=1)
    release = release[0]["ReleaseDate"] if release and len(release) > 0 else datetime.now().strftime("%Y-%m-%d")

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
        'bgms': SERIES_BGM[hero['series']]
    }) + "\n"
    content += mapUtil.MapAvailability({ 'start': ((release + 'T07:00:00Z') if release else None) })
    content += "==Unit data==\n{{#invoke:UnitData|main\n|" + diff + "=" + mapUtil.UnitData(SRPGMap) + "\n}}\n"
    content += mapUtil.InOtherLanguage(["MID_STAGE_SELECT_HERO_TRIAL", "M" + hero['id_tag']], "a", False)
    content += "{{Heroic Ordeals Navbox}}"

    return content

from sys import argv

if __name__ == "__main__":
    print(HeroicOrdeals(argv[1]))