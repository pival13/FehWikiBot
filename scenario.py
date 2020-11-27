#! /usr/bin/env python3

import util
import re

UNIT_IMAGE = util.fetchFehData("Common/SRPG/Person", "face_name")
UNIT_IMAGE.update(util.fetchFehData("Common/SRPG/Enemy", "face_name"))
UNIT_IMAGE.update({"ch00_00_Eclat_X_Normal": {'name': "Kiran"},
                    "ch00_13_Gustaf_M_Normal": {'name': "Gustav", 'id_tag': 'PID_グスタフ'},
                    "ch00_14_Henriette_F_Normal": {'name': "Henriette", 'id_tag': 'PID_ヘンリエッテ'},
                    "ch00_16_Freeze_M_Normal": {'name': "Hríd"},
                    "ch00_22_Tor_F_Normal": {'name': "Thórr", 'id_tag': 'PID_トール'},
                    "ch90_02_FighterAX_M_Normal": {'name': ''}})

def parseScenario(s: str, lang: str):
    wikitext = []
    data = {a['key']: a['value'] for a in util.fetchFehData(("USEN" if lang == 'en' else "JPJA") + "/Message/Data")}

    s = s.replace("$k", "").replace("$p", "\t").replace("$Nu", "{{Summoner}}").replace("$Nf", "{{Friend}}")

    sections = []
    for section in re.findall(r'\$[^$]*', s):
        for part in section.split('|'):
            sections += [part.strip().replace('\t', '<br>').replace('\n', '<br>')] if part != "" else []

    name = ""
    heroJSON = {}
    expr = ""
    for section in sections:
        if section[0] != '$' and len(section) > 0:
            nameplate = "|" if 'id_tag' in heroJSON and name == data['M'+heroJSON['id_tag']] else f"|duo={name}|" if 'legendary' in heroJSON and heroJSON['legendary'] and (heroJSON['legendary']['kind'] == 2 or heroJSON['legendary']['kind'] == 3) else f"|nameplate={name}|"
            wikitext += ["{{StoryTextTable" + nameplate +
                        (util.getName(heroJSON['id_tag']) if not 'name' in heroJSON else heroJSON['name']) +
                        (f"|expression={expr[5:]}|" if expr != 'Face' else '|') +
                        section + ('|ja}}' if lang == 'ja' else '}}')]
        elif section[:3] == '$Wm':
            info = section[3:].split(',')
            name = data[info[0]]
            heroJSON = UNIT_IMAGE[info[1]]
            expr = info[2]
        elif section[:2] == '$n':
            name = data[section[2:]]
        elif section[:2] == '$E':
            expr = section[2:]
        elif section[:4] == '$Sbp':
            wikitext += ["{{StoryBGM|" + section[4:section.find(',')] + "}}"]
        elif section[:4] == '$Ssp':
            wikitext += ["{{StorySE|" + section[4:] + "}}"]
        elif section[:3] == '$Fo':
            wikitext += ["{{StoryFo|" + section[3:].replace(',','|') + "}}"]

    return wikitext

def parseStructure(obj, lang):
    opening = []
    mapBegin = []
    mapEnd = []
    ending = []
    wikitext = []

    for key in obj:
        if key == "MID_SCENARIO_OPENING_BGM":
            opening += ["{{StoryBGM|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_OPENING_IMAGE":
            opening += ["{{StoryImage|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_OPENING":
            opening += parseScenario(obj[key], lang)
        elif key == "MID_SCENARIO_MAP_BEGIN_BGM":
            mapBegin += ["{{StoryBGM|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_MAP_BEGIN_IMAGE":
            mapBegin += ["{{StoryImage|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_MAP_BEGIN":
            mapBegin += parseScenario(obj[key], lang)
        elif key == "MID_SCENARIO_MAP_END_BGM":
            mapEnd += ["{{StoryBGM|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_MAP_END_IMAGE":
            mapEnd += ["{{StoryImage|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_MAP_END":
            mapEnd += parseScenario(obj[key], lang)
        elif key == "MID_SCENARIO_ENDING_BGM":
            ending += ["{{StoryBGM|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_ENDING_IMAGE":
            ending += ["{{StoryImage|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_ENDING":
            ending += parseScenario(obj[key], lang)
        else:
            wikitext += parseScenario(obj[key], lang)

    if len(opening) > 0:
        wikitext += ["===Opening===\n{{StoryTextTableHeader}}\n" + '\n'.join(opening) + "\n{{StoryTextTableEnd}}"]
    if len(mapBegin) > 0:
        wikitext += ["===Beginning of the battle===\n{{StoryTextTableHeader}}\n" + '\n'.join(mapBegin) + "\n{{StoryTextTableEnd}}"]
    if len(mapEnd) > 0:
        wikitext += ["===Stage Clear===\n{{StoryTextTableHeader}}\n" + '\n'.join(mapEnd) + "\n{{StoryTextTableEnd}}"]
    if len(ending) > 0:
        wikitext += ["===Ending===\n{{StoryTextTableHeader}}\n" + '\n'.join(ending) + "\n{{StoryTextTableEnd}}"]
    return wikitext

def Story(mapId: str):
    enJSON = {a['key']: a['value'] for a in util.readFehData("USEN/Message/Scenario/" + mapId + ".json")}
    jaJSON = {a['key']: a['value'] for a in util.readFehData("JPJA/Message/Scenario/" + mapId + ".json")}

    wikiTextUSEN = parseStructure(enJSON, "en")
    wikiTextJPJA = parseStructure(jaJSON, "ja")

    outputWikitext = ['==Story==']
    if len(wikiTextUSEN) == 1 and len(wikiTextJPJA) == 1:
        outputWikitext += [wikiTextUSEN[0][:wikiTextUSEN[0].find('\n')]]
        wikiTextUSEN[0] = wikiTextUSEN[0][wikiTextUSEN[0].find('\n')+1:]
        wikiTextJPJA[0] = wikiTextJPJA[0][wikiTextJPJA[0].find('\n')+1:]

    pmapid = mapId[:-1] + str(int(mapId[-1]) -1)
    pmapid = util.getName(pmapid) != pmapid and util.getName(pmapid) or ''
    answer = util.askFor(None, f"{mapId}: Previous story{pmapid != '' and (' is ' + pmapid + '?') or ''}")
    if answer and re.match('n|no', answer, re.IGNORECASE):
        pmapid = ""
    elif answer and not re.fullmatch('y|o|yes|oui|', answer, re.IGNORECASE):
        pmapid = answer

    nmapid = mapId[:-1] + str(int(mapId[-1]) +1)
    nmapid = util.getName(nmapid) != nmapid and util.getName(nmapid) or ''
    answer = util.askFor(None, f"{mapId}: Next story{nmapid != '' and (' is ' + nmapid + '?') or ''}")
    if answer and re.match('n|no', answer, re.IGNORECASE):
        nmapid = ""
    elif answer and not re.fullmatch('y|o|yes|oui|', answer, re.IGNORECASE):
        nmapid = answer

    navbar = '{{Story Navbar|' + pmapid + '|' + nmapid + '}}\n'
    return '\n'.join(outputWikitext + ['{{tab/start}}{{tab/header|English}}'] + wikiTextUSEN +
                     ['{{tab/header|Japanese}}'] + wikiTextJPJA + ['{{tab/end}}\n'+navbar])

from sys import argv

if __name__ == "__main__":
    print(Story(argv[1]))