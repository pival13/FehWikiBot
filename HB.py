#! /usr/bin/env python3

from datetime import datetime
import re
import json

import util
import mapUtil
from scenario import Story
from reward import parseReward
from globals import DATA, DIFFICULTIES, ERROR, UNIT_IMAGE

def getHeroWithName(name: str):
    heroes = util.fetchFehData("Common/SRPG/Person", None)
    for hero in heroes:
        if util.getName(hero['id_tag']) == name:
            return hero
    return {}

def getBHBHero(mapId: str):
    scenario = util.readFehData("USEN/Message/Scenario/"+mapId+".json")
    faceNames = list(dict.fromkeys(re.findall(r"ch\d{2}_\d{2}_\w+", scenario[1]['value'])))
    heroes = [UNIT_IMAGE[faceName] for faceName in faceNames]

    mapName = util.getName(mapId)
    heroesName = [util.getName(heroes[i]['id_tag']) for i in range(len(heroes))]
    if heroesName[0][0] == mapName[0] and heroesName[1][0] == mapName[4] and mapName[0] != mapName[4]:
        return heroes
    elif heroesName[0][0] == mapName[4] and heroesName[1][0] == mapName[0] and mapName[0] != mapName[4]:
        return [heroes[1], heroes[0]]
    elif mapName[0] != mapName[4]:
        print(ERROR + "Unexpected heroes on " + mapId + ': ' + ', '.join(heroesName))
    else:
        while True:
            rep = util.askFor(f"{heroesName[0]}|{heroesName[1]}|1|2", f"Which unit is the first one {heroesName[0]} or {heroesName[1]}?")
            if rep and (rep == '1' or rep == heroesName[0]):
                return heroes
            elif rep and ((rep == '2' or rep == heroesName[1])):
                return [heroes[1], heroes[0]]

def HBMapInfobox(StageEvent: dict, group: str, SRPGMap: dict=None):
    if SRPGMap and 'field' in SRPGMap and 'player_pos' in SRPGMap:
        SRPGMap['field'].update(SRPGMap['player_pos'])
    info = {
        'id_tag': StageEvent['id_tag'],
        'banner': 'Banner ' + StageEvent['banner_id'] + '.webp',
        'group': group,
        'requirement': [],
        'lvl': {}, 'rarity': {}, 'stam': {}, 'reward': {},
        'map': SRPGMap and 'field' in SRPGMap and SRPGMap['field'] or {'id': StageEvent['id_tag'], 'player_pos': []},
        'bgms': util.getBgm(StageEvent['id_tag'])
    }
    if StageEvent['scenarios'][-1]['survives']:             info['requirement'] += ['All allies must survive.']
    if StageEvent['scenarios'][-1]['no_lights_blessing']:   info['requirement'] += ["Cannot use {{It|Light's Blessing}}."]
    if StageEvent['scenarios'][-1]['turns_to_win'] != 0:    info['requirement'] += [f"Turns to win: {StageEvent['scenarios'][-1]['turns_to_win']}"]
    if StageEvent['scenarios'][-1]['turns_to_defend'] != 0: info['requirement'] += [f"Turns to defend: {StageEvent['scenarios'][-1]['turns_to_defend']}"]
    info['requirement'] = '<br>'.join(info['requirement'])

    if StageEvent['scenarios'][-1]['reinforcements']:
        info['mode'] = 'Reinforcement Map'
    for index in range(len(StageEvent['scenarios'])):
        diff = DIFFICULTIES[StageEvent['scenarios'][index]['difficulty']]
        info['lvl'].update({diff: StageEvent['scenarios'][index]['true_lv']})
        info['rarity'].update({diff: StageEvent['scenarios'][index]['stars']})
        info['stam'].update({diff: StageEvent['scenarios'][index]['stamina']})
        info['reward'].update({diff: StageEvent['scenarios'][index]['reward']})

    return mapUtil.MapInfobox(info)

def HBUnitData(StageEvent: dict, SRPGMap: dict, hero):
    if type(hero) != list:
        hero = [hero]

    s = "==Unit data==\n"
    s += "{{#invoke:UnitData|main"
    if SRPGMap == {} or not 'units' in SRPGMap:
        s += "|globalai="
    if StageEvent['scenarios'][-1]['reinforcements']:
        s += "\n|mapImage=" + mapUtil.MapImage(SRPGMap and 'field' in SRPGMap and SRPGMap['field'] or {'id': StageEvent['id_tag']}, True, True)
    if SRPGMap and 'units' in SRPGMap:
        #TODO unit data is present in assets files
        pass
        #for idiff in range(len(SRPGMap)):
        #    s += "|" + DIFFICULTIES[StageEvent['maps'][idiff]['scenarios'][index]['difficulty']] + "="
        #    s += mapUtil.UnitData(SRPGMap[idiff]) + "\n"
    else:
        for idiff, scenario in enumerate(StageEvent['scenarios']):
            s += '\n|' + DIFFICULTIES[scenario['difficulty']] + '='
            units = []
            for i in range(len([True for w in scenario['enemy_weps'] if w != -1])):
                units += [{'rarity': scenario['stars'], 'true_lv': scenario['true_lv']}]
                if scenario['difficulty'] > 2: units[-1]['refine'] = True
            for i, h in enumerate(hero):
                units[i]['id_tag'] = h['id_tag']
                units[i]['cooldown_count'] = None
            if scenario['reinforcements']:
                units += [{'rarity': scenario['stars'], 'true_lv': scenario['true_lv'], 'spawn_count': 0}]
                if scenario['difficulty'] > 2: units[-1]['refine'] = True
            s += mapUtil.UnitData({'units': units})
    return s + "\n}}\n"

def LegendaryHeroBattle(mapId: str):
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent")[mapId]
    SRPGMap = util.readFehData("../feh-assets-json/extras/SRPGMap/"+mapId+"A.json", True)

    hero = getHeroWithName(util.getName(mapId))
    kind = hero['legendary']['element'] > 4 and 'Mythic Hero Battle' or 'Legendary Hero Battle'

    content =  HBMapInfobox(StageEvent, kind, SRPGMap) + "\n"
    content += mapUtil.MapAvailability(StageEvent['avail'], f"{kind}! ({datetime.strptime(StageEvent['avail']['start'], util.TIME_FORMAT).strftime('%b %Y')}) (Notification)", f"[[{kind}]]")
    content += HBUnitData(StageEvent, SRPGMap, hero) + '\n'
    content += Story(mapId) + "\n"
    content += "==Trivia==\n*\n"
    content += mapUtil.InOtherLanguage(["MID_STAGE_"+mapId, "MID_STAGE_HONOR_"+mapId], 1)
    content += "{{Special Maps Navbox}}"
    return content

def BoundHeroBattle(mapId: str):
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent")[mapId]
    SRPGMap = util.readFehData("../feh-assets-json/extras/SRPGMap/"+mapId+"A.json", True)

    heroes = getBHBHero(mapId)
    name = util.getName(mapId)
    if name[0] != name[4]:
        name = name.replace(name[4], DATA["M"+heroes[1]['id_tag']], 1).replace(name[0], DATA["M"+heroes[0]['id_tag']], 1)
    else:
        name = name.replace(name[0], DATA["M"+heroes[1]['id_tag']], 2).replace(DATA["M"+heroes[1]['id_tag']], DATA["M"+heroes[0]['id_tag']], 1)

    content =  HBMapInfobox(StageEvent, "Bound Hero Battle", SRPGMap) + "\n"
    content += mapUtil.MapAvailability(StageEvent['avail'], f"Bound Hero Battle: {DATA['M'+heroes[0]['id_tag']]} & {DATA['M'+heroes[1]['id_tag']]} (Notification)", "[[Bound Hero Battle]]")
    content += HBUnitData(StageEvent, SRPGMap, heroes) + '\n'
    content += Story(mapId) + "\n"
    content += "==Trivia==\n*\n"
    content += mapUtil.InOtherLanguage(["MID_STAGE_"+mapId, "MID_STAGE_HONOR_"+mapId], 1)
    content += "{{Special Maps Navbox}}"

    return {name: content}

def GrandHeroBattle(mapId: str):
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent")[mapId]
    SRPGMap = util.readFehData("../feh-assets-json/extras/SRPGMap/"+mapId+"A.json", True)

    hero = getHeroWithName(util.getName(mapId))

    content =  HBMapInfobox(StageEvent, "Grand Hero Battle", SRPGMap) + "\n"
    content += mapUtil.MapAvailability(StageEvent['avail'], f"Grand Hero Battle - {util.getName(mapId)} (Notification)", "[[Grand Hero Battle]]")
    content += HBUnitData(StageEvent, SRPGMap, hero) + '\n'
    content += Story(mapId) + "\n"
    content += "==Trivia==\n*\n"
    content += mapUtil.InOtherLanguage(["MID_STAGE_"+mapId, "MID_STAGE_HONOR_"+mapId], 1)
    content += "{{Special Maps Navbox}}"

    return content

def LimitedHeroBattleTemplate(StageEvent: object):
    entry = []
    obj = {DIFFICULTIES[scenario['difficulty']]: scenario['reward'] for scenario in StageEvent['scenarios']}
    reward = "{\n"
    for diff in DIFFICULTIES:
        if diff in obj:
            reward += "  " + diff + "=" + parseReward(obj[diff]) + ";\n"
    reward += "}"
    for i in range(8*4):
        if StageEvent['scenarios'][0]['origins'] & (1 << i):
            entry.append(str(i))
    return "{{Limited Hero Battle\n" + \
        f"|map={StageEvent['id_tag']}|entry={','.join(entry)}" +\
        f"|refresher={StageEvent['scenarios'][0]['max_refreshers']}\n" + \
        f"|reward={reward}\n" + \
        f"|start={StageEvent['avail']['start']}|end={util.timeDiff(StageEvent['avail']['finish'])}\n" + \
        f"|notification=Limited Hero Battles! ({datetime.strptime(StageEvent['avail']['start'], util.TIME_FORMAT).strftime('%b %Y')}) (Notification)\n" + \
        "}}"

from wikiUtil import getPageContent
def LimitedHeroBattle(mapId: str):
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent")[mapId]
    pageName = util.cargoQuery('Maps', where=f"Map='{StageEvent['banner_id']}'", limit=1)[0]['Page'].replace('&amp;', '&')
    content = getPageContent([pageName])[pageName]

    if not re.search(r"==\s*Limited Hero Battle\s*==", content):
        content = re.sub(r"(==\s*Unit [dD]ata\s*==(\n.*)*?)\n==", "\\1\n==Limited Hero Battle==\n==", content)
    if content.find("{{Limited Hero Battle/header}}") == -1:
        content = re.sub(r"(==\s*Limited Hero Battle\s*==)\n", "\\1\n{{Limited Hero Battle/header}}\n|}\n", content)
    if not re.search(r"map\s*=\s*"+mapId, content):
        content = re.sub(r"(==\s*Limited Hero Battle\s*==(\n.*)*?)\n\|\}", "\\1\n"+LimitedHeroBattleTemplate(StageEvent)+"\n|}", content)
    return {pageName: content}

def RevivalHeroBattle(mapId: str):
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent")[mapId]
    pageName = util.cargoQuery('Maps', where=f"Map='{StageEvent['banner_id']}'", limit=1)[0]['Page'].replace('&amp;', '&')
    content = getPageContent([pageName])[pageName]

    if mapId[0] in ['I', 'Q', 'V'] or re.search(r"start\s*=\s*"+StageEvent['avail']['start']+r"\s*\|end\s*=\s*"+util.timeDiff(StageEvent['avail']['finish']), content):
        return {}
    
    starttime = datetime.strptime(StageEvent['avail']['start'], util.TIME_FORMAT)
    if starttime >= datetime.strptime(util.timeDiff(StageEvent['avail']['finish'], 86400*4), util.TIME_FORMAT):
        notification = ""
    else:
        kind = re.search(r"mapGroup\s*=\s*(.*)\n", content)[1]
        
        if kind.find('Legendary') != -1 or kind.find('Mythic') != -1:
            year = int(StageEvent['avail']['start'][:4])
            month = int(StageEvent['avail']['start'][5:7])
            day = int(StageEvent['avail']['start'][8:10])
            if day > 25 or day < 3:
                if day < 3: month -= 1
                if month % 2 == 0:
                    notification = f"Legendary Hero Battle! ({datetime(year=year,month=month,day=1).strftime('%b %Y')}) (Notification)"
                else:
                    notification = f"Mythic Hero Battle! ({datetime(year=year,month=month,day=1).strftime('%b %Y')}) (Notification)"
            else:
                notification = f'Legendary Hero Remix ({datetime(year=year,month=month,day=1).strftime("%b %Y")}) (Notification)'
    
        elif kind.find('Bound') != -1:
            if content.find('Bound Hero Battle Revival') == -1:
                notification = f"Bound Hero Battle Revival: {pageName[:pageName.find(':')]} (Notification)"
            else:
                notification = f"Bound Hero Battle Revival: {pageName[:pageName.find(':')]} ({starttime.strftime('%b %Y')}) (Notification)"

        elif kind.find('Grand') != -1:
            if content.find('Grand Hero Battle Revival') == -1:
                notification = f"Grand Hero Battle Revival - {pageName[:pageName.find(' (')]} (Notification)"
            else:
                notification = f"Grand Hero Battle Revival - {pageName[:pageName.find(' (')]} ({starttime.strftime('%b %Y')}) (Notification)"

        else:
            print(util.TODO + "Unknow revival")
            return {}
    
    content = re.sub(r"(\{\{MapDates[^\n]*)(\s*?\n)*(==\s*Unit [Dd]ata\s*==)", f"\\1\n* {{{{MapDates|start={StageEvent['avail']['start']}|end={util.timeDiff(StageEvent['avail']['finish'])}|notification={notification}}}}}\n\\3", content)
    return {pageName: content}


from sys import argv

if __name__ == '__main__':
    for arg in argv[1:]:
        if re.match(r'T\d{4}', arg) and util.getName(arg)[2] == '&':
            maps = list(BoundHeroBattle(arg).items())[0]
            print(maps[0], maps[1], sep='\n')
        elif re.match(r'T\d{4}', arg):
            print(GrandHeroBattle(arg))
        elif re.match(r'L\d{4}', arg):
            print(LegendaryHeroBattle(arg))
        elif re.match(r'I\d{4}', arg):
            print(LimitedHeroBattle(arg))
        else:
            print(util.ERROR, "Unknow argument", arg)