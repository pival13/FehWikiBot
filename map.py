#! /usr/bin/env python3

from sys import argv
import requests
import json
import re

from util import URL, TODO, ERROR, DATA
import util
from TD import TDmap
from HO import HOmap
from StoryParalogue import ParalogueMap, ParalogueGroup, StoryGroup, StoryMap
from DerivedMap import SquadAssault, ChainChallengeGroup, ChainChallengeMap
from HB import BHBMap, LHBMap, GHBMap

SESSION = None

def exportMap(name: str, content: str):
    global SESSION
    if not SESSION:
        SESSION = util.fehBotLogin()

    try:
        result = SESSION.post(url=URL, data={
            "action": "edit",
            "title": name,
            "text": content,
            "createonly": True,
            "bot": True,
            "tags": "automated",
            "summary": "bot: new map",
            "watchlist": "nochange",
            "token": util.getToken(SESSION),
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

def main():
    if len(argv) < 2:
        print("Enter at least one map id")
        exit(0)

    #S = util.fehBotLogin()
    for arg in argv:
        if arg == argv[0]:
            continue

        if "MID_STAGE_"+arg in DATA:
            name = DATA["MID_STAGE_"+arg]
            if "MID_STAGE_HONOR_"+arg in DATA:
                name += ": " + DATA["MID_STAGE_HONOR_"+arg]
        elif "MID_STAGE_TITLE_"+arg in DATA:
            name = DATA["MID_STAGE_TITLE_"+arg]
        elif "MID_CHAPTER_" + arg in DATA:
            name = DATA["MID_CHAPTER_"+arg]
        elif arg[0] == "Q":
            name = DATA["MID_STAGE_OCCUPATION"] + ": " + DATA["MID_STAGE_HONOR_OCCUPATION"]
        elif not arg[0] == "H":
            print(ERROR + "Unknow map " + arg)
            continue

        if re.match(r"S\d{4}", arg):
            exportMap(name, StoryMap(arg))

        if re.match(r"C\d{4}", arg):
            exportGroup(StoryGroup(arg))

        elif re.match(r"X[X0-9]\d{3}", arg):
            exportMap(name, ParalogueMap(arg))

        elif re.match(r"CX\d{3}", arg):
            exportGroup(ParalogueGroup(arg))

        elif re.match(r"H\d{4}", arg):
            mapId = int(re.compile(r"H(\d+)").match(arg)[1])
            hero = util.getHeroName(mapId)
            if hero:
                exportMap("Heroic Ordeals: " + hero + "'s Trial", HOmap(arg))
            else:
                print(ERROR + "Unknow map: " + arg)

        elif re.match(r"P[ABC]\d{3}", arg):
            exportMap(name, TDmap(arg))


        elif re.match(r"T\d{4}", arg):
            if re.compile(r"\w & \w").search(name):
                exportGroup(BHBMap(arg))
            else:
                exportMap(name + " (map)", GHBMap(arg))

        elif re.match(r"L\d{4}", arg):
            exportMap(name + " (map)", LHBMap(arg))

        elif re.match(r"Q\d{4}", arg):
            print("RD map: " + name + " (" + str(int(arg.replace("Q", ""))) + ")")

        elif re.match(r"V\d{4}", arg): #TODO
            print(TODO + "Special map: " + name)


        elif re.match(r"SB_\d{4}", arg):
            exportMap(name, SquadAssault(arg))

        elif re.match(r"ST_S\d{4}", arg) or re.match(r"ST_X\d{4}", arg):
            exportMap("Chain Challenge: " + (arg[3] == 'S' and f"Book {util.ROMAN[int(arg[5]) or 1]}, " or '') + name,
                ChainChallengeMap(arg))

        elif re.match(r"ST_C\d{4}", arg) or re.match(r"ST_CX\d{3}", arg):
            exportGroup(ChainChallengeGroup(arg))

        elif re.compile(r"BG_(WATER|WIND|EARTH|FIRE)_\d{4}").match(arg): #TODO
            print("Blessed Garden: " + name)


        else:
            print(ERROR + "Unknow map " + arg)


if __name__ == "__main__":
    main()