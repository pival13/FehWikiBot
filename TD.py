#! /usr/bin/env python3

from datetime import datetime

from util import DATA, DIFFICULTIES
import util
import mapUtil

TD_KIND = ['Basics', 'Skill Studies', 'Grandmaster']

def TDMapInfobox(stage: dict, field: dict):
    diff = DIFFICULTIES[stage['difficulty']]

    map = {}
    map['banner'] = 'Banner_Tactics_Drills_' + TD_KIND[stage['difficulty']].replace(" ", "_") + ".png"
    map['id_tag'] = stage['scenario']['id_tag']
    if stage['scenario']['reinforcements']:
        map['mode'] = 'Reinforcement Map'
    map['group'] = 'Tactics Drills: ' + TD_KIND[stage['difficulty']]
    map['stam'] = {diff: 0}
    map['reward'] = {diff: stage['scenario']['reward']}
    map['requirement'] = "Phases to win: " + str(stage['scenario']['turns_to_win'] * 2 - 1 + stage['scenario']['last_enemy_phase'])
    map['bgm'] = "bgm_map_FE14_t.ogg"
    map['map'] = field

    return mapUtil.MapInfobox(map)

def TDText(mapId: str):
    messageEn = util.readFehData("USEN/Message/Scenario/" + mapId + ".json")[0]['value'].replace('\n', '<br>')
    messageJp = util.readFehData("JPJA/Message/Scenario/" + mapId + ".json")[0]['value'].replace('\n', '<br>')
    return "==Text==\n{{TDMessage|" + \
          f"{messageEn}|{messageJp}}}}}\n"

def TDUnitData(SRPGMap: dict, StageEvent):
    return "==Unit data==\n" + \
           "{{#invoke:UnitData|main\n" + \
            (StageEvent['scenario']['reinforcements'] and ("|mapImage=" + mapUtil.MapImage(SRPGMap['field'], True, True) + "\n") or "") + \
           "|" + DIFFICULTIES[StageEvent['difficulty']] + "=" + \
            mapUtil.UnitData(SRPGMap) + "}}\n"

def Solution(SRPGMap: dict):
    return "==Solutions==\n===Text===\n#\n" + \
           "{| class=\"wikitable default mw-collapsed mw-collapsible\"\n! Map visual after the ? enemy phase\n|-\n|" + \
            mapUtil.MapImage(SRPGMap['field'], True) + "\n|}\n"

def TDmap(mapId: str):
    SRPGMap = util.readFehData("Common/SRPGMap/" + mapId + ".json")
    StageEvent = util.fetchFehData("Common/SRPG/StagePuzzle")[mapId]

    startTime = datetime.strptime(StageEvent['avail']['start'], '%Y-%m-%dT%H:%M:%SZ')
    SRPGMap['field'].update({'player_pos': SRPGMap['player_pos']})

    content = TDMapInfobox(StageEvent, SRPGMap['field'])
    content += "\n"
    content += mapUtil.MapAvailability(StageEvent['avail'] or {}, "New Tactics Drills! (" + startTime.strftime("%b %d, %Y").replace(" 0", " ") + ") (Notification)")
    content += TDText(mapId)
    content += TDUnitData(SRPGMap, StageEvent)
    content += Solution(SRPGMap)
    content += mapUtil.InOtherLanguage('MID_STAGE_' + mapId)
    content += "{{Tactics Drills Navbox}}"

    return content

from sys import argv

if __name__ == "__main__":
    print(TDmap(argv[1]))