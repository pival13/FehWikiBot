#! /usr/bin/env python3

import re

import util
from globals import UNIT_IMAGE, SOUNDS

def getBgm(id):
    if id in SOUNDS:
        return SOUNDS[id]['list'][0]['file'] + '.ogg'
    else:
        return id

def parseScenario(s: str, lang: str):
    wikitext = []
    data = {a['key']: a['value'] for a in util.fetchFehData(("USEN" if lang == 'en' else "JPJA") + "/Message/Data")}

    s = s.replace("$k", "").replace("$p", "\t").replace("$Nu", "{{Summoner}}").replace("$Nf", "{{Friend}}")
    s = re.sub(r"\$c([,0-9]+)(?:(\|$)|\|)", "@COLOR@\\1@\\2", s)

    sections = []
    for section in re.findall(r'\$[^$]*', s):
        for part in section.split('|'):
            sections += [part.strip().replace('\t', '<br>').replace('\n', '<br>')] if part != "" else []

    print(sections)
    name = ""
    heroJSON = {}
    expr = ""
    for section in sections:
        if len(section) == 0: continue
        if section[0] != '$':
            nameplate = '' if 'id_tag' in heroJSON and name == data['M'+heroJSON['id_tag']] else f"|duo={name}" if 'legendary' in heroJSON and 'kind' in heroJSON['legendary'] and heroJSON['legendary']['kind'] in [2,3] else f"|nameplate={name}"
            if len(re.findall(r'@COLOR@', section)) == 2 and section[:7] == '@COLOR@' and section[-23:] == '@COLOR@255,255,255,255@':
                section = re.sub(r"^@COLOR@([^@]+)@(.*)@COLOR@.*$", "color=\\1|\\2", section)
            else:
                section = re.sub(r"@COLOR@([^@]+)@(.*?)(?:@!COLOR@|(@COLOR@))", "{{#tag:span style='color:rgb(\\1)'|\\2}}\\3", section.replace('@COLOR@255,255,255,255@','@!COLOR@'))
            wikitext += ["{{StoryTextTable" + nameplate +
                        (util.getName(heroJSON['id_tag']) if not 'name' in heroJSON else heroJSON['name']) +
                        (f"|expression={expr[5:]}" if expr != 'Face' else '') +
                        '|' + section + ('|ja}}' if lang == 'ja' else '}}')]
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
            wikitext += ["{{StoryBGM|" + getBgm(section[4:section.find(',')]) + "}}"]
        elif section[:4] == '$Ssp':
            wikitext += ["{{StorySE|" + section[4:] + "}}"]
        elif section[:3] == '$Fo':
            wikitext += ["{{StoryFo|" + section[3:].replace(',','|') + "}}"]
        elif section[:3] == '$Fi': continue# Fade In (remove the fade panel)
        elif section[:4] == '$Sbs': continue# Stop BGM
        else:
            print(util.TODO + 'Unsupported story flag: ' + section)

    return wikitext

def parseStructure(obj, lang):
    opening = []
    mapBegin = []
    mapEnd = []
    ending = []
    wikitext = []

    for key in obj:
        if key == "MID_SCENARIO_OPENING_BGM":
            opening += ["{{StoryBGM|" + getBgm(obj[key]) + "}}"]
        elif key == "MID_SCENARIO_OPENING_IMAGE":
            opening += ["{{StoryImage|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_OPENING":
            opening += parseScenario(obj[key], lang)
        elif key == "MID_SCENARIO_MAP_BEGIN_BGM":
            mapBegin += ["{{StoryBGM|" + getBgm(obj[key]) + "}}"]
        elif key == "MID_SCENARIO_MAP_BEGIN_IMAGE":
            mapBegin += ["{{StoryImage|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_MAP_BEGIN":
            mapBegin += parseScenario(obj[key], lang)
        elif key == "MID_SCENARIO_MAP_END_BGM":
            mapEnd += ["{{StoryBGM|" + getBgm(obj[key]) + "}}"]
        elif key == "MID_SCENARIO_MAP_END_IMAGE":
            mapEnd += ["{{StoryImage|" + obj[key] + "}}"]
        elif key == "MID_SCENARIO_MAP_END":
            mapEnd += parseScenario(obj[key], lang)
        elif key == "MID_SCENARIO_ENDING_BGM":
            ending += ["{{StoryBGM|" + getBgm(obj[key]) + "}}"]
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

def Conversation(mapId, tag):
    enJSON = {a['key']: a['value'] for a in util.readFehData("USEN/Message/Scenario/" + mapId + ".json")}
    jaJSON = {a['key']: a['value'] for a in util.readFehData("JPJA/Message/Scenario/" + mapId + ".json")}
    wikiTextUSEN = []
    wikiTextJPJA = []

    if tag in enJSON:
        if tag + "_BGM" in enJSON:
            wikiTextUSEN += ["{{StoryBGM|" + getBgm(enJSON[tag+"_BGM"]) + "}}"]
        if tag + "_IMAGE" in enJSON:
            wikiTextUSEN += ["{{StoryImage|" + enJSON[tag+"_IMAGE"] + "}}"]
        wikiTextUSEN += parseScenario(enJSON[tag], "en")
    else:
        wikiTextUSEN = ["{{StoryImage|}}", "{{StoryTextTable||}}"]

    if tag in jaJSON:
        if tag + "_BGM" in jaJSON:
            wikiTextJPJA += ["{{StoryBGM|" + getBgm(jaJSON[tag+"_BGM"]) + "}}"]
        if tag + "_IMAGE" in jaJSON:
            wikiTextJPJA += ["{{StoryImage|" + jaJSON[tag+"_IMAGE"] + "}}"]
        wikiTextJPJA += parseScenario(jaJSON[tag], "ja")
    else:
        wikiTextJPJA = ["{{StoryImage|}}", "{{StoryTextTable|||ja}}"]

    return '\n'.join(['{{tab/start}}{{tab/header|English}}','{{StoryTextTableHeader}}'] + wikiTextUSEN +
                     ['{{StoryTextTableEnd}}','{{tab/header|Japanese}}','{{StoryTextTableHeader}}'] +
                     wikiTextJPJA + ['{{StoryTextTableEnd}}','{{tab/end}}'])

def StoryNavBar(mapId, prev='', next=''):
    answer = util.askFor(None, f"{mapId}: Previous story{prev != '' and (' is ' + prev + '?') or ''}")
    if answer and re.match('n|no', answer, re.IGNORECASE):
        prev = ""
    elif answer and not re.fullmatch('y|o|yes|oui|', answer, re.IGNORECASE):
        prev = answer
    answer = util.askFor(None, f"{mapId}: Next story{next != '' and (' is ' + next + '?') or ''}")
    if answer and re.match('n|no', answer, re.IGNORECASE):
        next = ""
    elif answer and not re.fullmatch('y|o|yes|oui|', answer, re.IGNORECASE):
        next = answer
    return '{{Story Navbar|' + prev + '|' + next + '}}'

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
    pmapid = util.getName(pmapid) if mapId[0] in ['S','X'] and util.getName(pmapid) != pmapid else ''
    nmapid = mapId[:-1] + str(int(mapId[-1]) +1)
    nmapid = util.getName(nmapid) if mapId[0] in ['S','X'] and util.getName(nmapid) != nmapid else ''
    navbar = StoryNavBar(mapId, pmapid, nmapid) + "\n"

    return '\n'.join(outputWikitext + ['{{tab/start}}{{tab/header|English}}'] + wikiTextUSEN +
                     ['{{tab/header|Japanese}}'] + wikiTextJPJA + ['{{tab/end}}\n'+navbar])

from sys import argv

if __name__ == "__main__":
    print(Story(argv[1]))