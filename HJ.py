#! /usr/bin/env python3

from datetime import datetime
from os.path import isfile

import util
from Reverse import reverseHeroesJourney
from reward import parseReward

def HJInfobox(data: dict):
    return "{{Heroes Journey Infobox\n" + \
        f"|memento={';'.join([util.getName('MID_'+memento['id_tag']+'_Title') for memento in data['memento_event']])}\n" + \
        f"|startTime={data['avail']['start']}\n" + \
        f"|endTime={util.timeDiff(data['avail']['finish'])}\n" + \
        "}}"

def HJAvailability(data: dict):
    s = "==Availability==\nThis [[Heroes Journey]] event was made available:\n" + \
        f"* {{{{HT|{data['avail']['start']}}}}} — {{{{HT|{util.timeDiff(data['avail']['finish'])}}}}} " + \
        f"([[Heroes Journey Has Begun ({datetime.strptime(data['avail']['start'], util.TIME_FORMAT).strftime('%b %Y')}) (Notification)|Notification]])"
    return s

def HJRewards(data: dict):
    s = "==Rewards==\n===Battle rewards===\n{{#invoke:Reward/HeroesJourney|battle\n"
    for stage in data['stages']:
        s += f" |{util.getName('MID_JOURNEY_STAGE_LEVEL'+str(stage['difficulty']))}="
        if stage['base_memento'] > 0:
            stage['reward'] = [{'kind': 'Memento Points', 'count': f"{stage['base_memento']}~"}] + (stage['reward'] or [])
        s += parseReward(stage['reward']) + "\n"
    s += "}}\n===Rapport rewards===\n{{#invoke:Reward/HeroesJourney|rapport\n"
    for r in data['rewards']:
        s += f" |{r['points']}=" + parseReward(r['reward']) + "\n"
    return s + "}}"

def HeroesJourney(tag: str):
    datas = reverseHeroesJourney(tag)

    ret = {}
    for data in datas:
        nb = int(util.cargoQuery('HeroesJourney', 'COUNT(DISTINCT _pageName)=Nb')[0]['Nb']) + 1
        s = HJInfobox(data) + "\n"
        s += HJAvailability(data) + "\n"
        s += HJRewards(data) + "\n"
        s += "==Memento events==\n"
        s += "==Trivia==\n*\n{{Main Events Navbox}}"
        ret[f"Heroes Journey {nb}"] = s
    return ret

from sys import argv

if __name__ == '__main__':
    if len(argv) <= 1:
        print("Enter at least one update tag")
        exit(1)
    for arg in argv[1:]:
        if not isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Journey/Terms/' + arg + '.bin.lz'):
            print(f'No Heroes Journey are related to the tag "{arg}"')
            continue
        hjs = HeroesJourney(arg)
        for hj in hjs:
            print(hj, hjs[hj])