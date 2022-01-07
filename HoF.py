#! /usr/bin/env python3

from os.path import isfile

import util
from globals import DATA
from Reverse import reverseHallOfForms
from reward import parseReward

def HoFInfobox(data: dict, nb: int):
    return "{{Hall of Forms Infobox\n" + \
        f"|number={nb}\n" + \
        f"|promoArt=Hall of Forms {nb}.jpg\n" + \
        f"|forma={','.join([util.getName(unit) for unit in data['forma']['heroes']])}\n" + \
        f"|startTime={data['avail']['start']}\n" + \
        f"|endTime={util.timeDiff(data['avail']['finish'])}\n}}}}"

def HoFRewards(data: dict):
    s = "==Rewards==\n===Daily rewards===\n{{#invoke:Reward/HallOfForms|daily\n"
    for i in range(len(data['daily_bonuses'])):
        s += f" |{i+1}=" + parseReward(data['daily_bonuses'][i]['reward']) + "\n"
    s += "}}\n===Chamber cleared===\n{{#invoke:Reward/HallOfForms|chambers\n"
    for chamber in data['chambers']:
        s += f" | {util.getName('MID_IDOL_TOWER_STAGE_'+chamber['id_tag'])} = " + parseReward(chamber['reward']) + "\n"
    return s + "}}"

def HallOfForms(tag: str):
    datas = reverseHallOfForms(tag)

    ret = {}
    for data in datas:
        nb = int(util.cargoQuery('HallOfForms', 'COUNT(_pageName)=Nb')[0]['Nb']) + 1
        s = HoFInfobox(data, nb) + "\n"
        s += HoFRewards(data) + "\n"
        s += "==Trivia==\n*\n{{Main Events Navbox}}"
        ret[f"Hall of Forms {nb}"] = s
    return ret

from sys import argv

if __name__ == '__main__':
    if len(argv) <= 1:
        print("Enter at least one update tag")
        exit(1)
    for arg in argv[1:]:
        if not isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/SRPG/IdolTower/' + arg + '.bin.lz'):
            print(f'No Hall of Forms are related to the tag "{arg}"')
            continue
        hofs = HallOfForms(arg)
        for hof in hofs:
            print(hof, hofs[hof])