#! /usr/bin/env python3

from globals import DATA, DIFFICULTIES, ROMAN, ERROR
import util
import mapUtil
from DerivedMapSettings import DERIVED_SETTINGS

def MapIdToDiff(mapId):
    return DIFFICULTIES[ord(mapId[-1]) - ord('A')]

def getRequiredStage(mapId: str):
    for scenario in util.fetchFehData("Common/SRPG/StageScenario", None):
        for m in scenario['maps'][0]['scenarios']:
            if m['id_tag'][:-1] == mapId:
                return scenario
    return {}

def getDerivedSettings(dMap: list, groupId: str, index):
    for settings in DERIVED_SETTINGS:
        ok = True
        if len(settings['mapCond']) == len(dMap):
            for i in range(len(dMap)):
                for cond in settings['mapCond'][i]:
                    if settings['mapCond'][i][cond] != dMap[i][cond]:
                        ok = False
            if ok:
                for i in range(len(settings['extraCond'])):
                    if settings['extraCond'][i](groupId, index):
                        return settings['value'][i]
    return {'name': '', 'diff': []}

def DerivedUnitData(derivedMap, i: int, newId: str):
    if type(derivedMap) is dict:
        derivedMap = [derivedMap]
    SRPGMap = util.readFehData("Common/SRPGMap/" + derivedMap[0]['map_id'] + ".json")
    dSett = getDerivedSettings(derivedMap, newId, i-1)

    allyPos = []
    for ally in SRPGMap['player_pos']:
        allyPos += [str(chr(ally['x'] + ord('a'))) + str(ally['y'] + 1)]

    derivedTabs = []
    if len(dSett['diff']) != 0:
        for j in range(len(derivedMap)):
            derivedTabs += [dSett['diff'][j] + "=" + MapIdToDiff(derivedMap[j]['map_id'])]

    return "{{#invoke:UnitData|main" + \
        f"|mapImage={mapUtil.MapImage(SRPGMap['field'], True).replace('{{MapLayout', '{{#invoke:MapLayout|map')}" + \
        f"|allyPos={','.join(allyPos)}|battle={i}|derived={dSett['name']}" + \
        f"|derivedMap={util.getName('MID_STAGE_' + derivedMap[0]['map_id'][0:5])}" + \
        "|derivedTabs={" + ';'.join(derivedTabs) + "} }}\n"

def UnitDataSA(maps: dict):
    content = "==Unit data==\n"
    for i in range(1,len(maps['map_ids'])+1):
        content += f"===Battle {i}===\n"
        content += DerivedUnitData(maps['map_ids'][i-1], i, maps['group_id'])
    return content

def SquadAssault(mapId: str):
    StageEvent = util.fetchFehData("Common/SRPG/SequentialTrialBind")[mapId]
    diff = DIFFICULTIES[StageEvent['scenario']['difficulty']]
    startTime = util.askFor(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z|)", f"StartTime of {DATA['MID_STAGE_TITLE_'+mapId]}:") or ''
    notif = util.askFor(r".+ \(Notification\)", f"Notification of {DATA['MID_STAGE_TITLE_'+mapId]}:") or ''

    content = mapUtil.MapInfobox({
        'id_tag': mapId,
        'group': "Squad Assault",
        'lvl': {diff: StageEvent['scenario']['true_lv']},
        'rarity': {diff: StageEvent['scenario']['stars']},
        'stam': {diff: StageEvent['scenario']['stamina']},
        'reward': {diff: StageEvent['scenario']['reward']}
    }, True) + "\n"
    content += mapUtil.MapAvailability({'start': startTime}, notif, "[[Squad Assault]]") + "{{clear|right}}\n\n"
    content += UnitDataSA(StageEvent['scenario']['maps'])
    content += mapUtil.InOtherLanguage("MID_STAGE_TITLE_" + mapId)
    content += "{{Squad Assaults Navbox}}"
    return content

def MapInfoboxCC(stage: dict, index: int):
    info = {
        'id_tag': stage['lists'][0]['list'][index]['id_tag'][:-1],
        'banner': stage['id_tag'] + '.webp',
        'group': "Chain Challenge: " + (stage['book'] and f"Book {ROMAN[stage['book']]}, " or '') + util.getName("MID_CHAPTER_"+stage['id_tag']),
        'mapName': "Chain Challenge: " + (stage['book'] and f"Book {ROMAN[stage['book']]}, " or '') + util.getName("MID_STAGE_TITLE_" + stage['lists'][0]['list'][index]['id_tag'][:-1]),
        'lvl': {}, 'rarity': {}, 'stam': {}, 'reward': {}
    }
    if stage['book']:
        info['book'] = 'Book ' + ROMAN[stage['book']]
    for idiff in range(len(stage['lists'])):
        diff = DIFFICULTIES[stage['lists'][idiff]['list'][index]['difficulty']]
        info['lvl'].update({diff: stage['lists'][idiff]['list'][index]['true_lv'] or stage['lists'][idiff]['list'][index]['lv']})
        info['rarity'].update({diff: stage['lists'][idiff]['list'][index]['stars']})
        info['stam'].update({diff: stage['lists'][idiff]['list'][index]['stamina']})
        info['reward'].update({diff: stage['lists'][idiff]['list'][index]['reward']})
    return mapUtil.MapInfobox(info, True)

def BasedCC(StageEvent: dict, index: int):
    s = "A [[Chain Challenge]] based on "

    title = util.getName(getRequiredStage(StageEvent['lists'][0]['list'][index]['maps']['map_ids'][0]['map_id'][:-1])['id_tag'])
    if StageEvent['is_paralogue']:
        s += f"[[Paralogue Maps#{title}|{title}]]"
    else:
        s += f"[[Story Maps#{title[title.find('C'):]}|{title}]]"
    if len(StageEvent['lists'][0]['list'][index]['maps']['map_ids']) > 5:
        title = util.getName(getRequiredStage(StageEvent['lists'][0]['list'][index]['maps']['map_ids'][-1]['map_id'][:-1])['id_tag'])
        if StageEvent['is_paralogue']:
            s += f" and [[Paralogue Maps#{title}|{title}]]"
        else:
            s += f" and [[Story Maps#{title[title.find('C'):]}|{title}]]"

    return s + ".\n__TOC__\n"

def UnitDataCC(stage: dict, index: int):
    content = "==Unit data==\n"
    for i in range(1,len(stage['lists'][0]['list'][index]['maps']['map_ids'])+1):
        content += f"===Battle {i}===\n"
        content += DerivedUnitData([stage['lists'][diff]['list'][index]['maps']['map_ids'][i-1] for diff in range(len(stage['lists']))],
            i, stage['lists'][0]['list'][index]['maps']['group_id'][:-1])
    return content

def ChainChallengeMap(mapId: str, StageEvent: dict=None, index: int=None, notif: str=''):
    if not StageEvent:
        for scenario in util.fetchFehData("Common/SRPG/SequentialTrialSideStory", None) + util.fetchFehData("Common/SRPG/SequentialTrialMainStory", None):
            for m in scenario['lists'][0]['list']:
                if m['id_tag'][:-1] == mapId:
                    StageEvent = scenario
                    index = scenario['lists'][0]['list'].index(m)
                    req = getRequiredStage(StageEvent['prerequisites'][0][:-1])
                    StageEvent['avail']['start'] = StageEvent['avail']['start'] or req['avail']['start']
                    notif = util.askFor(None, "What is the notification for \33[3mChain Challenge: " + (StageEvent['book'] and f"Book {ROMAN[StageEvent['book']]}, " or '') + DATA["MID_STAGE_TITLE_"+mapId] + f"\33[0m ({mapId})?") or ''

    content = MapInfoboxCC(StageEvent, index)
    content += BasedCC(StageEvent, index) + "\n"
    content += mapUtil.MapAvailability({'start': StageEvent['avail']['start']}, notif, "[[Chain Challenge]]") + "{{clear|right}}\n\n"
    content += UnitDataCC(StageEvent, index)
    content += "{{Chain Challenges Navbox|" + (StageEvent['is_paralogue'] and 'paralogues' or ('book-' + ROMAN[StageEvent['book']].lower())) + "}}"
    return content

def ChainChallengeGroup(groupId: str):
    if groupId[4] == 'X':
        StageEvent = util.fetchFehData("Common/SRPG/SequentialTrialSideStory")[groupId]
    else:
        StageEvent = util.fetchFehData("Common/SRPG/SequentialTrialMainStory")[groupId]

    StageEvent['avail']['start'] = StageEvent['avail']['start'] or getRequiredStage(StageEvent['prerequisites'][0][:-1])['avail']['start']
    notif = util.askFor(None, "What is the notification for \33[3mChain Challenge: " + (StageEvent['book'] and f"Book {ROMAN[StageEvent['book']]}, " or '') + util.getName("MID_CHAPTER_" + StageEvent['id_tag']) + f"\33[0m ({groupId})?") or ''

    ret = {}
    for i in range(StageEvent['lists'][0]['count']):
        ret.update({"Chain Challenge: " + (StageEvent['book'] and f"Book {ROMAN[StageEvent['book']]}, " or '') +
            util.getName("MID_STAGE_TITLE_" + StageEvent['lists'][0]['list'][i]["id_tag"][:-1]):
                ChainChallengeMap("", StageEvent, i, notif)})
    return ret

def BlessedGarden(groupId: str):
    #TODO Maybe
    return

from sys import argv

if __name__ == "__main__":
    if len(argv) == 1:
        exit(0)
    if argv[1][0:3] == 'SB_':
        print(SquadAssault(argv[1]))
    elif argv[1][0:4] == 'ST_C':
        print(ChainChallengeGroup(argv[1]))
    elif argv[1][0:3] == 'ST_':
        print(ChainChallengeMap(argv[1]))
    elif argv[1][0:3] == 'BG_':
        BlessedGarden(argv[1])
    else:
        print(ERROR + "Unknow map")