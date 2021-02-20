#! /usr/bin/env python3

from datetime import datetime, timedelta
import json
import re

from util import DATA
import util
import mapUtil
from scenario import Conversation, StoryNavBar
from reward import parseReward
from Reverse import reverseFile

COLORS = ['Red', 'Orange', 'Green', 'Blue']

def FBInfobox(data):
    return "{{Forging Bonds Infobox" + \
        "\n|number=" + str(int(util.cargoQuery('ForgingBonds', 'COUNT(DISTINCT _pageName)=Nb')[0]['Nb']) + 1) + \
        "\n|characters=" + ",".join([util.getName(unit) for unit in data['units']]) + \
        "\n|accessories=" + ",".join([util.getName(acc) for acc in data['bonus_accessories']]) + \
        f"\n|startTime={data['event_avail']['start']}" + \
        f"\n|endTime={(datetime.strptime(data['event_avail']['finish'], util.TIME_FORMAT) - timedelta(seconds=1)).strftime(util.TIME_FORMAT)}" + \
        "\n}}"

def FBAvailability(data):
    return "==Availability==\nThis [[Forging Bonds]] event was made available:\n" +\
        "* {{HT|" + data['event_avail']['start'] + "}} – {{HT|" + (datetime.strptime(data['event_avail']['finish'], util.TIME_FORMAT) - timedelta(seconds=1)).strftime(util.TIME_FORMAT) + "}} " + \
        f"([[Forging Bonds: {util.getName(data['title'])} (Notification)|Notification]])"

def FBRewards(data):
    s = "==Rewards==\n{{#invoke:Reward/ForgingBonds|main"
    s += "\n|wikiname=" + util.cleanStr(f"{util.getName(data['title'])} {datetime.strptime(data['event_avail']['start'], util.TIME_FORMAT).strftime('%Y%m%d')}")
    for i, color in enumerate(COLORS):
        s += f"\n|{color}={{"
        for r in data['hero_rewards']:
            if r['unit'] == i+1:
                s += f"\n  {r['score']}={parseReward(r['reward'])};"
        s += "\n}"
        s = re.sub(r"<!--Summoning Ticket: \[[^]]*\]-->", "First Summon Ticket I", s)
    s += "\n}}"
    return s

def FBConversation(data):
    s = "==Special conversations==\n"
    s += f"==={util.getName(data['title'])}===\n"
    s += f"===={util.getName(data['title'])} - Opening====\n"
    s += Conversation(f"PORTRAIT_{data['original_id_tag']}", "MID_SCENARIO_OPENING")
    for t in ['C', 'B', 'A']:
        s += f"\n===={util.getName(data['title'])} - {t}====\n"
        s += "{{tab/start}}{{tab/header|English}}\n{{StoryTextTableHeader}}\n" + \
            "{{StoryImage|}}\n{{StoryTextTable||}}\n{{StoryTextTableEnd}}\n" +  \
            "{{tab/header|Japanese}}\n{{StoryTextTableHeader}}\n{{StoryImage|}}\n" + \
            "{{StoryTextTable|||ja}}\n{{StoryTextTableEnd}}\n{{tab/end}}"
    for unit in [util.getName(u) for u in data['units']]:
        s += f"\n==={unit}==="
        for t in ['C', 'B', 'A', 'S']:
            s += f"\n===={unit} - {t}====\n"
            s += "{{tab/start}}{{tab/header|English}}\n{{StoryTextTableHeader}}\n" + \
                "{{StoryImage|}}\n{{StoryTextTable|"+unit+"|}}\n{{StoryTextTableEnd}}\n" +  \
                "{{tab/header|Japanese}}\n{{StoryTextTableHeader}}\n{{StoryImage|}}\n" + \
                "{{StoryTextTable|"+unit+"||ja}}\n{{StoryTextTableEnd}}\n{{tab/end}}"
    s += "\n" + StoryNavBar(util.getName(data['title']), "", "")
    return s

def FBMap(tagId: str) -> dict:
    datas = reverseFile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Portrait/' + tagId + '.bin.lz')
    content = {}
    for data in datas:
        s = FBInfobox(data) + "\n"
        s += FBAvailability(data) + "\n"
        s += FBRewards(data) + "\n"
        s += FBConversation(data) + "\n"
        s += mapUtil.InOtherLanguage(data['title'])
        s += "{{Main Events Navbox}}"
        content[util.getName(data['title'])] = s
    return content

from sys import argv

if __name__ == '__main__':
    for arg in argv[1:]:
        if re.match(r'^\d+_\w+$', arg):
            a = FBMap(arg)
            for k in a:
                print(k, a[k])
        else:
            print("A tagId (\\d+_\\w+) is expected, but got '"+arg+"'")
