#! /usr/bin/env python3

import json
import re
import util
from globals import TIME_FORMAT, MIN_TIME, MAX_TIME
from reward import parseReward
from datetime import datetime, timedelta

from MissionTemplated import templateMissions

SORTING_PATTERN = [
    {'value': 1, 'pattern': r'YEAR'},
    {'value': 2, 'pattern': r'^W?_?M'}, # Monthly
    {'value': 3, 'pattern': r'^WEEK_'},
    {'value': 4, 'pattern': r'^DAILY_'},
    {'value': 10, 'pattern': r'STORY', 'nbQuests': 5}, # Story maps
    {'value': 11, 'pattern': r'STORY', 'nbQuests': 3}, # Paralogue maps
    {'value': 15, 'pattern': r'VOTE'}, # Voting Gauntlet
    {'value': 16, 'pattern': r'SENKA'}, # Tempest Trials
    {'value': 17, 'pattern': r'TAPBTL'}, # Tap Battle
    {'value': 18, 'pattern': r'DAISEIATU'}, # Grand Conquests
    {'value': 20, 'pattern': r'SHADOW'}, # Rokkr Sieges
    {'value': 23, 'pattern': r'MJOLNIR'}, #Mjölnir's Strike
	{'value': 24, 'pattern': r'MAMORE'}, # Frontline Phalanx
	{'value': 25, 'pattern': r'BOARDGAME'}, # Pawns of Loki
	{'value': 26, 'pattern': r'JOURNEY'}, # Heroes Journey
    {'value': 31, 'pattern': r'HERO'}, # Grand Hero
    {'value': 32, 'pattern': r'KIZUNA'}, # Bound Hero
    #[] = {'pattern': r'CHARA'}, # Three Heroes
    #[] = {'pattern': r'SKY'}, # Aether Raids
    #[] = {'pattern': r'ARENA'}, # Coliseum
    #[] = {'pattern': r'BRAVE'}, # Unit specific (Alfonse, Ljosalfar & Heroes, etc)
    #[] = {'pattern': r'ADVANCE'} # Movetype 'Strike'
    #[] = {'pattern': r'BIND'} # Movetype 'Mastery'
    {'value': 50, 'pattern': r'SUBSC'}, # FeH Pass
]

def stringifyQuests(groups: list):
    for i,group in enumerate(groups):
        if isinstance(group,str):
            groups[i] = {'template': group}
        else:
            groups[i]['quests'] = [
                json.dumps(quest, indent=0, ensure_ascii=False)\
                    .replace("\\\"", "\\@").replace("\": ", "=").replace("\"", "").replace("\\@", "\"")\
                    .replace(",\n", ";").replace('}\n','};').replace('\n','')
            for quest in group['quests']]
    quests = json.dumps(groups, indent=2, ensure_ascii=False)
    quests = quests.replace("\\\"", "\\@").replace("\": ", "=").replace("\"", "").replace("\\@", "\"")
    quests = quests.replace(",\n", ";\n")
    return quests

def groupQuestJsonToStr(groups: list):
    groups = parseQuestGroup(groups)
    if len(groups) == 0:
        return "[]"

    mergeGroup = []
    for group in groups:
        if any([group['title'] == mg['title'] and group['quests'] == mg['quests'] for mg in mergeGroup]):
            for mg in mergeGroup:
                if group['title'] == mg['title'] and group['quests'] == mg['quests']:
                    mg['startTime'] += group['startTime']
                    mg['endTime'] += group['endTime']
        else:
            mergeGroup += [group]
    
    sameTimeLength = lambda qus, i : qus['startTime'][i+1] - qus['startTime'][i] == qus['startTime'][i+2] - qus['startTime'][i+1] and \
        qus['endTime'][i+1] - qus['endTime'][i] == qus['endTime'][i+2] - qus['endTime'][i+1]
    for gr in mergeGroup:
        if len(gr['startTime']) > 2 and all([sameTimeLength(gr, i) for i in range(len(gr['startTime'])-2)]):
            gr['availTime'] = int((gr['endTime'][0] - gr['startTime'][0]).total_seconds()) + 1
            gr['cycleTime'] = int((gr['startTime'][1] - gr['startTime'][0]).total_seconds())
            if gr['availTime'] == gr['cycleTime']:
                gr.pop('cycleTime')
            gr['startTime'] = gr['startTime'][0].strftime(TIME_FORMAT)
            gr['endTime'] = gr['endTime'][-1].strftime(TIME_FORMAT)
        else:
            gr['startTime'] = ','.join([t.strftime(TIME_FORMAT) for t in gr['startTime']])
            gr['endTime'] = ','.join([t.strftime(TIME_FORMAT) for t in gr['endTime']])
            gr.pop('availTime')
            gr.pop('cycleTime')

    templateMissions(mergeGroup)
    return stringifyQuests(mergeGroup)

def parseSortValue(quests: dict):
    for cond in SORTING_PATTERN:
        if  (not 'pattern' in cond or re.findall(cond['pattern'], quests['id_tag'])) and \
            (not 'nbQuests' in cond or cond['nbQuests'] == quests['lists'][0]['quest_count']):
            return cond['value']
    return 40

def parseStage(quest: dict, startTime: str):#TODO
    if quest['game_mode'] == 7:#VG
        return ";stage="
        #query
    elif quest['game_mode'] == 8:#TT
        return ";stage=" + util.getName('MID_SEQUENTIAL_MAP_TERM_' + quest['map_group'])
    elif quest['game_mode'] == 12:#TB
        return ";stage="
        #query
    elif quest['game_mode'] == 14:#GC
        return ";stage="
        #query
    elif quest['game_mode'] == 21:#RS
        return ";stage="
        #query
    elif quest['map_group']:
        if quest['map_group'][0] == 'T':
            return ";stage=" + util.cargoQuery('Maps', where=f"Map='{quest['map_group']}'")[0]['Page']
        else:
            return ";stage=" + util.getName(quest['map_group'])
    else:
        return ""

def parseQuests(questDiffs: dict, startTime: str):
    quests = []
    for qDiff in questDiffs:
        for quest in qDiff['quests']:
            qu = {
                'name': util.getName('MID_MISSION_' + (quest['common_id'] or quest['quest_id'])),
                'description': util.getName('MID_MISSION_H_' + (quest['common_id'] or quest['quest_id'])).replace("\n", "<br>"),
                'times': quest['times'],
                'reward': parseReward(quest['reward']),
            }
            if quest['times'] == 1:
                qu.pop('times')
            stage = parseStage(quest, startTime)
            if stage:
                qu['stage'] = stage[7:]
            if quest['unit_reqs']['hero_id']:
                qu['unit'] = util.getName(quest['unit_reqs']['hero_id'])
            if qDiff['difficulty']:
                qu['difficulty'] = qDiff['difficulty'].capitalize()
            quests.append(qu)
    return quests

def parseQuestGroup(missions: list):
    missions = [{
        "title": util.getName('MID_MISSION_' + m['title']),
        "startTime": [datetime.strptime(m['avail']['start'] if 'avail' in m else m['start'] if 'start' in m else MIN_TIME, TIME_FORMAT)],
        "endTime": [datetime.strptime(m['avail']['finish'] if 'avail' in m else m['finish'] if 'finish' in m else MAX_TIME, TIME_FORMAT)-timedelta(seconds=1)],
        "availTime": None,
        "cycleTime": None,
        "sort": parseSortValue(m),
        "quests": parseQuests(m['lists'], m['avail']['start'] if 'avail' in m else m['start'] if 'start' in m else MIN_TIME)
    } for m in missions]
    return missions

def Mission(minTime, maxTime):
    minTime = datetime.strptime(minTime, TIME_FORMAT)
    maxTime = datetime.strptime(maxTime, TIME_FORMAT)
    allMissions = util.fetchFehData("Common/Mission", None)
    missions = []
    for m in allMissions:
        start = datetime.strptime(m['avail']['start'] if 'avail' in m else m['start'] if 'start' in m else MIN_TIME, TIME_FORMAT)
        if start >= minTime and start <= maxTime:
            missions += [m]
    return groupQuestJsonToStr(missions)

def MissionsOf(update: str):
    missions = util.readFehData("Common/Mission/"+update+".json")
    return groupQuestJsonToStr(missions)

from sys import argv

if __name__ == "__main__":
    begin = MIN_TIME if len(argv) < 2 else argv[1]
    end = MAX_TIME if len(argv) < 3 else argv[2]
    print(Mission(begin, end))