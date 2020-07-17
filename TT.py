#! /usr/bin/env python3

from datetime import datetime
import json
import re

from util import DATA, DIFFICULTIES
import util
import mapUtil
from scenario import Story
from HB import getHeroWithName
from reward import MOVE
import Reverse

TT_DIFFICULTIES = ["Normal/LV.8/3 battles","Normal/LV.14/3 battles","Normal/LV.20/3 battles","Hard/LV.25/4 battles","Hard/LV.30/5 battles","Lunatic/LV.35/5 battles","Lunatic/LV.40/7 battles"]

def getTTTag(mapId: str):
    return util.askFor(r"\d+_\w+", f"Which update is this TT related to ({mapId})?")

def TTInfobox():
    return ""

def TTMapInfobox(StageEvent: dict, SRPGMap: dict, tag: str):
    name = util.getName('MID_SEQUENTIAL_MAP_TERM_' + "20"+tag[:tag.find('_')][:4])#TODO
    SRPGMap['field']['player_pos'] = SRPGMap['player_pos']
    SRPGMap['field']['enemy_pos'] = [unit['pos'] for unit in SRPGMap['units']]
    SRPGMap['field']['enemy_pos'][0] = {}
    info = {
        'banner': 'Banner ' + name + '.png',
        'mapName': name,
        'group': 'Tempest Trials',
        'map': SRPGMap['field'],
        'lvl': {'Normal': '8{{RarityStar|2}}/14{{RarityStar|2}}/20{{RarityStar|3}}',
                'Hard': '25{{RarityStar|3}}/30{{RarityStar|4}}',
                'Lunatic': '35{{RarityStar|4}}/40{{RarityStar|5}}'},
        'rarity': {'Normal': '', 'Hard': '', 'Lunatic': ''},
        'stam': {'Normal': '10', 'Hard': '12/15', 'Lunatic': '15'},
        'bgm': '','bgm2': '',
    }
    return mapUtil.MapInfobox(info, True).replace("reward={\n}", "reward={{Score Reward|rewardNormal=25/30/35|rewardHard=35|rewardLunatic=40}}")

def TTUnitData(SRPGMaps: list):
    s = "==Unit data==\n"
    s += "{{#invoke:UnitData|main\n"
    regex = re.compile(r"\{unit=([^;]+);([^}]*;slot=[^1;]+[^}]*);stats=[^}]*;(ai=[^;]+);\};")

    for idiff in range(len(SRPGMaps)):
        randomUnit = []
        tmp = mapUtil.UnitData(SRPGMaps[idiff])
        toRep = regex.findall(tmp)
        for repSeq in toRep:
            randomUnit += [{
                'move': ("Armored" if repSeq[0].find('Knight') != -1 else
                        "Cavalry" if repSeq[0].find('Cavalier') != -1 or repSeq[0].find('Troubadour') != -1 else
                        "Flying" if repSeq[0].find('Flier') != -1 or repSeq[0].find('Dragon') != -1 or repSeq[0].find('Fáfnir') != -1 else
                        "Infantry"),
                'weapon': "Close" if repSeq[0].find('Sword') != -1 or repSeq[0].find('Lance') != -1 or repSeq[0].find('Axe') != -1 or repSeq[0].find('Fáfnir') != -1 or repSeq[0].find('Manakete') != -1 else
                          "Ranged",
                'staff': 1 if repSeq[0] == 'Cleric' or repSeq[0] == 'Troubadour' else 0,
            }]
            tmp = regex.sub(f"{{{repSeq[1]};{repSeq[2]};random={{moves={randomUnit[-1]['move']};weapons={randomUnit[-1]['weapon']}" +\
                            (";staff=true" if randomUnit[-1]['staff'] and randomUnit[-1]['weapon'] == 'Ranged' else
                             ";staff=false" if randomUnit[-1]['weapon'] == 'Ranged' else "") + "};};",
                            tmp, 1)

        s += "|" + TT_DIFFICULTIES[idiff] + "=" + tmp + "\n"
    s += "}}\n"

    boss = getHeroWithName(re.search(r'unit=([^;]+);', tmp)[1])
    s += "===Randomized units===\nThe other enemy units are selected randomly from the below pool of Heroes:\n"
    for i in range(len(randomUnit)):
        s += f"====Enemy {i+2}: {randomUnit[i]['weapon']} {randomUnit[i]['move'].lower()} unit====\n"
        s += f"{{{{RandomTTUnits|WeaponClass={randomUnit[i]['weapon']}|MoveType={randomUnit[i]['move']}|Date=" +\
            (f"|boss={util.getName(boss['id_tag'])}" if boss['regular_hero'] and MOVE[boss['move_type']] == randomUnit[i]['move'] else "") +\
            ("|NoStave=1" if randomUnit[i]['weapon'] == 'Ranged' and randomUnit[-1]['staff'] == 0 else '') + "}}\n" #TODO Date
        #{{RandomTTUnits|WeaponClass=|MoveType=|Date=|boss=|NoStaves=}}

    return s

def TTMap(mapId: str):
    tag = "200701_summer" or getTTTag(mapId)
    StageEvent = {}#util.fetchFehData("Common/SRPG/StageEvent")[mapId]
    SRPGMaps = [util.readFehData('Common/SRPGMap/'+argv[1]+c+'.json') for c in ['A','B','C','D','E','F','G']]
    name = util.getName('MID_SEQUENTIAL_MAP_TERM_' + "20"+tag[:tag.find('_')][:4])#TODO

    SRPGMaps[-1]['field'].update({'player_pos': SRPGMaps[-1]['player_pos'], 'enemy_pos': [SRPGMaps[-1]['units'][i]['pos'] for i in range(len(SRPGMaps[-1]['units']))]})
    SRPGMaps[-1]['field']['enemy_pos'][0] = {}

    content = '{| style="float:right"\n|'
    content += TTInfobox() + '\n|-\n|'
    content += TTMapInfobox(StageEvent, SRPGMaps[-1], tag) + "|}\n"
    content += mapUtil.MapAvailability({}, f"Tempest Trials+: {name} (Notification)",)
    #content += TTRewards()
    content += TTUnitData(SRPGMaps)
    content += Story("SENKA" + "20"+tag[:4])#TODO
    content += "==Trivia==\n*\n"
    content += mapUtil.InOtherLanguage(["MID_SEQUENTIAL_MAP_TERM_"+"20"+tag[:4]])#TODO
    content += "{{Main Events Navbox}}"

    return content

from sys import argv

if __name__ == '__main__':
    if len(argv) != 2 or len(argv[1]) != 5:
        exit(0)
    print(TTMap(argv[1]))
