#! /usr/bin/env python3

import re
from num2words import num2words
from datetime import datetime

import util
import wikiUtil
from globals import DATA, UNIT_IMAGE
from scenario import Story, getBgm
from reward import parseReward
from mapUtil import InOtherLanguage
from Reverse import reverseTapBattle

def TBInfobox(data):
    bgms = list({stage['bgm']: 1 for diff in data['stages'] for stage in data['stages'][diff]}.keys())
    bgmsBoss = list({stage['boss_stage'][-1]['bgm']: 1 for diff in data['stages'] for stage in data['stages'][diff] if len(stage['boss_stage']) > 0}.keys())
    bgmsExtra = list({stage['bgm']: 1 for diff in data['extras'] for stage in data['extras'][diff]}.keys())
    bgmsExtraBoss = list({stage['boss_stage'][-1]['bgm']: 1 for diff in data['extras'] for stage in data['extras'][diff] if len(stage['boss_stage']) > 0}.keys())
    return "{{Tap Battle Infobox\n" + \
        f"|number={int(data['id_tag'][5:9])}\n" + \
        '\n'.join([f"|BGM{i+1 if i != 0 else ''}={getBgm(bgm)}" for i,bgm in enumerate(bgms)]) + '\n' + \
        '\n'.join([f"|BGMExtra{i+1 if i != 0 else ''}={getBgm(bgm)}" for i,bgm in enumerate(bgmsExtra)]) + '\n' + \
        '\n'.join([f"|BGMBoss{i+1 if i != 0 else ''}={getBgm(bgm)}" for i,bgm in enumerate(bgmsBoss)]) + '\n' + \
        '\n'.join([f"|BGMExtraBoss{i+1 if i != 0 else ''}={getBgm(bgm)}" for i,bgm in enumerate(bgmsExtraBoss)]) + '\n' + \
        f"|startTime={data['start']}\n" + \
        f"|endTime={util.timeDiff(data['finish'])}\n" + \
        "}}"

def TBStages(data):
    s = "==Stages==\n{{#invoke:TapBattle|stages\n|stages=[\n"
    for i, floor in enumerate(data['stages']['normal']):
        s += '{name=' + DATA[f"MID_TAP_BATTLE_STAGE_TITLE_{floor['begining_floor']}_{floor['begining_floor']+4}"]
        s += f";rewards={parseReward(floor['rewards'])}"
        if i == 0 or floor['bgm'] != data['stages']['normal'][i-1]['bgm']:
            if floor['bgm']:
                s += f";BGM={getBgm(floor['bgm'])};BPM={floor['BPM']}"
            else:
                s += ';BGM=-'
        if floor['score'] > 0:
            s += f";scores=[{floor['score']};{data['stages']['hard'][i]['score']}]"
        if floor['boss_id']:
            s += f";boss={','.join([util.getName('PID_'+boss['boss_id']) for boss in floor['boss_stage']])}"
            s += f";bossBGM={','.join(list({getBgm(boss['bgm']): 1 for boss in floor['boss_stage']}.keys()))}"
            s += f";bossBPM={','.join(list({boss['bgm']: str(boss['BPM']) for boss in floor['boss_stage']}.values()))}"
            s += f";bossHP=[;]"
        s += "};\n"
    s += "]}}"
    if data['extra_count'] > 0:
        s += "\n==Extra Stages==\n{{#invoke:TapBattle|stages\n"
        s += f"|delay={(datetime.strptime(data['extras']['normal'][0]['start'], util.TIME_FORMAT) - datetime.strptime(data['start'], util.TIME_FORMAT)).days}\n"
        s += '|stages=[\n'
        for i, floor in enumerate(data['extras']['normal']):
            s += '{name=' + DATA[f"MID_TAP_BATTLE_EXTRA_STAGE_TITLE_{i+1}"]
            s += f";rewards={parseReward(floor['rewards'])}"
            if i == 0 or floor['bgm'] != data['extras']['normal'][i-1]['bgm']:
                if floor['bgm']:
                    s += f";BGM={getBgm(floor['bgm'])};BPM={floor['BPM']}"
                else:
                    s += ';BGM=-'
            if floor['score'] > 0:
                s += f";scores=[{floor['score']};{data['extras']['hard'][i]['score']}]"
            if floor['boss_id']:
                s += f";boss={','.join([util.getName('PID_'+(boss['boss_id'] if boss['boss_id'] else floor['boss_id'])) for boss in floor['boss_stage']])}"
                s += f";bossBGM={','.join(list({getBgm(boss['bgm']): 1 for boss in floor['boss_stage']}.keys()))}"
                s += f";bossBPM={','.join(list({boss['bgm']: str(boss['BPM']) for boss in floor['boss_stage']}.values()))}"
                s += f";bossHP=[;]"
            s += "};\n"
        s += "]}}"
    return s

def TBEnemies(data):
    foes = []
    for foe in data['foes']:
        if foe['id_tag'].find('/Enemy.plist/') == -1:
            foes += [UNIT_IMAGE[foe['id_tag'][foe['id_tag'].rfind('/')+1:]]]
    if len(foes) == 0:
        return ""
    else:
        s = '==Unique Enemies==\n'
        s += '{| class="wikitable default" style="text-align: center; margin:1em; width:400px;\n'
        s += '! style="width:33%" | Hero\n! style="width:25%" | Stage\n'
        for foe in foes:
            s += f"|-\n| {{{{HeroIcon with Type and Name|name={util.getName(foe['id_tag'])}}}}}\n| \n"
        s += '|}'
        return s

def TBStories(data):
    s = "==Story==\n"
    #TODO
    s += "\n"
    s += "===Final reward===\n"
    if data['backdrop'] == 'Spa_45_valentine01':
        s += "{{HotSpring}}"
    else:
        s += util.askFor(intro="What is the template used for spa ?")
    return s

def EncoreTapBattle(nb: int):
    data = reverseTapBattle(nb, True)

    name = util.getName(data["name"])
    page = wikiUtil.getPageContent(name)[name]

    if page.find(data["start"]) == -1:
        page = re.sub(r'(startTime=[^\n|}]+)', '\\1;'+data['start'], page, 1)
    if page.find(util.timeDiff(data["finish"])) == -1:
        page = re.sub(r'(endTime=[^\n|}]+)', '\\1;'+util.timeDiff(data["finish"]), page, 1)
    for floor in data['stages']['normal']:
        stageName = DATA[f"MID_TAP_BATTLE_STAGE_TITLE_{floor['begining_floor']}_{floor['begining_floor']+4}"]
        if not re.search(stageName + '.*encoreRewards', page):
            page = re.sub(f"({stageName}.*?reward.*?}})", f"\\1;encoreRewards={parseReward(floor['rewards'])}", page)
    for i, floor in enumerate(data['extras']['normal']):
        stageName = DATA[f"MID_TAP_BATTLE_EXTRA_STAGE_TITLE_{i+1}"]
        if not re.search(stageName + '.*encoreRewards', page):
            page = re.sub(f"({stageName}.*?reward.*?}})", f"\\1;encoreRewards={parseReward(floor['rewards'])}", page)
    return page

def TapBattle(nb: int):
    data = reverseTapBattle(nb, False)

    content = ""
    content += TBInfobox(data) + "\n"
    content += f"This is the {num2words(nb, to='ordinal')} [[Tap Battle]]" + "\n"
    content += TBStages(data) + "\n"
    content += TBEnemies(data) + "\n"
    content += TBStories(data) + "\n"
    content += "==Quests==\n{{#invoke:Quest|queryQuest}}\n"
    content += "==Trivia==\n*\n"
    content += InOtherLanguage(data['name'])
    content += "{{Main Events Navbox}}"

    return content

from sys import argv

if __name__ == '__main__':
    for arg in argv[1:]:
        if re.match(r'\d+.2', arg):
            r = EncoreTapBattle(int(arg[:-2]))
            print(r)
        elif re.match(r'\d+', arg):
            r = TapBattle(int(arg))
            print(r)
        else:
            print("Either a mapId (W\\d{4}) or a tagId (\\d+_\\w+) is expected")