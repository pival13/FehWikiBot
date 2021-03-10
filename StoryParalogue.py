#! /usr/bin/env python3

import re

from util import DATA, DIFFICULTIES, ROMAN
import util
import mapUtil
from scenario import Story

def StoryMapInfobox(stage: dict, field: dict, mapId: str, index: int):
    map = {}
    map['banner'] = stage['id_tag'] + (' C' if index == 4 else '')  + ".webp"
    map['id_tag'] = mapId
    if stage['maps'][0]['scenarios'][index]['reinforcements']:
        map['mode'] = 'Reinforcement Map'
    if stage['book']:
        map['book'] = 'Book ' + ROMAN[stage['book']]
    map['group'] = DATA['MID_CHAPTER_TITLE_' + stage['id_tag']] + ": " + DATA['MID_CHAPTER_' + stage['id_tag']] if stage['id_tag'][:3] != 'CXX' else 'Xenologue'
    map['map'] = field
    map['stam'] = {}
    map['lvl'] = {}
    map['rarity'] = {}
    map['reward'] = {}
    for idiff in range(len(stage['maps'])):
        diff = DIFFICULTIES[stage['maps'][idiff]['scenarios'][index]['difficulty']]
        map['lvl'].update({diff: stage['maps'][idiff]['scenarios'][index]['true_lv']})
        map['rarity'].update({diff: stage['maps'][idiff]['scenarios'][index]['stars']})
        map['stam'].update({diff: stage['maps'][idiff]['scenarios'][index]['stamina']})
        map['reward'].update({diff: stage['maps'][idiff]['scenarios'][index]['reward']})

    map['requirement'] = []
    if stage['maps'][0]['scenarios'][index]['survives']: map['requirement'] += ['All allies must survive.']
    if stage['maps'][0]['scenarios'][index]['no_lights_blessing']: map['requirement'] += ["Cannot use {{It|Light's Blessing}}."]
    if stage['maps'][0]['scenarios'][index]['turns_to_win'] != 0: map['requirement'] += [f"Turns to win: {stage['maps'][0]['scenarios'][index]['turns_to_win']}"]
    if stage['maps'][0]['scenarios'][index]['turns_to_defend'] != 0: map['requirement'] += [f"Turns to defend: {stage['maps'][0]['scenarios'][index]['turns_to_defend']}"]
    map['requirement'] = '<br>'.join(map['requirement'])
    map['bgms'] = util.getBgm(mapId)

    return mapUtil.MapInfobox(map)

def StoryUnitData(SRPGMap: list, StageEvent: dict, index: int):
    s = "==Unit data==\n{{#invoke:UnitData|main\n"

    if StageEvent['maps'][0]['scenarios'][index]['reinforcements']:
        s += "|mapImage=" + mapUtil.MapImage(SRPGMap[0]['field'], True, True) + "\n"

    for idiff in range(len(SRPGMap)):
        s += "|" + DIFFICULTIES[StageEvent['maps'][idiff]['scenarios'][index]['difficulty']] + "="
        s += mapUtil.UnitData(SRPGMap[idiff]) + "\n"

    return s + "}}\n"

def StoryMap(mapId: str, StageScenario: dict=None, index: int=None, notif: str=''):
    if not StageScenario:
        for scenario in util.fetchFehData("Common/SRPG/StageScenario", None):
            for m in scenario['maps'][0]['scenarios']:
                if m['id_tag'][:-1] == mapId:
                    StageScenario = scenario
                    index = scenario['maps'][0]['scenarios'].index(m)
                    groupName = DATA['MID_CHAPTER_TITLE_' + scenario['id_tag']] + ": " + DATA['MID_CHAPTER_' + scenario['id_tag']]
                    notif = util.askFor(None, f"What is the notification for {groupName} ({scenario['id_tag']})?") or ''

    SRPGMap = [util.readFehData("Common/SRPGMap/" + Id + ".json") for Id in [StageScenario['maps'][i]['scenarios'][index]["id_tag"] for i in range(3)]]

    SRPGMap[0]['field'].update({'player_pos': SRPGMap[0]['player_pos']})

    content = StoryMapInfobox(StageScenario, SRPGMap[0]['field'], mapId, index)
    content += "\n"
    content += mapUtil.MapAvailability(StageScenario['avail'], notif)
    content += StoryUnitData(SRPGMap, StageScenario, index)
    content += '==Other appearances==\n{{BattleAppearances}}\n\n'
    content += Story(mapId)
    content += mapUtil.InOtherLanguage('MID_STAGE_' + mapId)
    content += "{{Story Maps Navbox|book=" + str(StageScenario['book']) + "}}"

    return content

def ParalogueMap(mapId: str, StageScenario: dict=None, index: int=None, notif: str=''):
    if not StageScenario:
        for scenario in util.fetchFehData("Common/SRPG/StageScenario", None):
            for m in scenario['maps'][0]['scenarios']:
                if m['id_tag'][:-1] == mapId:
                    StageScenario = scenario
                    index = scenario['maps'][0]['scenarios'].index(m)
                    notif = "Special Heroes Summoning Event: " + util.getName('MID_CHAPTER_'+StageScenario['id_tag']) + " (Notification)"
                    answer = util.askFor(None, "Is the notification '"+notif+"'?")
                    notif = notif if (not answer or re.match('y|o|yes|oui|', answer, re.IGNORECASE)) else answer

    SRPGMap = [util.readFehData("Common/SRPGMap/" + Id + ".json") for Id in [StageScenario['maps'][i]['scenarios'][index]["id_tag"] for i in range(3)]]

    SRPGMap[0]['field'].update({'player_pos': SRPGMap[0]['player_pos']})

    content = StoryMapInfobox(StageScenario, SRPGMap[0]['field'], mapId, index)
    content += "\n"
    content += mapUtil.MapAvailability(StageScenario['avail'], notif)
    content += StoryUnitData(SRPGMap, StageScenario, index)
    content += '==Other appearances==\n{{BattleAppearances}}\n\n'
    content += Story(mapId)
    content += mapUtil.InOtherLanguage('MID_STAGE_' + mapId)
    content += "{{Paralogue Maps Navbox}}"

    return content

def StoryGroup(groupId: str):
    StageScenario = util.fetchFehData("Common/SRPG/StageScenario")[groupId]
    groupName = DATA['MID_CHAPTER_TITLE_' + groupId] + ": " + DATA['MID_CHAPTER_' + groupId]
    notif = util.askFor(None, f"What is the notification for {groupName} ({groupId})?") or ''

    ret = {}
    for i in range(StageScenario['maps'][0]['scenario_count']):
        ret.update({util.getName("MID_STAGE_" + StageScenario['maps'][0]['scenarios'][i]["id_tag"][:-1]):
            StoryMap(StageScenario['maps'][0]['scenarios'][i]["id_tag"][:-1], StageScenario, i, notif)})
    return ret

def ParalogueGroup(groupId: str):
    StageScenario = util.fetchFehData("Common/SRPG/StageScenario")[groupId]
    notif = "Special Heroes Summoning Event: " + util.getName('MID_CHAPTER_'+StageScenario['id_tag']) + " (Notification)"
    answer = util.askFor(None, "Is the notification '"+notif+"'?")
    notif = notif = notif if (not answer or re.match('y|o|yes|oui|', answer, re.IGNORECASE)) else answer

    ret = {}
    for i in range(StageScenario['maps'][0]['scenario_count']):
        ret.update({util.getName("MID_STAGE_" + StageScenario['maps'][0]['scenarios'][i]["id_tag"][:-1]):
            ParalogueMap(StageScenario['maps'][0]['scenarios'][i]["id_tag"][:-1], StageScenario, i, notif)})
    return ret

from sys import argv

if __name__ == "__main__":
    if argv[1][0] == 'X':
        print(ParalogueMap(argv[1]))
    elif argv[1][0] == 'S':
        print(StoryMap(argv[1]))
    elif argv[1][:2] == 'CX':
        print(ParalogueGroup(argv[1]))
    elif argv[1][0] == 'C':
        print(StoryGroup(argv[1]))