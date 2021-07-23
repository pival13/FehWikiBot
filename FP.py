#! /usr/bin/env python3

from datetime import datetime
import json
from os.path import isfile
from num2words import num2words

import util
import mapUtil
from Reverse import reverseFrontlinePhalanx
from reward import parseReward

def FPInfobox(data: dict, nb: int):
    return "{{Frontline Phalanx Infobox\n" + \
        f"|image=Banner Encourage {data['id_tag']}.webp\n" + \
        f"|heroes={','.join([util.getName('PID_'+unit) for unit in data['heroes']])}\n" + \
        f"|bosses={','.join([util.getName('PID_'+unit) for unit in data['bosses']]) if data['bosses'].count(data['bosses'][0]) != len(data['bosses']) else util.getName('PID_'+data['bosses'][0])}\n" + \
        f"|startTime={data['avail']['start']}\n" + \
        f"|endTime={util.timeDiff(data['avail']['finish'])}\n" + \
        "|defeatTime=\n}}"

def FPRewards(data: dict):
    s = "==Rewards==\n===Daily rewards===\n{{#invoke:Reward/FrontlinePhalanx|daily\n"
    for i in range(len(data['daily_rewards'])):
        s += f" |{i+1}=" + parseReward(data['daily_rewards'][i]['rewards']) + "\n"
    s += "}}\n===Boss rewards===\n{{#invoke:Reward/FrontlinePhalanx|bosses\n"
    for i in range(len(data['boss_rewards'])):
        s += f" |{i+1}=" + parseReward(data['boss_rewards'][i]['rewards']) + "\n"
    s += "}}\n===Rank rewards===\n{{#invoke:Reward/FrontlinePhalanx|rank\n"
    maxsize = len(str(data['rank_rewards'][-1]['rank_hi']))
    for rank in data['rank_rewards']:
        ranks = "{{:>{}}}~{{:>{}}}".format(maxsize, maxsize).format(rank['rank_hi'], rank['rank_lo'] if rank['rank_lo'] != -1 else "")
        s += f" |{ranks}=" + parseReward(rank['rewards']) + "\n"
    return s + "}}"

def FrontlinePhalanx(tag: str):
    datas = reverseFrontlinePhalanx(tag)

    ret = {}
    for data in datas:
        nb = int(util.cargoQuery('FrontlinePhalanx', 'COUNT(DISTINCT _pageName)=Nb')[0]['Nb']) + 1
        s = FPInfobox(data, nb) + "\n"
        s += f"The {num2words(nb, to='ordinal')} [[Frontline Phalanx]] event." + "\n"
        s += mapUtil.Availability(data['avail'], f"Frontline Phalanx ({datetime.strptime(data['avail']['start'], util.TIME_FORMAT).strftime('%b %Y')}) (Notification)", "[[Frontline Phalanx]] event") + "\n"
        s += "<!--** However, it actually ended at {{HT|}} with the defeat of the third boss.-->\n"
        s += FPRewards(data) + "\n"
        s += "==Trivia==\n*\n{{Main Events Navbox}}"
        ret[f"Frontline Phalanx {nb}"] = s
    return ret

from sys import argv

if __name__ == '__main__':
    if len(argv) <= 1:
        print("Enter at least one update tag")
        exit(1)
    for arg in argv[1:]:
        if not isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Encourage/' + arg + '.bin.lz'):
            print(f'No Frontline Phalanx are related to the tag "{arg}"')
            continue
        FPs = FrontlinePhalanx(arg)
        for FP in FPs:
            print(FP, FPs[FP])