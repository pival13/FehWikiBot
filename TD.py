#! /usr/bin/env python3

from datetime import datetime
import re

import util
from globals import DATA, DIFFICULTIES
import mapUtil

TD_KIND = ['Basics', 'Skill Studies', 'Grandmaster']

def TDMapInfobox(stage: dict, field: dict):
    diff = DIFFICULTIES[stage['difficulty']]

    map = {}
    map['banner'] = 'Banner_Tactics_Drills_' + TD_KIND[stage['difficulty']].replace(" ", "_") + ".png"
    map['id_tag'] = stage['scenario']['id_tag']
    if stage['scenario']['reinforcements']:
        map['mode'] = 'Reinforcement Map'
    map['group'] = 'Tactics Drills: ' + TD_KIND[stage['difficulty']]
    map['stam'] = {diff: 0}
    map['reward'] = {diff: stage['scenario']['reward']}
    map['requirement'] = "Phases to win: " + str(stage['scenario']['turns_to_win'] * 2 - 1 + stage['scenario']['last_enemy_phase'])
    map['bgms'] = ["bgm_map_FE14_t.ogg"]
    map['map'] = field

    return mapUtil.MapInfobox(map)

def TDText(mapId: str):
    fileUSEN = util.readFehData("USEN/Message/Scenario/" + mapId + ".json")
    fileJPJA = util.readFehData("JPJA/Message/Scenario/" + mapId + ".json")
    messageEn = fileUSEN[0]['value'].replace('\n', '<br>') if len(fileUSEN) > 0 else ''
    messageJp = fileJPJA[0]['value'].replace('\n', '<br>') if len(fileJPJA) > 0 else ''
    return "==Text==\n{{TDMessage|" + \
          f"{messageEn}|{messageJp}}}}}\n"

def TDUnitData(SRPGMap: dict, StageEvent):
    return "==Unit data==\n" + \
           "{{#invoke:UnitData|main\n" + \
            (StageEvent['scenario']['reinforcements'] and ("|mapImage=" + mapUtil.MapImage(SRPGMap['field'], True, True) + "\n") or "") + \
           "|" + DIFFICULTIES[StageEvent['difficulty']] + "=" + \
            mapUtil.UnitData(SRPGMap) + "}}\n"

def Solution(field: dict, units: list):
    layout = mapUtil.MapImage(field, simpleMap=True)
    baseMap = re.search(r'baseMap=(\w*)', layout)
    backdrop = re.search(r'backdrop=(\w*)', layout)
    wallStyle = re.search(r'style=([^}|]*)', layout)
    walls = re.findall(r'(\w{2})=\{\{Wall.*?hp=(.)', layout)
    heroes = []
    enemies = [[]]
    for unit in units:
        if not unit['is_enemy']:
            heroes.append(util.getName(unit['id_tag']))
        elif unit['spawn_turns'] > 0 and len(enemies) < unit['spawn_turns']+1:
            enemies.insert(unit['spawn_turns'], [util.getName(unit['id_tag'])])
        else:
            enemies[max(unit['spawn_turns'],0)].append(util.getName(unit['id_tag']))
    for i, hero in enumerate(heroes):
        if ':' in hero and all([name == hero or name.find(hero[:hero.find(':')]) == -1 for name in heroes]):
            heroes[i] = hero[:hero.index(':')]
    for i, turn in enumerate(enemies):
        for j, enemy in enumerate(turn):
            if ':' in enemy and all([name == enemy or name.find(enemy[:enemy.find(':')]) == -1 for t in enemies for name in t]):
                enemies[i][j] = enemy[:enemy.index(':')]
    turns = [[f'{{enemy={enemy};move=}};' for enemy in turn] for turn in enemies]
    turns[0] = [f'{{unit={hero};move=;attack=}};' for hero in heroes] + turns[0]
    turns[0][0] = '<!--' + turns[0][0]
    turns[-1][-1] += '-->'
    return "==Solutions==\n" + \
           "{{#invoke:TacticsDrillsSolution|main\n" + \
          f"|baseMap={baseMap and baseMap[1] or ''}|backdrop={backdrop and backdrop[1] or ''}\n" + \
          f"|wallStyle={wallStyle and wallStyle[1] or ''}" + \
          f"|wall={{{';'.join([wall[0]+'='+wall[1] for wall in walls])}}}\n|" + \
         "\n|".join([f'turn{i+1}=[\n'+'\n'.join(s)+'\n]' for i, s in enumerate(turns)]) + \
           "\n}}\n"

def TacticsDrills(mapId: str):
    SRPGMap = util.readFehData("Common/SRPGMap/" + mapId + ".json")
    StageEvent = util.fetchFehData("Common/SRPG/StagePuzzle")[mapId]

    content = TDMapInfobox(StageEvent, SRPGMap['field']) + "\n"
    content += mapUtil.MapAvailability(StageEvent['avail'] or {}, "New Tactics Drills! (" + datetime.strptime(StageEvent['avail']['start'], util.TIME_FORMAT).strftime("%b %d, %Y").replace(" 0", " ") + ") (Notification)")
    content += TDText(mapId)
    content += TDUnitData(SRPGMap, StageEvent)
    content += Solution(SRPGMap['field'], SRPGMap['units'])
    content += mapUtil.InOtherLanguage('MID_STAGE_' + mapId)
    content += "{{Tactics Drills Navbox}}"

    return content

from sys import argv

if __name__ == "__main__":
    print(TacticsDrills(argv[1]))