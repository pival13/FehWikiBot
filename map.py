#! /usr/bin/env python3

from sys import argv
import requests
import json
import re

from util import URL, TODO, ERROR, DATA, TIME_FORMAT
import util
from TD import TDmap
from HO import HOmap
from StoryParalogue import ParalogueMap, ParalogueGroup, StoryGroup, StoryMap
from DerivedMap import SquadAssault, ChainChallengeGroup, ChainChallengeMap
from HB import BHBMap, LHBMap, GHBMap
from RD import RDmap
from EventMap import exportEventMap

def exportMap(name: str, content: str):
    S = util.fehBotLogin()

    try:
        result = S.post(url=URL, data={
            "action": "edit",
            "title": name,
            "text": content,
            "createonly": True,
            "bot": True,
            "tags": "automated",
            "summary": "bot: new map",
            "watchlist": "nochange",
            "token": util.getToken(),
            "format": "json"
        }).json()
        if 'error' in result and result['error']['code'] == 'articleexists':
            print(f"Page already exist: " + name)
        elif 'edit' in result and result['edit']['result'] == 'Success':
            print(f"Page created: " + name)
        else:
            print(result)

    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        exportMap(name, content)

def exportGroup(group: dict):
    for name in group:
        exportMap(name, group[name])

def parseMapId(mapId: str):
    if "MID_STAGE_"+mapId in DATA:
        name = DATA["MID_STAGE_"+mapId]
        if "MID_STAGE_HONOR_"+mapId in DATA:
            name += ": " + DATA["MID_STAGE_HONOR_"+mapId]
    elif "MID_STAGE_TITLE_"+mapId in DATA:
        name = DATA["MID_STAGE_TITLE_"+mapId]
    elif "MID_CHAPTER_" + mapId in DATA:
        name = DATA["MID_CHAPTER_"+mapId]
    elif mapId[0] == "Q":
        name = DATA["MID_STAGE_OCCUPATION"] + ": " + DATA["MID_STAGE_HONOR_OCCUPATION"]
    elif not mapId[0] == "H" and not re.fullmatch(r"V\d{4}-V\d{4}", mapId):
        print(ERROR + "Unknow map " + mapId)
        return

    if re.match(r"S\d{4}", mapId):
        exportMap(name, StoryMap(mapId))

    if re.match(r"C\d{4}", mapId):
        exportGroup(StoryGroup(mapId))

    elif re.match(r"X[X0-9]\d{3}", mapId):
        exportMap(name, ParalogueMap(mapId))

    elif re.match(r"CX\d{3}", mapId):
        exportGroup(ParalogueGroup(mapId))

    elif re.match(r"H\d{4}", mapId):
        hero = util.getHeroName(int(re.compile(r"H(\d+)").match(mapId)[1]))
        if hero:
            exportMap("Heroic Ordeals: " + hero + "'s Trial", HOmap(mapId))
        else:
            print(ERROR + "Unknow map: " + mapId)

    elif re.match(r"P[ABC]\d{3}", mapId):
        exportMap(name, TDmap(mapId))


    elif re.match(r"T\d{4}", mapId):
        if re.compile(r"\w & \w").search(name):
            exportGroup(BHBMap(mapId))
        else:
            exportMap(name + " (map)", GHBMap(mapId))

    elif re.match(r"L\d{4}", mapId):
        exportMap(name + " (map)", LHBMap(mapId))

    elif re.match(r"Q\d{4}", mapId):
        exportMap(name + " (" + str(int(mapId.replace("Q", ""))) + ")", RDmap(mapId))
        print(TODO + "Edit Grand Conquests Trivia")

    elif re.match(r"V\d{4}-V\d{4}", mapId):
        exportEventMap(mapId[:5], mapId[-5:])

    elif re.match(r"V\d{4}", mapId):
        exportEventMap(mapId)


    elif re.match(r"SB_\d{4}", mapId):
        exportMap(name, SquadAssault(mapId))

    elif re.match(r"ST_S\d{4}", mapId) or re.match(r"ST_X\d{4}", mapId):
        exportMap("Chain Challenge: " + (mapId[3] == 'S' and f"Book {util.ROMAN[int(mapId[5]) or 1]}, " or '') + name,
            ChainChallengeMap(mapId))

    elif re.match(r"ST_C\d{4}", mapId) or re.match(r"ST_CX\d{3}", mapId):
        exportGroup(ChainChallengeGroup(mapId))

    elif re.compile(r"BG_(WATER|WIND|EARTH|FIRE)_\d{4}").match(mapId): #TODO
        print("Blessed Garden: " + name)


    else:
        print(ERROR + "Unknow map " + mapId)


def parseTagUpdate(tag: str):
    StageBG = util.readFehData("Common/SRPG/BlessingGarden/"+tag+".json")
    StageSA = util.readFehData("Common/SRPG/SequentialTrialBind/"+tag+".json")
    StageCCS = util.readFehData("Common/SRPG/SequentialTrialMainStory/"+tag+".json")
    StageCCX = util.readFehData("Common/SRPG/SequentialTrialSideStory/"+tag+".json")
    StageEvent = util.readFehData("Common/SRPG/StageEvent/"+tag+".json")
    StagePuzzle = util.readFehData("Common/SRPG/StagePuzzle/"+tag+".json")
    StageScenario = util.readFehData("Common/SRPG/StageScenario/"+tag+".json")
    StagePerson = util.readFehData("Common/SRPG/Person/"+tag+".json")

    for stage in StagePerson:
        parseMapId(f"H{stage['id_num']:04}")
    for Stages in [StagePuzzle, StageScenario, StageEvent, StageBG, StageSA, StageCCS, StageCCX]:
        for stage in Stages:
            parseMapId(stage['id_tag'])
    findUpcoming()

from datetime import datetime
from mapUtil import MapAvailability

def findUpcoming():
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent/", False)
    print('Upcoming special maps:')
    for stage in StageEvent:
        datetime.fromordinal
        if datetime.strptime(stage['avail']['start'], TIME_FORMAT) > datetime.now():
            print(stage['id_tag'], util.getName(stage['id_tag']), MapAvailability(stage['avail'], "")[72:-17])

def main():
    if len(argv) < 2:
        print("Enter at least one map id")
        exit(0)
    elif len(argv) == 2 and re.match(r"\d+_\w+", argv[1]):
        parseTagUpdate(argv[1])
    elif len(argv) == 2 and argv[1] == 'upcoming':
        findUpcoming()
    else:
        for arg in argv:
            if arg == argv[0]:
                continue

            parseMapId(arg)


if __name__ == "__main__":
    main()