#! /usr/bin/env python3

from datetime import datetime
import re
import json

from util import DATA, DIFFICULTIES, ERROR
import util
import mapUtil
from scenario import Story, UNIT_IMAGE

def getHeroWithName(name: str):
    heroes = util.fetchFehData("Common/SRPG/Person", None)
    for hero in heroes:
        if util.getName(hero['id_tag']) == name:
            return hero
    return {}

def getBHBHero(mapId: str):
    scenario = util.readFehData("USEN/Message/Scenario/"+mapId+".json")
    faceNames = list(dict.fromkeys(re.findall(r"ch\d{2}_\d{2}_\w+", scenario[1]['value'])))
    heroes = [UNIT_IMAGE[faceName] for faceName in faceNames]

    mapName = util.getName(mapId)
    heroesName = [util.getName(heroes[i]['id_tag']) for i in range(len(heroes))]
    if heroesName[0][0] == mapName[0] and heroesName[1][0] == mapName[4] and mapName[0] != mapName[4]:
        return heroes
    elif heroesName[0][0] == mapName[4] and heroesName[1][0] == mapName[0] and mapName[0] != mapName[4]:
        heroes[0], heroes[1] = heroes[1], heroes[0]
        return heroes
    elif mapName[0] != mapName[4]:
        print(ERROR + "Unexpected heroes on " + mapId + ': ' + ' '.join(heroesName))
    else:
        while True:
            rep = util.askFor(f"{heroesName[0]}|{heroesName[1]}|1|2", f"Which unit is the first one {heroesName[0]} or {heroesName[1]}?")
            if rep and (rep == '1' or rep == heroesName[0]):
                return heroes
            elif rep and ((rep == '2' or rep == heroesName[1])):
                heroes[0], heroes[1] = heroes[1], heroes[0]
                return heroes

def HBMapInfobox(StageEvent: dict, group: str, SRPGMap: dict=None):
    if SRPGMap and 'field' in SRPGMap and 'player_pos' in SRPGMap:
        SRPGMap['field'].update(SRPGMap['player_pos'])
    info = {
        'id_tag': StageEvent['id_tag'],
        'banner': 'Banner ' + StageEvent['banner_id'] + '.webp',
        'group': group,
        'requirement': '',
        'lvl': {}, 'rarity': {}, 'stam': {}, 'reward': {},
        'map': SRPGMap and 'field' in SRPGMap and SRPGMap['field'] or {'id': StageEvent['id_tag'], 'player_pos': []},
        'bgm2': ""
    }
    info['requirement'] += 'All allies must survive.' if StageEvent['scenarios'][-1]['survives'] else ''
    info['requirement'] += (info['requirement'] != '' and '<br>' or '') + "Cannot use {{It|Light's Blessing}}." if StageEvent['scenarios'][-1]['no_lights_blessing'] else ''
    info['requirement'] += (info['requirement'] != '' and '<br>' or '') + f"Turns to win: {StageEvent['scenarios'][-1]['turns_to_win']}" if StageEvent['scenarios'][-1]['turns_to_win'] != 0 else ''
    info['requirement'] += (info['requirement'] != '' and '<br>' or '') + f"Turns to defend: {StageEvent['scenarios'][-1]['turns_to_defend']}" if StageEvent['scenarios'][-1]['turns_to_defend'] != 0 else ''

    if StageEvent['scenarios'][-1]['reinforcements']:
        info['mode'] = 'Reinforcement Map'
    for index in range(len(StageEvent['scenarios'])):
        diff = DIFFICULTIES[StageEvent['scenarios'][index]['difficulty']]
        info['lvl'].update({diff: StageEvent['scenarios'][index]['true_lv']})
        info['rarity'].update({diff: StageEvent['scenarios'][index]['stars']})
        info['stam'].update({diff: StageEvent['scenarios'][index]['stamina']})
        info['reward'].update({diff: StageEvent['scenarios'][index]['reward']})

    if SRPGMap and SRPGMap != {}:
        "Toto"
    return mapUtil.MapInfobox(info)

def HBUnitData(StageEvent: dict, SRPGMap: dict, hero):
    if type(hero) != list:
        hero = [hero]

    s = "==Unit data==\n"
    s += "{{#invoke:UnitData|main"
    if SRPGMap == {} or not 'units' in SRPGMap:
        s += "|globalai="
    if StageEvent['scenarios'][-1]['reinforcements']:
        s += "\n|mapImage=" + mapUtil.MapImage(SRPGMap and 'field' in SRPGMap and SRPGMap['field'] or {'id': StageEvent['id_tag']}, True, True)
    if SRPGMap and 'units' in SRPGMap:
        "Toto"
        #for idiff in range(len(SRPGMap)):
        #    s += "|" + DIFFICULTIES[StageEvent['maps'][idiff]['scenarios'][index]['difficulty']] + "="
        #    s += mapUtil.UnitData(SRPGMap[idiff]) + "\n"
    else:
        for idiff in range(StageEvent['scenario_count']):
            s += '\n|' + DIFFICULTIES[StageEvent['scenarios'][idiff]['difficulty']] + '='
            units = []
            for i in range(StageEvent['scenarios'][idiff]['difficulty'] > 2 and 6 or 5):
                units += [{'rarity': StageEvent['scenarios'][idiff]['stars'], 'true_lv': StageEvent['scenarios'][idiff]['true_lv']}]
                if idiff > 2 and i != 0:
                    units[-1]['refine'] = 1
            for i in range(len(hero)):
                units[i]['id_tag'] = hero[i]['id_tag']
                units[i]['cooldown_count'] = None
            if StageEvent['scenarios'][idiff]['reinforcements']:
                units += [{'rarity': StageEvent['scenarios'][idiff]['stars'], 'true_lv': StageEvent['scenarios'][idiff]['true_lv'], 'spawn_count': 0}]
                if idiff > 2:
                    units[-1]['refine'] = 1
            s += mapUtil.UnitData({'units': units})
    return s + "\n}}\n"

def LHBMap(mapId: str):
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent")[mapId]
    SRPGMap = util.readFehData("../feh-assets-json/extras/SRPGMap/"+mapId+"A.json", True)

    hero = getHeroWithName(util.getName(mapId))
    kind = hero['legendary']['element'] > 4 and 'Mythic Hero Battle' or 'Legendary Hero Battle'
    startTime = datetime.strptime(StageEvent['avail']['start'], '%Y-%m-%dT%H:%M:%SZ')

    content = ""
    content += HBMapInfobox(StageEvent, kind, SRPGMap) + "\n"
    content += mapUtil.MapAvailability(StageEvent['avail'], f"{kind}! ({startTime.strftime('%b %Y')}) (Notification)", f"[[{kind}]]")
    content += HBUnitData(StageEvent, SRPGMap, hero) + '\n'
    content += Story(mapId) + "\n"
    content += "==Trivia==\n*\n"
    content += mapUtil.InOtherLanguage(["MID_STAGE_"+mapId, "MID_STAGE_HONOR_"+mapId], 1)
    content += "{{Special Maps Navbox}}"
    return content

def BHBMap(mapId: str):
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent")[mapId]
    SRPGMap = util.readFehData("../feh-assets-json/extras/SRPGMap/"+mapId+"A.json", True)

    heroes = getBHBHero(mapId)
    name = util.getName(mapId)
    if name[0] != name[4]:
        name = name.replace(name[4], DATA["M"+heroes[1]['id_tag']], 1).replace(name[0], DATA["M"+heroes[0]['id_tag']], 1)
    else:
        name = name.replace(name[0], DATA["M"+heroes[1]['id_tag']], 2).replace(DATA["M"+heroes[1]['id_tag']], DATA["M"+heroes[0]['id_tag']], 1)

    content = ""
    content += HBMapInfobox(StageEvent, "Bound Hero Battle", SRPGMap) + "\n"
    content += mapUtil.MapAvailability(StageEvent['avail'], f"Bound Hero Battle: {DATA['M'+heroes[0]['id_tag']]} & {DATA['M'+heroes[1]['id_tag']]} (Notification)", "map was a [[Bound Hero Battle]] map which")
    content += HBUnitData(StageEvent, SRPGMap, heroes) + '\n'
    content += Story(mapId) + "\n"
    content += "==Trivia==\n*\n"
    content += mapUtil.InOtherLanguage(["MID_STAGE_"+mapId, "MID_STAGE_HONOR_"+mapId], 1)
    content += "{{Special Maps Navbox}}"

    return {name: content}

def GHBMap(mapId: str):
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent")[mapId]
    SRPGMap = util.readFehData("../feh-assets-json/extras/SRPGMap/"+mapId+"A.json", True)

    hero = getHeroWithName(util.getName(mapId))

    content = ""
    content += HBMapInfobox(StageEvent, "Grand Hero Battle", SRPGMap) + "\n"
    content += mapUtil.MapAvailability(StageEvent['avail'], f"Grand Hero Battle - {util.getName(mapId)} (Notification)", "[[Grand Hero Battle]]")
    content += HBUnitData(StageEvent, SRPGMap, hero) + '\n'
    content += Story(mapId) + "\n"
    content += "==Trivia==\n*\n"
    content += mapUtil.InOtherLanguage(["MID_STAGE_"+mapId, "MID_STAGE_HONOR_"+mapId], 1)
    content += "{{Special Maps Navbox}}"

    return content

from sys import argv

if __name__ == '__main__':
    if len(argv) != 2 or len(argv[1]) != 5:
        exit(0)
    if argv[1][0] == 'T' and util.getName(argv[1])[2] == '&':
        maps = list(BHBMap(argv[1]).items())[0]
        print(maps[0], maps[1], sep='\n')
    elif argv[1][0] == 'T':
        print(GHBMap(argv[1]))
    elif argv[1][0] == 'L':
        print(LHBMap(argv[1]))