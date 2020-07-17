#! /usr/bin/env python3

import json
import re
from util import TIME_FORMAT, MIN_TIME, MAX_TIME
import util
from reward import parseReward
from datetime import datetime, timedelta

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

    return json.dumps(mergeGroup, indent=2, ensure_ascii=False)\
        .replace(",\n", ";\n").replace("\\\"", "\\@").replace("\": ", "=").replace("\"", "").replace("\\@", "\"")

def parseSortValue(quests: dict):
    return 0 #TODO

def parseStage(quest: dict, startTime: str):
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
            return ";stage="
        else:
            return ";stage=" + util.getName(quest['map_group'])
    else:
        return ""

def parseQuests(questDiffs: dict, startTime: str):
    quests = []
    for qDiff in questDiffs:
        for quest in qDiff['quests']:
            qu = "{name=" + util.getName('MID_MISSION_' + (quest['common_id'] or quest['quest_id'])) + \
                ";description=" + util.getName('MID_MISSION_H_' + (quest['common_id'] or quest['quest_id']))
            if quest['times'] != 1:
                qu += f";times={quest['times']}"
            qu += ";reward=" + parseReward(quest['reward']) + parseStage(quest, startTime)
            if quest['unit_reqs']['hero_id']:
                qu += ";unit=" + util.getName(quest['unit_reqs']['hero_id'])
            if qDiff['difficulty']:
                qu += ";difficulty=" + qDiff['difficulty'].capitalize()
            quests += [qu + (";}" if qu[-1] == "}" else "}")]
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
    #print(MissionsOf("200602_summer"))
    print(Mission(begin, end))