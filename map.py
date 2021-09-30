#! /usr/bin/env python3

from os.path import isfile
import json
import re

import util
from globals import TODO, ERROR, DATA
from wikiUtil import exportPage, exportSeveralPages

from StoryParalogue import StoryMap, StoryGroup, ParalogueMap, ParalogueGroup, UpdateStoryParalogueList
from TD import TacticsDrills
from HO import HeroicOrdeals
from DerivedMap import SquadAssault, ChainChallengeMap, ChainChallengeGroup

from HB import GrandHeroBattle, BoundHeroBattle, LegendaryHeroBattle, LimitedHeroBattle, RevivalHeroBattle
from RD import RivalDomains
from EventMap import exportEventMap

#from VG import VotingGauntlet
from TT import TempestTrials
from TB import TapBattle, EncoreTapBattle
#from GC import GrandConquest
from FB import exportForgingBonds
from RS import RokkrSieges
from LL import LostLore
from HoF import HallOfForms
from MS import MjolnirsStrike
from FP import FrontlinePhalanx
from PoL import PawnsOfLoki
from HJ import HeroesJourney

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
    elif not mapId[0] in ["H", "I"] and not re.fullmatch(r"V\d{4}-V\d{4}", mapId):
        print(ERROR + "Unknow map " + mapId)
        return

    if re.match(r"S\d{4}", mapId):
        exportPage(name, StoryMap(mapId), 'Bot: new Story Map', create=True)

    if re.match(r"C\d{4}", mapId):
        exportSeveralPages(StoryGroup(mapId), 'Bot: new Story Map', create=True)
        exportSeveralPages(UpdateStoryParalogueList(mapId), 'Bot: ' + util.getName(mapId))

    elif re.match(r"X[X0-9]\d{3}", mapId):
        exportPage(name, ParalogueMap(mapId), 'Bot: new Paralogue Map', create=True)

    elif re.match(r"CX\d{3}", mapId):
        exportSeveralPages(ParalogueGroup(mapId), 'Bot: new Paralogue Map', create=True)
        exportSeveralPages(UpdateStoryParalogueList(mapId), 'Bot: ' + util.getName(mapId))

    elif re.match(r"H\d{4}", mapId):
        nb = int(re.match(r"H(\d+)", mapId)[1])
        heroes = util.fetchFehData("Common/SRPG/Person", 'id_num')
        if nb in heroes:
            exportPage("Heroic Ordeals: " + util.getName(heroes[nb]['id_tag']) + "'s Trial", HeroicOrdeals(mapId), 'Bot: new Heroic Ordeals', create=True)
        else:
            print(ERROR + "Unknow map: " + mapId)

    elif re.match(r"P[ABC]\d{3}", mapId):
        exportPage(name, TacticsDrills(mapId), 'Bot: new Tactics Drills', create=True)


    elif re.match(r"T\d{4}", mapId):
        if re.match(r"\w{1,2} & \w{1,2}", name):
            exportSeveralPages(BoundHeroBattle(mapId), 'Bot: new Bound Hero Battle', create=True)
        else:
            exportPage(name + " (map)", GrandHeroBattle(mapId), 'Bot: new Grand Hero Battle', create=True)

    elif re.match(r"L\d{4}", mapId):
        content = LegendaryHeroBattle(mapId)
        isMythic = content.find("Mythic Hero Battle") != -1
        exportPage(name + " (map)", content, 'Bot: new Legendary Hero Battle' if not isMythic else 'Bot: new Mythic Hero Battle', create=True)

    elif re.match(r"Q\d{4}", mapId):
        exportPage(name + f" ({int(mapId[1:])})", RivalDomains(mapId), 'Bot: new Rival Domains', create=True)
        print(TODO + "Edit Grand Conquests Trivia")

    elif re.match(r"V\d{4}-V\d{4}", mapId):
        exportEventMap(mapId[:5], mapId[-5:])

    elif re.match(r"V\d{4}", mapId):
        exportEventMap(mapId)

    elif re.match(r"I\d{4}", mapId):
        exportSeveralPages(LimitedHeroBattle(mapId), 'Bot: new Limited Hero Battle', create=False)


    elif re.match(r"SB_\d{4}", mapId):
        exportPage(name, SquadAssault(mapId), 'Bot: new Squad Assault', create=True)

    elif re.match(r"ST_S\d{4}", mapId) or re.match(r"ST_X\d{4}", mapId):
        name = "Chain Challenge: " + (f"Book {util.ROMAN[int(mapId[5]) or 1]}, " if mapId[3] == 'S' else '') + name
        exportPage(name, ChainChallengeMap(mapId), 'Bot: new Chain Challenge', create=True)

    elif re.match(r"ST_C\d{4}", mapId) or re.match(r"ST_CX\d{3}", mapId):
        exportSeveralPages(ChainChallengeGroup(mapId), 'Bot: new Chain Challenge', create=True)

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
        try:
            parseMapId(f"H{stage['id_num']:04}")
        except:
            print(ERROR + "Failed to parse " + f"H{stage['id_num']:04}")
    for Stages in [StagePuzzle, StageScenario, StageEvent, StageBG, StageSA, StageCCS, StageCCX]:
        for stage in Stages:
            try:
                parseMapId(stage['id_tag'])
            except:
                print(ERROR + "Failed to parse " + stage['id_tag'])
    findEvents(tag)
    findUpcoming()

from datetime import datetime
from mapUtil import MapAvailability

def findEvents(tag: str):
    lastTBRevival = 9#Here to change
    lastTB = 20#Here to change

    #if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Tournament' + tag + '.bin.lz'): print(TODO + "New Voting Gauntlet")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + f'Common/TapAction/TapBattleData/TDID_{lastTB+1:04}.bin.lz'):
        print(TODO + "New Tap Battle")
        with open(__file__, 'r') as f: __file__Content = f.read()
        with open(__file__, 'w') as f: f.write(re.sub(r"lastTB = \d+#Here to change", f"lastTB = {lastTB+1}#Here to change", __file__Content))
    if isfile(util.BINLZ_ASSETS_DIR_PATH + f'Common/TapAction/TapBattleData/TDID_{lastTBRevival+1:04}_01.bin.lz'):
        try:
            exportPage(util.getName(f'MID_TAP_BATTLE_DATA_TITLE_{lastTBRevival+1:04}'), EncoreTapBattle(lastTBRevival+1), 'Bot: Encore Tap Battle', create=False)
            with open(__file__, 'r') as f: __file__Content = f.read()
            with open(__file__, 'w') as f: f.write(re.sub(r"lastTBRevival = \d+#Here to change", f"lastTBRevival = {lastTBRevival+1}#Here to change", __file__Content))
        except: print(TODO + "Encore Tap Battle")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/SRPG/SequentialMap/' + tag + '.bin.lz'):
        try: exportSeveralPages(TempestTrials(tag), 'Bot: new Tempest Trials', create=True)
        except: print(TODO + "Tempest Trials")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Occupation/Data/' + tag + '.bin.lz'): print(TODO + "New Grand Conquests")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Portrait/' + tag + '.bin.lz'):
        try: exportForgingBonds(tag)
        except: print(TODO + "Forging Bonds")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Shadow/' + tag + '.bin.lz'):
        try: exportSeveralPages(RokkrSieges(tag), 'Bot: new Rokkr Sieges', create=True)
        except: print(TODO + "Rokkr Sieges")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Trip/Terms/' + tag + '.bin.lz'):
        try: exportSeveralPages(LostLore(tag), 'Bot: new Lost Lore', create=True)
        except: print(TODO + "Lost Lore")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/SRPG/IdolTower/' + tag + '.bin.lz'):
        try: exportSeveralPages(HallOfForms(tag), 'Bot: new Hall of Forms', create=True)
        except: print(TODO + "Hall of Form")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Mjolnir/BattleData/' + tag + '.bin.lz'):
        try: exportSeveralPages(MjolnirsStrike(tag), 'Bot: new Mjölnir\'s Strike', create=True)
        except: print(TODO + "Mjölnir's Strike")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Encourage/' + tag + '.bin.lz'):
        try: exportSeveralPages(FrontlinePhalanx(tag), 'Bot: new Frontline Phalanx', create=True)
        except: print(TODO + "Frontline Phalanx")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/SRPG/BoardGame/' + tag + '.bin.lz'):
        try: exportSeveralPages(PawnsOfLoki(tag), 'Bot: new Pawns of Loki', create=True)
        except: print(TODO + "Pawns of Loki")
    if isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Journey/Terms/' + tag + '.bin.lz'):
        try:  exportSeveralPages(HeroesJourney(tag), 'Bot: new Heroes Journey', create=True)
        except: print(TODO + 'New Heroes Journey')

def findUpcoming():
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent/", False)
    print('Upcoming special maps:')
    for stage in StageEvent:
        if datetime.strptime(stage['avail']['start'], util.TIME_FORMAT) > datetime.now():
            exportSeveralPages(RevivalHeroBattle(stage['id_tag']), 'Bot: new revival', minor=True, create=False)

def main(arg):
    if len(arg) < 2:
        print("Enter at least one map id")
        exit(0)
    elif len(arg) == 2 and re.match(r"\d+_\w+", arg[1]):
        parseTagUpdate(arg[1])
    elif len(arg) == 2 and arg[1] == 'upcoming':
        findUpcoming()
    else:
        for a in arg[1:]:
            try:
                parseMapId(a)
            except:
                print(ERROR + "Failed to parse map " + a)


from sys import argv
if __name__ == "__main__":
    main(argv)