#! /usr/bin/env python3

from datetime import datetime, timedelta
import json
from os.path import isfile
from num2words import num2words

from util import DATA, DIFFICULTIES
import util
from Reverse import reverseFile
from reward import parseReward

def MSInfobox(data: dict, nb: int):
    askrlv = util.askFor(r'\d+', f'What is the Askr Level on "Mjölnir\'s Strike {nb}" ?') or ""
    enemylv = util.askFor(r'\d+', f'What is the Enemy Level on "Mjölnir\'s Strike {nb}" ?') or ""
    return "{{Mjolnirs Strike Infobox\n" + \
        f"|image=Mjolnirs Strike {util.cleanStr(util.getName(data['unit_id']))}.jpg\n" + \
        "|mapImage={{MapLayout " + data['map_id'] + "}}\n" + \
        f"|startTime={data['shield_avail']['start']}\n" + \
        f"|endTime={util.timeDiff(data['event_avail']['finish'])}\n" + \
        f"|leader={util.getName(data['unit_id'])}\n" + \
        f"|bonusStructure={util.getName('MID_MF_'+data['bonus_structure'][:-1])}\n" + \
        f"|askrLV={askrlv}\n|strikeLV={enemylv}\n|askrScore=\n|strikeScore=\n|timesStronger=\n" + \
        "|season=" + ("LightDark" if data['season'] == 0 else 'DarkLight' if data['season'] == 1 else 'HeavenLogic' if data['season'] == 2 else 'LogicHeaven') + "\n}}"

def MSAvailability(data: dict, nb: int, isStart: bool):
    start = util.askAgreed(f"Does Mjölnir's Strike {nb} begin at {data['event_avail']['start']} ?", askNo='When does it begin ?', defaultTrue=data['event_avail']['start']) if isStart else data['event_avail']['start']
    notifTime = datetime.strptime(data['shield_avail']['start'], util.TIME_FORMAT) - timedelta(days=2)
    return "==Availability==\nThis [[Mjölnir's Strike]] event was made available:\n" + \
        f"* {{{{HT|{start}}}}} – {{{{HT|{util.timeDiff(data['event_avail']['finish'])}}}}} ([[Brace Yourselves - Mjölnir's Strike Begins ({notifTime.strftime('%b %d, %Y').replace(' 0', ' ')}) (Notification)|Notification]])\n" + \
        "** Brace Phase: {{HT|" + start + "}} – {{HT|" + util.timeDiff(data['shield_avail']['start']) + '}}\n' + \
        "** Shield Phase: {{HT|" + data['shield_avail']['start'] + "}} – {{HT|" + util.timeDiff(data['shield_avail']['finish']) + '}}\n' + \
        "** Counter Phase: {{HT|" + data['counter_avail']['start'] + "}} – {{HT|" + util.timeDiff(data['counter_avail']['finish']) + '}}'

def MSRewards(data: dict):
    rewardsTier = [r for r in data['rewards'] if r['kind'] == 2]
    rewardsLv = [r for r in data['rewards'] if r['kind'] == 1]
    
    s = "==Rewards==\n===Tier rewards===\n{{#invoke:Reward/MjolnirsStrike|tier\n"
    for r in rewardsTier:
        s += f" |{r['tier_hi']+1}=" + parseReward(r['reward']) + "\n"
    s += "}}\n===Askr LV. rewards===\n{{#invoke:Reward/MjolnirsStrike|askrLevel\n"
    for r in rewardsLv:
        s += f" |{r['tier_hi']+1}=" + parseReward(r['reward']) + "\n"
    return s + "}}"

def MjolnirsStrike(tag: str):
    datas = reverseFile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Mjolnir/BattleData/' + tag + '.bin.lz')

    ret = {}
    for data in datas:
        nb = int(data['id_tag'][2:])
        s = MSInfobox(data, nb) + "\n"
        s += f"The {num2words(nb, to='ordinal')} [[Mjölnir's Strike]] event." + "\n"
        s += MSAvailability(data, nb, data == datas[0]) + "\n"
        s += MSRewards(data) + "\n"
        s += "==Final results==\n{{MjolnirStrikeResults\n"
        for i in range(21):
            s += f"|askr{i+1}=|strike{i+1}=\n"
        s += "}}\n{{Main Events Navbox}}"
        ret[f"Mjölnir's Strike {nb}"] = s
    return ret

from sys import argv

if __name__ == '__main__':
    if len(argv) <= 1:
        print("Enter at least one update tag")
        exit(1)
    for arg in argv[1:]:
        if not isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Mjolnir/BattleData/' + arg + '.bin.lz'):
            print(f'No Mjölir\'s Strike are related to the tag "{arg}"')
            continue
        ms = MjolnirsStrike(arg)
        for m in ms:
            print(m, ms[m])