#! /usr/bin/env python3

import re
import json
from sys import stderr
from num2words import num2words

import util
import mapUtil
from wikiUtil import _exportPage
from globals import DIFFICULTIES, ERROR, UNIT_NAMES

WEAPON_NAME = ['剣', '槍', '斧', '弓', '弓', '弓', '弓', '暗器', '暗器', '暗器', '暗器']
MAGIC_NAME = [['','',''],['ファイアー','エルファイアー','ボルガノン'],['サンダー','エルサンダー','トロン'],['ウインド','エルウインド','レクスカリバー'],['ライト','エルライト','シャイン'],['ミィル','ルイン','ノスフェラート'],['ロック','エルロック','アトラース']]
BEAST_NAME = ['歩行', '重装', '騎馬', '飛行']

def exportEventMap(mapId1: str, mapId2: str=None):
    if mapId2:
        content = EventGroup(mapId1, mapId2)
    else:
        content = {util.getName(mapId1): EventMap(mapId1)}
    append = ""

    for name in content:
        success = False
        while not success:
            result = _exportPage(name + append, content[name], 'Bot: new Event Map', create=True)
            if 'edit' in result and result['edit']['result'] == 'Success':
                success = True
            else:
                append = util.askAgreed(f"\"{name}\" already exist. Should something be append to the name?", useTrueDefault=False, askTrue="What should be append?")
                if not append:
                    break

def getDefaultWeapon(unit: dict, diff: int, level: int):
    weapon = unit['weapon_type']
    if diff == 0 and level == 5:
        if weapon < len(WEAPON_NAME):
            return "SID_鉄の"+WEAPON_NAME[weapon]
        elif weapon >= 11 and weapon <= 14:
            return "SID_"+MAGIC_NAME[unit['tome_class']][0]
        elif weapon == 15:#Staff
            return "SID_アサルト"
        elif weapon >= 16 and weapon <= 19:#Breath
            return "SID_火のブレス"
        elif weapon >= 20 and weapon <= 23:#Beast
            return "SID_幼獣の化身・" + BEAST_NAME[unit['move_type']]
    elif diff == 1 and level == 15:
        if weapon < len(WEAPON_NAME):
            return "SID_鋼の"+WEAPON_NAME[weapon]
        elif weapon >= 11 and weapon <= 14:
            return "SID_"+MAGIC_NAME[unit['tome_class']][1]
        elif weapon == 15:#Staff
            return "SID_アサルト"
        elif weapon >= 16 and weapon <= 19:#Breath
            return "SID_火炎のブレス"#SID_灼熱のブレス
        elif weapon >= 20 and weapon <= 23:#Beast
            return "SID_若獣の化身・" + BEAST_NAME[unit['move_type']]#成獣の化身・
    return ""

def EventMapInfobox(StageEvent: dict, group: str):
    info = {
        'id_tag': StageEvent['id_tag'],
        'banner': 'Banner ' + StageEvent['banner_id'] + '.webp',
        'group': group,
        'requirement': [],
        'lvl': {}, 'rarity': {}, 'stam': {}, 'reward': {},
        'map': {'id': StageEvent['id_tag'], 'player_pos': []},
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

    allyPos = util.askFor(r"([a-f][1-8],){3}[a-f][1-8]", f"What is the players position in \"{util.getName(StageEvent['id_tag'])}\" ({StageEvent['id_tag']})?") or ""
    backdrop = util.askFor(r"Lava|Wave|.+Pattern.+", f"What is the map backdrop in \"{util.getName(StageEvent['id_tag'])}\" ({StageEvent['id_tag']})?") or ""
    return mapUtil.MapInfobox(info).replace("|allyPos=", "|allyPos="+allyPos).replace("|backdrop=", "|backdrop="+backdrop)

def EventUnitData(StageEvent: dict, weaponKind):    
    askedUnits = []
    asked = True
    print(f"Following will be asked the units for \"{util.getName(StageEvent['id_tag'])}\" ({StageEvent['id_tag']}). Its format is \"[unit] [pos]\" or \"[unit] ??\". If it does not follow this format, it will be considered as the end of the unit listing.", file=stderr)
    while asked:
        asked = util.askFor(r".+ ([a-f][1-8]|\?\?)", f"{num2words(len(askedUnits)+1, to='ordinal').capitalize()} enemy unit:")
        if asked:
            askedUnits += [{'unit': asked[:-3], 'pos': asked[-2:]}]
            if not askedUnits[-1]['unit'] in UNIT_NAMES:
                print(ERROR + "Unknow unit: "+askedUnits[-1]['unit'], file=stderr)
                askedUnits.remove(askedUnits[-1])
            elif askedUnits[-1]['pos'] == '??':
                askedUnits[-1]['pos'] = None

    s = "==Unit data==\n"
    s += "{{#invoke:UnitData|main|globalai="
    if StageEvent['scenarios'][-1]['reinforcements']:
        s += "\n|mapImage=" + mapUtil.MapImage({'id': StageEvent['id_tag']}, simpleMap=True, useDebris=True)

    for idiff in range(StageEvent['scenario_count']):
        s += '\n|' + DIFFICULTIES[StageEvent['scenarios'][idiff]['difficulty']] + '='
        units = []
        for i in range(len(askedUnits)):
            units += [{'id_tag': UNIT_NAMES[askedUnits[i]['unit']]['id_tag'], 'rarity': StageEvent['scenarios'][idiff]['stars'], 'true_lv': StageEvent['scenarios'][idiff]['true_lv']}]
            u = UNIT_NAMES[askedUnits[i]['unit']]
            units[i]['weapon'] = u['skills'][4][0] if 'skills' in u and (weaponKind == 'P' or (weaponKind == 'D' and len(util.cargoQuery("Units", where="_pageName='"+askedUnits[i]['unit'].replace("'", "\\'")+"' AND (Properties__full LIKE \"%special%\" OR Properties__full LIKE \"%specDisplay%\")")) != 0)) else \
                                 util.askFor("", f"Weapon for \"{askedUnits[i]['unit']}\" at difficulty {DIFFICULTIES[StageEvent['scenarios'][idiff]['difficulty']]}:") if weaponKind == 'C' else \
                                 getDefaultWeapon(u, StageEvent['scenarios'][idiff]['difficulty'], StageEvent['scenarios'][idiff]['true_lv'])
        if StageEvent['scenarios'][idiff]['reinforcements']:
            units += [{'rarity': StageEvent['scenarios'][idiff]['stars'], 'true_lv': StageEvent['scenarios'][idiff]['true_lv'], 'spawn_count': 0}]
        s += mapUtil.UnitData({'units': units})
        for i in range(len(askedUnits)):
            s = s.replace(";pos=;", ";pos="+(askedUnits[i]['pos'] or '@@@')+";", 1)
                 #.replace(";weapon=;", ";weapon="++";", 1)
    return s.replace('@@@', '').replace('Fire Breath+', 'Fire Breath-').replace('+;', ';').replace('Fire Breath-', 'Fire Breath+') + "\n}}\n"

def EventMap(mapId: str, kindUnitWeapon=None, event=None, notif=None):
    if event is None:
        event = util.askAgreed(f"Is \"{util.getName(mapId)}\" ({mapId}) related to the event \"{util.getName('MID_STAGE_HONOR_'+mapId)}\"?", defaultTrue=util.getName('MID_STAGE_HONOR_'+mapId), askFalse="Then what is it related to?")
    if notif is None:
        notif = util.askFor(r".+ \(Notification\)", f"Which notification is \"{util.getName(mapId)}\" ({mapId}) related to?") or ""
    while not kindUnitWeapon:
        kindUnitWeapon = util.askFor(r"Personal|Default|Full Default|Custom|P|D|C|F", f"How should be interpreted units weapon on \"{util.getName(mapId)}\" ({mapId})? Enter one of: Personal / P (Use their unique personal weapon), Default / D (Use rank 1 and 2 weapon for regular units, personal weapon for special units), Full Default / F (Use their rank 1 and 2 weapon), Custom / C.", 1)
    kindUnitWeapon = kindUnitWeapon[0].upper()
    
    StageEvent = util.fetchFehData('Common/SRPG/StageEvent')[mapId]

    content = EventMapInfobox(StageEvent, event) + "\n"
    content += mapUtil.MapAvailability(StageEvent['avail'], notif, f"map is part of the [[{event} (Event)|{event}]] event and")
    content += EventUnitData(StageEvent, kindUnitWeapon)
    content += mapUtil.InOtherLanguage(["MID_STAGE_"+mapId, "MID_STAGE_HONOR_"+mapId], util.getName("MID_STAGE_"+mapId)+": "+event)
    content += "{{Special Maps Navbox}}\n[[Category:Event maps]]"
    return content

def EventGroup(mapId1: str, mapId2: str):
    begin = int(mapId1[1:])
    end = int(mapId2[1:])

    event = util.askAgreed(f"Are those maps ({mapId1}-{mapId2}) related to the event \"{util.getName('MID_STAGE_HONOR_'+mapId1)}\"?", defaultTrue=util.getName('MID_STAGE_HONOR_'+mapId1), askFalse="Then what are they related to?")
    notif = util.askFor(r".+ \(Notification\)", "Which notification are they related to?") or ""
    weaponKind = None
    while not weaponKind:
        weaponKind = util.askFor(r"Personal|Default|Full Default|Custom|P|D|C|F", f"How should be interpreted units weapon on those maps ({mapId1}-{mapId2})? Enter one of: Personal / P (Use their unique personal weapon), Default / D (Use rank 1 and 2 weapon for regular units, personal weapon for special units), Full Default / F (Use their rank 1 and 2 weapon), Custom / C.", 1)
    weaponKind = weaponKind[0].upper()

    content = {}
    for mId in range(begin, end+1):
        content.update({util.getName(f"MID_STAGE_V{mId:04}")+f": {event}":
            EventMap(f"V{mId:04}", weaponKind, event, notif)})
    return content

def readPersonalJson(file: str):
    js = json.load(open(file))
    print(js['event'])
    print(js['notification'])
    print(js['weaponType'])
    for m in js['maps']:
        print(m['pos'])
        print(m['backdrop'])
        for u in m["units"]:
            print(u['name'] + " " + u['pos'])
        print("")
    return

from sys import argv

if __name__ == '__main__':
    if len(argv) == 3 and re.match(r"^V\d{4}$", argv[1]) and re.match(r"^V\d{4}$", argv[2]) and int(argv[1][1:]) < int(argv[2][1:]):
        print(json.dumps(EventGroup(argv[1], argv[2]), indent=2))
    elif len(argv) == 2 and re.match(r"^V\d{4}$", argv[1]):
        print(json.dumps(EventMap(argv[1]), indent=2))
    elif len(argv) == 2:
        readPersonalJson(argv[1])