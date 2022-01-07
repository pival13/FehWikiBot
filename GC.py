#! /usr/bin/env python3

from datetime import datetime
from os.path import isfile
import re

import util
import mapUtil
from scenario import Story
from Reverse import reverseGrandConquests
from reward import parseReward
from wikiUtil import exportSeveralPages, getPageContent
from redirect import redirect
import GCWorld
from uploadImage import exportImage

BONUS = {
    '歩行能力強化': 'Infantry Boost',
    '歩行奥義': 'Infantry Special',
    '重装能力強化': 'Armored Boost',
    '重装移動強化': 'Armored Move',
    '騎馬能力強化': 'Cavalry Boost',
    '騎馬追撃': 'Cavalry Attack',
    '飛行能力強化': 'Flying Boost',
    '飛行先導': 'Flying Warp',
}

def GCInfobox(data: dict, nb: int):
    return "{{Grand Conquests Infobox\n" + \
        f"|number={nb}\n" + \
        f"|red={util.getName('PID_'+data['leaders'][0])}\n" +\
        f"|blue={util.getName('PID_'+data['leaders'][1])}\n" +\
        f"|green={util.getName('PID_'+data['leaders'][2])}\n" + \
        f"|startTime={data['battles'][0]['avail']['start']}\n" + \
        f"|endTime={util.timeDiff(data['event_avail']['finish'])}\n" + \
        '}}'

def GCRewards(data: dict):
    s = "==Rewards==\n===Tier===\n"
    s += "{{Hatnote|See [[Grand Conquests#Rewards]] for details on Grand Conquests Tiers and levelling up.}}\n"
    s += "{{#invoke:Reward/GrandConquests|tier\n"
    for reward in data['rewards']:
        if reward['type'] == 1:
            s += f" |{reward['lower_bound']}=" + parseReward(reward['reward']) + "\n"
    s += "}}\n===Score===\nThe same items are rewarded in all three battles.\n"
    s += "{{#invoke:Reward/GrandConquests|score|time="+data['battles'][0]['avail']['start']+"\n"
    rewards = {}
    for reward in data['rewards']:
        if reward['type'] == 4 and not reward['lower_bound'] in rewards:
            score = str(reward['lower_bound']) + (('~' + (str(reward['upper_bound']) if reward['upper_bound'] != -1 else '')) if reward['lower_bound'] != reward['upper_bound'] else '')
            s += f" |{score}=" + parseReward(reward['reward']) + "\n"
            rewards[reward['lower_bound']] = reward['reward']
        elif reward['type'] == 4 and reward['lower_bound'] in rewards and rewards[reward['lower_bound']] != reward['reward']:
            raise Exception('Inconsistent rewards between rounds')
    s += "}}\n===Rank===\nThe same items are rewarded in all three battles.\n"
    s += "{{#invoke:Reward/GrandConquests|rank|time="+data['battles'][0]['avail']['start']+"\n"
    rewards = {}
    for reward in data['rewards']:
        if reward['type'] == 3 and not reward['lower_bound'] in rewards:
            score = str(reward['upper_bound']) + (('~' + (str(reward['lower_bound']) if reward['lower_bound'] != -1 else '')) if reward['lower_bound'] != reward['upper_bound'] else '')
            s += f" |{score}=" + parseReward(reward['reward']) + "\n"
            rewards[reward['lower_bound']] = reward['reward']
        elif reward['type'] == 3 and reward['lower_bound'] in rewards and rewards[reward['lower_bound']] != reward['reward']:
            raise Exception('Inconsistent rewards between rounds')
    return s + "}}"

def GCAreas(data: dict):
    areas = [util.readFehData('Common/Occupation/World/'+data['battles'][i]['world_id']+'.json') for i in range(3)]
    getArea = lambda ibattle, iarea: [area for area in areas[ibattle]['areas'] if area['area_no'] == iarea][0]
    s = '==Areas==\n{| class="wikitable sortable" style="text-align:center;"\n'
    s += '!rowspan="2"|Area\n!rowspan="2"|Map\n!colspan="3"|Area effect\n|-\n!Battle 1\n!Battle 2\n!Battle 3\n'
    for i in range(areas[0]['area_count']):
        area = getArea(0, i+1)
        s += f"|-\n|{i+1}\n"
        s += '|' + mapUtil.MapImage({'id': area['map_id'], 'base_terrain': 'normal', 'terrain': [['']*8]*10}, True).replace('\n|','\n |') + '\n'
        for j in range(3):
            s += '|'
            area = getArea(j, i+1)
            if area['is_base']:
                s += f"'''{re.sub(': .*','',util.getName('PID_'+data['leaders'][area['army']]))}'s HQ'''\n"
                continue
            for bonus in area['area_bonuses']:
                if bonus:
                    s += f"{{{{GCAreaEffect|This Area|{BONUS[bonus]}}}}}"
            if area['adjacent_area_bonus']:
                s += f"{{{{GCAreaEffect|Adjacent Allied Areas|{BONUS[area['adjacent_area_bonus']]}}}}}"
            else:
                for adjacentArea in [getArea(j, otherArea) for otherArea in area['neighbours']]:
                    if adjacentArea['adjacent_area_bonus']:
                        s += f"{{{{GCAreaEffect|from Adjacent Allied Area|{BONUS[adjacentArea['adjacent_area_bonus']]}}}}}"
                        break
            s += '\n'
    return s + '|}'

def GrandConquests(tag: str):
    datas = reverseGrandConquests(tag)

    ret = {}
    for data in datas:
        nb = int(util.cargoQuery('GrandConquests', 'COUNT(DISTINCT _pageName)=Nb')[0]['Nb']) #+ 1
        s = GCInfobox(data, nb) + "\n"
        s += GCRewards(data) + "\n"
        s += GCAreas(data) + "\n"
        s += Story('DAISEIATSU'+data['id_tag']).replace('Opening', util.getName('MID_OCCUPATION_RECOLLECTION_TITLE_'+data['id_tag']))
        s += "==Trivia==\n*\n{{Main Events Navbox}}"
        ret[f"Grand Conquests {nb}"] = s
    return ret

def uploadGrandConquestWorld(tag: str):
    datas = reverseGrandConquests(tag)
    for data in datas:
        res = util.cargoQuery('GrandConquests', 'Number', f"StartTime={data['battles'][0]['avail']['start']}", limit=1)
        if len(res) == 0:
            res = util.cargoQuery('GrandConquests', 'COUNT(_pageName)=Number')
        world = GCWorld.GCDefaultWorld(data['str1'], data['battles'][0]['world_id'])
        exportImage(f"File:Grand Conquests {res[0]['Number']} Area.png", world, '[[Category:Grand Conquests overworld map files]]', 'Bot: Grand Conquests areas', True)
        if not getPageContent(f"File:Grand Conquests {res[0]['Number']} Map.png")[f"File:Grand Conquests {res[0]['Number']} Map.png"]:
            redirect(f"File:Grand Conquests {res[0]['Number']} Map.png", f"File:GC {data['world']}.webp")

from sys import argv

if __name__ == '__main__':
    if len(argv) <= 1:
        print("Enter at least one update tag")
        exit(1)
    for arg in argv[1:]:
        if not isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Occupation/Data/' + arg + '.bin.lz'):
            print(f'No Grand Conquests are related to the tag "{arg}"')
            continue
        GCs = GrandConquests(arg)
        #uploadGrandConquestWorld(arg)
        #exportSeveralPages(GCs, create=False, minor=True)
        for GC in GCs:
            print(GC, GCs[GC])
