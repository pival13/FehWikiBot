#! /usr/bin/env python3

import json
import re

from util import DATA, DIFFICULTIES
import util
import mapUtil
from scenario import Story
from HB import getHeroWithName
from reward import MOVE, parseReward
from Reverse import reverseFile

TT_DIFFICULTIES = ["Normal/LV.8/3 battles","Normal/LV.14/3 battles","Normal/LV.20/3 battles","Hard/LV.25/4 battles","Hard/LV.30/5 battles","Lunatic/LV.35/5 battles","Lunatic/LV.40/7 battles"]

def getTTTag(mapId: str):
    return util.askFor(r"\d+_\w+", f"Which update is this TT related to ({mapId})?")

def TTInfobox(StageEvent: str):
    name = util.getName('MID_SEQUENTIAL_MAP_TERM_' + StageEvent['id_tag'])
    heroes = StageEvent['units1']['units'] + StageEvent['units2']['units']
    rewardsHeroes = []
    for rewards in StageEvent['score_rewards']:
        for reward in rewards['rewards']:
            if reward['kind'] == 1 and not reward['id_tag'] in rewardsHeroes:
                rewardsHeroes += [reward['id_tag']]
    mapIds = []
    maps = []
    for sets in StageEvent['sets']:
        for battle in sets['battles'][:-1]:
            mapIds += [m[:-1] for m in battle['maps'] if not m[:-1] in mapIds]
    for mapId in mapIds:
        if mapId[0] == 'S':
            values = [1,2,3,4,5]
            s = ('[[Story Maps#' + util.getName('C00' + mapId[1:-2]) + '|Book I, ' + util.getName('C00' + mapId[1:-2])) if mapId[1] in '01' else \
                ('[[Story Maps#' + re.sub('Book [^,]+, ', '', util.getName('C0' + mapId[1:-1])) + '|' + util.getName('C0' + mapId[1:-1]))
            for i in values:
                if mapIds.count(mapId[0:-1]+str(i)): mapIds.remove(mapId[0:-1]+str(i))
                else: values.remove(i)
            if len(values) != 5:
                s += ' (Maps ' + ' & '.join([str(v) for v in values]).replace(' & ', ', ', len(values)-2) + ')'
            maps += [s + ']]']
        elif mapId[0] == 'X' and mapId[1] != 'X':
            values = [1,2,3]
            s = '[[Paralogue Maps#' + util.getName('CX' + mapId[1:-1]) + '|' + util.getName('CX' + mapId[1:-1])
            for i in values:
                if mapIds.count(mapId[0:-1]+str(i)): mapIds.remove(mapId[0:-1]+str(i))
                else: values.remove(i)
            if len(values) != 3:
                s += ' (Maps ' + ' & '.join([str(v) for v in values]) + ')'
            maps += [s + ']]']
        else:
            maps += ['[[' + util.getName(mapId) + ']]']

    return "{{Tempest Trials Infobox\n|name=" + name + '\n' + \
        "|promoArt=Tempest_Trials_" + util.cleanStr(name).replace(' ', '_') + '_2.jpg\n' + \
        "|rewardHeroes=" + ','.join([util.getName(hero) for hero in rewardsHeroes]) + '\n' + \
        "|bonusHeroes=" + ','.join([util.getName(hero) for hero in heroes]) + '\n' + \
        "|startTime=" + StageEvent['avail']['start'] + '\n' + \
        "|endTime=" + util.timeDiff(StageEvent['avail']['finish']) + '\n' + \
        "|maps=" + ' &<br>'.join(maps).replace(' &', ',', len(maps)-2) + '\n' + \
        "}}\n"

def TTMapInfobox(StageEvent: dict, SRPGMap: dict):
    name = util.getName('MID_SEQUENTIAL_MAP_TERM_' + StageEvent['id_tag'])
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
        'bgms': util.getBgm(SRPGMap['field']['id'])
    }
    return mapUtil.MapInfobox(info, True).replace("reward={\n}", "reward={{Score Reward|rewardNormal=25/30/35|rewardHard=35|rewardLunatic=40}}")

def TTRewards(StageEvent: dict):
    s = "==Rewards==\n{{#invoke:Reward/TempestTrials|score\n"
    for rewards in StageEvent['score_rewards']:
        s += f"|{rewards['score']}=" + parseReward(rewards['rewards']) + '\n'
    s += '}}\n===Rank rewards===\n{{#invoke:Reward/TempestTrials|rank|time=\n'
    for rewards in StageEvent['rank_rewards']:
        s += f"|{rewards['rank_hi']:6}~{rewards['rank_lo']:6}=" + parseReward(rewards['rewards']) + '\n'
    return s + '}}\n'

def TTUnitData(SRPGMaps: list, startTime: str):
    s = "==Unit data==\n"
    s += "{{#invoke:UnitData|main\n"
    regex = re.compile(r"\{unit=([^;]+);([^}]*;slot=[^1;]+[^}]*);stats=[^}]*;(ai=[^}]+\});\};")

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
                            (";staff=1" if randomUnit[-1]['staff'] and randomUnit[-1]['weapon'] == 'Ranged' else
                             ";staff=0" if randomUnit[-1]['weapon'] == 'Ranged' else "") + "};};",
                            tmp, 1)

        s += "|" + TT_DIFFICULTIES[idiff] + "=" + tmp + "\n"
    s += "}}\n"

    boss = getHeroWithName(re.search(r'unit=([^;]+);', tmp)[1])
    s += "===Randomized units===\nThe other enemy units are selected randomly from the below pool of Heroes:\n"
    for i in range(len(randomUnit)):
        s += f"====Enemy {i+2}: {randomUnit[i]['weapon']} {randomUnit[i]['move'].lower()} unit====\n"
        s += f"{{{{RandomTTUnits|WeaponClass={randomUnit[i]['weapon']}|MoveType={randomUnit[i]['move']}|Date=" + startTime[:10] +\
            (f"|boss={util.getName(boss['id_tag'])}" if 'regular_hero' in boss and boss['regular_hero'] and MOVE[boss['move_type']] == randomUnit[i]['move'] else "") +\
            ("|NoStaves=1" if randomUnit[i]['weapon'] == 'Ranged' and randomUnit[-1]['staff'] == 0 else '') + "}}\n"

    return s

def TTContent(StageEvent: dict):
    SRPGMaps = [util.readFehData('Common/SRPGMap/'+ sets['battles'][-1]['maps'][0] +'.json') for sets in StageEvent['sets']]

    SRPGMaps[-1]['field'].update({'player_pos': SRPGMaps[-1]['player_pos'], 'enemy_pos': [SRPGMaps[-1]['units'][i]['pos'] for i in range(len(SRPGMaps[-1]['units']))]})
    SRPGMaps[-1]['field']['enemy_pos'][0] = {}

    content = '{| style="float:right"\n|'
    content += TTInfobox(StageEvent) + '|-\n|'
    content += TTMapInfobox(StageEvent, SRPGMaps[-1]) + "|}\n"
    content += mapUtil.MapAvailability(StageEvent['avail'], f"Tempest Trials+: {util.getName('MID_SEQUENTIAL_MAP_TERM_' + StageEvent['id_tag'])} (Notification)", '[[Tempest Trials]]')
    content += TTRewards(StageEvent)
    content += TTUnitData(SRPGMaps, StageEvent['avail']['start'])
    content += Story(StageEvent['full_id_tag'])
    content += "==Trivia==\n*\n"
    content += mapUtil.InOtherLanguage(["MID_SEQUENTIAL_MAP_TERM_"+StageEvent['id_tag']])
    content += "{{Main Events Navbox}}"

    return content

def TempestTrials(mapTagId: str) -> dict:
    if re.match(r'W\d{4}', mapTagId):
        tagId = getTTTag(mapTagId)
    elif re.match(r'\d+_\w+', mapTagId):
        tagId = mapTagId
    
    datas = reverseFile(util.BINLZ_ASSETS_DIR_PATH + 'Common/SRPG/SequentialMap/' + tagId + '.bin.lz')
    content = {}
    for data in datas:
        if re.match(r'W\d{4}', mapTagId) and data['sets'][0]['battles'][-1]['maps'][0][:-1] != mapTagId:
            continue
        content[util.getName('MID_SEQUENTIAL_MAP_TERM_' + data['id_tag'])] = TTContent(data)
    return content

from sys import argv

if __name__ == '__main__':
    for arg in argv[1:]:
        if re.match(r'W\d{4}', arg) or re.match(r'\d+_\w+', arg):
            print(TempestTrials(arg))
        else:
            print("Either a mapId (W\\d{4}) or a tagId (\\d+_\\w+) is expected")
