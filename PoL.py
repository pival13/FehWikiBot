#! /usr/bin/env python3

from datetime import datetime
import json
from os.path import isfile
from num2words import num2words

from util import DATA
import util
from Reverse import reverseFile
from reward import parseReward

WEAPON_CATEGORY = {
    0b000000000000000000000111: "Melee",
    0b000000000000000001111000: "Bow",
    0b000000000000011110000000: "Dagger",
    0b000000000111100000000000: "Magic",
    0b000000001000000000000000: "Staff",
    0b000011110000000000000000: "Dragonstone",
    0b111100000000000000000000: "Beast",
    
    0b000100010000100010001001: "Red",
    0b001000100001000100010010: "Blue",
    0b010001000010001000100100: "Green",
    0b100010001100010001000000: "Colorless",

    0b111111110000000000000111: "Close",
    0b000000001111111111111000: "Ranged",
    
    0b111100000000011111111111: "Physical",
    0b000011111111100000000000: "Magical",
    
    0b000000000000011111111000: "Missile",

    0b111111111111111111111111: "All",
    0b000000000000000000000000: "None",
}

def PoLInfobox(data: dict):
    bonus = []
    for i in range(data['nbRound']):
        mask = (int(data['rounds'][i]['weapons'], 2))
        nbonus = 0b111111111111111111111111 ^ mask
        bonus += ["{{Cwti|" + WEAPON_CATEGORY[nbonus] + "}}"]
    if len(bonus) == 1: bonus = bonus[0]
    else: bonus = "<br><!--\n-->".join([f"'''Round {i+1}''': {bonus[i]}" for i in range(len(bonus))])
    if bonus == "{{Cwti|None}}": bonus = "All"
    return "{{Pawns of Loki Infobox\n" + \
        f"|startTime={data['event_avail']['start']}\n" + \
        f"|endTime={util.timeDiff(data['event_avail']['finish'])}\n" + \
        "|bonus=" + bonus + "\n}}"

def PoLAvailability(data: dict):
    s = "==Availability==\nThis [[Pawns of Loki]] event was made available:\n" + \
        f"* {{{{HT|{data['event_avail']['start']}}}}} – {{{{HT|{util.timeDiff(data['event_avail']['finish'])}}}}} " + \
        f"([[Pawns of Loki Is Here! ({datetime.strptime(data['event_avail']['start'], util.TIME_FORMAT).strftime('%b %d, %Y').replace(' 0', ' ')}) (Notification)|Notification]])"
    if data['nbRound'] > 1:
        for r in range(data['nbRound']):
            s += f"\n** '''Round {r+1}''': " + \
                f"{{{{HT|{data['round_avails'][r]['start']}}}}} – " + \
                f"{{{{HT|{util.timeDiff(data['round_avails'][r]['finish'])}}}}}"
    return s

def PoLRewards(data: dict):
    s = "==Rewards==\n===Cumulative Points rewards===\n{{#invoke:Reward/PawnsOfLoki|points\n"
    length = len(str(data['score_rewards'][-1]['score']))
    for r in data['score_rewards']:
        score = "{{:<{}}}".format(length).format(r['score'])
        s += f" | {score} = " + parseReward(r['reward']) + "\n"
    s += "}}\n===Tier rewards===\n{{#invoke:Reward/PawnsOfLoki|tier\n"
    for r in data['tier_rewards']:
        s += f" |{r['tier']+1}=" + parseReward(r['reward']) + "\n"
    return s + "}}"

def PawnsOfLoki(tag: str):
    datas = reverseFile(util.BINLZ_ASSETS_DIR_PATH + 'Common/SRPG/BoardGame/' + tag + '.bin.lz')

    ret = {}
    for data in datas:
        nb = int(data['id_tag'][3:])
        s = PoLInfobox(data) + "\n"
        s += f"The {num2words(nb, to='ordinal')} [[Pawns of Loki]] event." + "\n"
        s += PoLAvailability(data) + "\n"
        s += PoLRewards(data) + "\n"
        s += "==Trivia==\n*\n{{Main Events Navbox}}"
        ret[f"Pawns of Loki {nb}"] = s
    return ret

from sys import argv

if __name__ == '__main__':
    if len(argv) <= 1:
        print("Enter at least one update tag")
        exit(1)
    for arg in argv[1:]:
        if not isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/SRPG/BoardGame/' + arg + '.bin.lz'):
            print(f'No Pawns of Loki are related to the tag "{arg}"')
            continue
        pols = PawnsOfLoki(arg)
        for pol in pols:
            print(pol, pols[pol])