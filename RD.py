#! /usr/bin/env python3

import requests
import json
import re
from num2words import num2words

from reward import MOVE
from util import DATA, DIFFICULTIES, URL
import util
import mapUtil

duplicate = {}

def getDuplicateMap(mapId: str):
    global duplicate
    try:
        result = requests.get(url=URL, params={
            "action": "query",
            "titles": "File:Map "+mapId+".webp",
            "prop": "duplicatefiles",
            "format": "json"
        }).json()
        result = list(result['query']['pages'].values())[0]
        for m in 'duplicatefiles' in result and result['duplicatefiles'] or []:
            if re.match(r"O\d{4}", m['name'][4:9]):
                duplicate[mapId] = [m['name'][4:9]]
                return m['name'][4:9]
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return getDuplicateMap(mapId)

def drawRDMapLayout(mapLayout: dict):
    key = [[ c + str(n) for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] ] for n in range(10, 0, -1) ]
    mapNormal = mapLayout['map']
    enemySpawn = re.compile(r"\{\{RDTerrain\|color=Enemy\|type=Spawn\}\}")
    enemyCamp = re.compile(r"\{\{RDTerrain\|color=Enemy\|type=Camp( Spawn)?\}\}")
    enemyWarpSpawn = re.compile(r"\{\{RDTerrain\|color=Enemy\|type=Warp Spawn\}\}")
    cellIsKind = lambda a, b, regex: a >= 0 and b >= 0 and a < len(mapNormal) and b < len(mapNormal[a]) and regex.search(mapLayout['map'][a][b])

    #Case 2 Spawn cell
    if sum([sum([bool(enemySpawn.search(cell)) for cell in line]) for line in mapNormal]) == 2:
        mapNormal = [[enemySpawn.sub("", cell) if enemySpawn.search(cell) else cell for cell in line] for line in mapNormal]
    #Case 2 Camp
    elif sum([sum([bool(enemyCamp.search(cell)) for cell in line]) for line in mapNormal]) == 2:
        mapNormal = [[re.sub("Warp Spawn", "Warp", mapNormal[i][j]) if cellIsKind(i, j, enemyWarpSpawn) and
            any([cellIsKind(x, y, enemyCamp) for (x, y) in [(i, j-1), (i, j+1), (i-1, j), (i+1, j)]])
                else mapNormal[i][j] for j in range(len(mapNormal[i]))] for i in range(len(mapNormal))]
    #Case 6 Warp Spawn. In this case, Warp Spawn next to only one warp spawn are remove
    elif sum([sum([bool(enemyWarpSpawn.search(cell)) for cell in line]) for line in mapNormal]) == 6:
        mapNormal = [[re.sub("Warp Spawn", "Warp", mapNormal[i][j]) if cellIsKind(i, j, enemyWarpSpawn) and
            any([cellIsKind(x, y, enemyCamp) and cellIsKind(x2, y2, enemyWarpSpawn) for (x, y, x2, y2) in [(i, j-1, i, j-2), (i, j+1, i, j+2), (i-1, j, i-2, j), (i+1, j, i+2, j)]])
                else mapNormal[i][j] for j in range(len(mapNormal[i]))] for i in range(len(mapNormal))]

    content = "|version1=Standard\n|mapImage={{MapLayout|type=RD|baseMap=" + mapLayout['basemap'] + "|backdrop=" + mapLayout['backdrop'] + "\n"
    for i in range(len(mapLayout['map'])):
        for j in range(len(mapLayout['map'][i])):
            content += "| " + key[i][j] + "=" + mapNormal[i][j] + ' '
        content = content[:-1] + '\n'
    content += "}}\n"
    content += "|version2=Infernal\n|mapImageV2={{MapLayout|type=RD|baseMap=" + mapLayout['basemap'] + "|backdrop=" + mapLayout['backdrop'] + "\n"
    for i in range(len(mapLayout['map'])):
        for j in range(len(mapLayout['map'][i])):
            content += "| " + key[i][j] + "=" + mapLayout['map'][i][j] + ' '
        content = content[:-1] + '\n'
    content += "}}"
    return content

def RDMapLayout(mapId: str):
    global duplicate
    dupMap = mapId in duplicate and duplicate[mapId][0] or getDuplicateMap(mapId)
    if not dupMap:
        return

    GC = int((int(dupMap[1:])-1) / 30) + 1
    result = -1
    while result == -1:
        try:
            result = requests.get(url=URL, params={
                "action": "query",
                "titles": "Grand Conquests " + str(GC),
                "prop": "revisions",
                "rvprop": "content",
                "rvslots": "*",
                "format": "json"
            }).json()
        except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            continue
    result = list(result['query']['pages'].values())[0]['revisions'][0]['slots']['main']['*']
    GCLayout = re.compile(r"\d+\s*\n\s*\|\s*{{MapLayout\D+"+dupMap+".*\n((?!}}\n)(.*\n))+}}\n").search(result)
    if not GCLayout:
        return
    else:
        GCLayout = GCLayout[0]

    duplicate[mapId] = [dupMap, re.findall(r"^(\d+)", GCLayout)[0]]
    result = {
        'basemap': mapId,
        'backdrop': re.findall(r"backdrop=(\w*)\n", GCLayout)[0],
        'map': [ re.findall(r"."+str(i)+r"=\s*(\{\{[^}]+\}\}|)\s*(?:\n|\|)", GCLayout) for i in range(10,0,-1) ]
    }
    return drawRDMapLayout(result)

def RDMapInfobox(StageEvent: dict):
    info = {
        'id_tag': 'OCCUPATION',
        'banner': 'Banner_Rival_Domains_' + MOVE[int(StageEvent['banner_id'][-1])-1] + '.png',
        'group': 'Rival Domains',
        'requirement': 'Reach the target [[Rival Domains#Scoring|score]] to earn<br>a reward. Bonus for defeating<br>foes with {{Mt|'+MOVE[int(StageEvent['banner_id'][-1])-1].lower()+'}} allies.',
        'mode': 'Reinforcement Map',
        'lvl': {'Normal': 30, 'Hard': 35, 'Lunatic': 40, 'Infernal': 40},
        'rarity': {'Normal': 3, 'Hard': 4, 'Lunatic': 5, 'Infernal': 5},
        'stam': {}, 'reward': {}, 'map': {}
    }

    for index in range(len(StageEvent['scenarios'])):
        diff = DIFFICULTIES[StageEvent['scenarios'][index]['difficulty']]
        info['stam'].update({diff: StageEvent['scenarios'][index]['stamina']})
        info['reward'].update({diff: StageEvent['scenarios'][index]['reward']})

    return re.sub(r"\|mapImage[^}]+\}\}", RDMapLayout(StageEvent['id_tag']), mapUtil.MapInfobox(info))

def RivalDomains(mapId: str):
    StageEvent = util.fetchFehData("Common/SRPG/StageEvent")[mapId]

    content = RDMapInfobox(StageEvent) + '\n'
    content += mapUtil.MapAvailability(StageEvent['avail'], "Update - Special Maps: Rival Domains (Week "+str(int(mapId[1:]))+") (Notification)")
    content += "==Unit data==\n===Enemy AI Settings===\n{{EnemyAI|activeall}}\n===Stats===\n{{RivalDomainsEnemyStats}}\n"
    content += "===List of enemy units===\nThese enemy units make up the brigade for this rival domains:\n{{RDEnemyBrigade|}}\n"
    content += "==Strategy / General Tips==\n*\n"
    content += "==Trivia==\n*\n"
    if mapId in duplicate and len(duplicate[mapId]) == 2:
        GC = int((int(duplicate[mapId][0][1:])-1) / 30) + 1
        content = content[:-1] + "This map layout is the same as Area "+duplicate[mapId][1]+" of [[Grand Conquests "+str(GC)+"|the "+num2words(GC, to="ordinal")+" Grand Conquests event]].\n"
    content += "{{Special Maps Navbox}}"
    return content

from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        if arg[0] == 'Q':
            print(RivalDomains(arg))