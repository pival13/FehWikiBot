#! /usr/bin/env python3

from PIL import Image
from datetime import datetime, timedelta

from util import DATA, DIFFICULTIES
from reward import parseReward
import util

USE_ALLY_STATS = ['PID_ヘルビンディ味方', 'PID_レーギャルン味方', 'PID_レーヴァテイン味方', 'PID_ロキ味方', 'PID_スルト味方', 'PID_スラシル味方', 'PID_リーヴ味方']
USE_ENEMY_STATS = ['EID_ヘルビンディ', 'EID_レーギャルン', 'EID_レーヴァテイン', 'EID_ロキ', 'EID_スルト', 'EID_スラシル', 'EID_リーヴ']

REFINED = util.fetchFehData("Common/SRPG/WeaponRefine", "refined")

def mapTerrain(terrain: list, wallStyle: str, x: int, y: int, useDebris: bool):
    walls = [8,9,10,11,12,13,14,19,20,33,34]
    debris = [[8],[9,11,13,19,33],[10,12,14,20,34]]
    if not terrain or len(terrain) < y or len(terrain[y]) < x:
        return ""
    t = terrain[y][x]
    wallType = ""
    if y != len(terrain) -1 and terrain[y+1][x] in walls and (not useDebris or terrain[y+1][x] in debris[0]):
        wallType += "N"
    if x != len(terrain[y]) -1 and terrain[y][x+1] in walls and (not useDebris or terrain[y][x+1] in debris[0]):
        wallType += "E"
    if y != 0 and terrain[y-1][x] in walls and (not useDebris or terrain[y-1][x] in debris[0]):
        wallType += "S"
    if x != 0 and terrain[y][x-1] in walls and (not useDebris or terrain[y][x-1] in debris[0]):
        wallType += "W"
    if wallType == "":
        wallType = "Pillar"
    if t in walls:
        if useDebris:
            return "{{Wall|style=" + wallStyle + "|type=" + (t in debris[0] and wallType or ("Debris_" + ((x+y) % 2 == 0 and "A" or "B"))) + "|hp=" + (t in debris[0] and "U" or "0") + "}}"
        else:
            return "{{Wall|style=" + wallStyle + "|type=" + wallType + "|hp=" + (t in debris[1] and "1" or t in debris[2] and "2" or "U") + "}}"
    return ""

def containDebris(terrain: list):
    for line in terrain:
        for cell in line:
            if cell in [9,11,13,19,33,10,12,14,20,34]:
                return True
    return False

def needBackdrop(mapId):
    if not mapId:
        return True

    path = '../MEmu Download/Data/assets/Common/Field/'
    if not mapId in util.fetchFehData("Common/SRPG/Field", 'map_id'):
        path += 'Chip/'

    with Image.open(path + mapId + '.png') as im:
        if 'a' in im.mode or 'A' in im.mode:
            mina, maxa = im.getextrema()[-1]
            if (maxa-mina)/256 > 0.1:
                return True
    return False

def MapImage(field: dict, simpleMap: bool=False, useDebris: bool=False, units: dict=None):
    mapType = ""
    wallStyle = ""
    backdrop = ""
    allyPos = ""
    enemyPos = ""
    if 'base_terrain' in field and field['base_terrain'] != -1:
        wallStyle = 'normal' if field['base_terrain'] == 0 else 'inside' if field['base_terrain'] == 1 else 'desert' if field['base_terrain'] == 2 else ''
        if 'id' in field and field['id'][0] == 'P':
            mapType = "\n|type=TD"
            backdrop = 'Wave'
        elif 'id' in field and field['id'][0] == 'H':
            mapType = "\n|type=HO"
            backdrop = 'Wave'
    elif 'id' in field:
        extraField = util.fetchFehData("Common/SRPG/Field", "map_id")[field['id']]
        if 'terrain' in field and containDebris(field['terrain']):
            wallStyle = 'normal' if extraField['wall']['filename'] == 'Wallpattern.png' else extraField['wall']['filename'][12:-4]
        backdrop = extraField['backdrop']['filename'][:-11] if extraField['backdrop']['filename'][-11:] == "Pattern.jpg" else extraField['backdrop']['filename'][:-4]

    if 'player_pos' in field and (not simpleMap or field['player_pos']):
        allyPos = "\n|allyPos="
        for ally in field['player_pos']:
            if ally != field['player_pos'][0]:
                allyPos += ','
            allyPos += (str(chr(ally['x'] + 97)) + str(ally['y'] + 1)) if 'x' in ally and 'y' in ally else ''
    if 'enemy_pos' in field and field['enemy_pos']:
        enemyPos = "\n|enemyPos="
        for enemy in field['enemy_pos']:
            if enemy != field['enemy_pos'][0]:
                enemyPos += ','
            enemyPos += (str(chr(enemy['x'] + 97)) + str(enemy['y'] + 1)) if 'x' in enemy and 'y' in enemy else ''

    terrain = None
    if 'terrain' in field:
        terrain = []
        for i in range(len(field['terrain'])):
            terrain += [[]]
            for j in range(len(field['terrain'][i])):
                terrain[i] += [mapTerrain(field['terrain'], wallStyle, j, i, useDebris)] if wallStyle != '' else ''
    if units and terrain:
        for unit in units:
            if unit['spawn_count'] == -1:
                name = util.getName(unit['id_tag'])
                terrain[unit['pos']['y']][unit['pos']['x']] += ('{{Enemy|' if unit['is_enemy'] else '{{Ally|') + \
                                                                ('generic=' if name.find(':') == -1 else 'hero=') + \
                                                                name + '}}'

    return f"{{{{{simpleMap and 'MapLayout' or '#invoke:MapLayout|initTabber'}" + \
           f"\n|baseMap={'id' in field and field['id'] or ''}\n|backdrop={backdrop if 'id' in field and needBackdrop(field['id']) else ''}{mapType}".replace("\n", "" if simpleMap else "\n") + \
           f"{allyPos}{enemyPos}\n" + \
           f"| a8={terrain and terrain[7][0] or ''} | b8={terrain and terrain[7][1] or ''} | c8={terrain and terrain[7][2] or ''} | d8={terrain and terrain[7][3] or ''} | e8={terrain and terrain[7][4] or ''} | f8={terrain and terrain[7][5] or ''}\n" + \
           f"| a7={terrain and terrain[6][0] or ''} | b7={terrain and terrain[6][1] or ''} | c7={terrain and terrain[6][2] or ''} | d7={terrain and terrain[6][3] or ''} | e7={terrain and terrain[6][4] or ''} | f7={terrain and terrain[6][5] or ''}\n" + \
           f"| a6={terrain and terrain[5][0] or ''} | b6={terrain and terrain[5][1] or ''} | c6={terrain and terrain[5][2] or ''} | d6={terrain and terrain[5][3] or ''} | e6={terrain and terrain[5][4] or ''} | f6={terrain and terrain[5][5] or ''}\n" + \
           f"| a5={terrain and terrain[4][0] or ''} | b5={terrain and terrain[4][1] or ''} | c5={terrain and terrain[4][2] or ''} | d5={terrain and terrain[4][3] or ''} | e5={terrain and terrain[4][4] or ''} | f5={terrain and terrain[4][5] or ''}\n" + \
           f"| a4={terrain and terrain[3][0] or ''} | b4={terrain and terrain[3][1] or ''} | c4={terrain and terrain[3][2] or ''} | d4={terrain and terrain[3][3] or ''} | e4={terrain and terrain[3][4] or ''} | f4={terrain and terrain[3][5] or ''}\n" + \
           f"| a3={terrain and terrain[2][0] or ''} | b3={terrain and terrain[2][1] or ''} | c3={terrain and terrain[2][2] or ''} | d3={terrain and terrain[2][3] or ''} | e3={terrain and terrain[2][4] or ''} | f3={terrain and terrain[2][5] or ''}\n" + \
           f"| a2={terrain and terrain[1][0] or ''} | b2={terrain and terrain[1][1] or ''} | c2={terrain and terrain[1][2] or ''} | d2={terrain and terrain[1][3] or ''} | e2={terrain and terrain[1][4] or ''} | f2={terrain and terrain[1][5] or ''}\n" + \
           f"| a1={terrain and terrain[0][0] or ''} | b1={terrain and terrain[0][1] or ''} | c1={terrain and terrain[0][2] or ''} | d1={terrain and terrain[0][3] or ''} | e1={terrain and terrain[0][4] or ''} | f1={terrain and terrain[0][5] or ''}\n" + \
           "}}"

def MapInfobox(obj: dict, restricted: bool=False):
    """obj: {'lvl': {'diff': ..., ...}, 'rarity': {'diff': ..., ...}, 'lvl': {'stam': ..., ...}, 'lvl': {'reward': ..., ...},
             'id_tag', ('name', 'title', 'epiteth'), 'banner', 'book', 'group', 'mode', 'map': SRPGMap(['field']+['allypos'])}"""
    rarity = ""
    stam = ""
    lvl = ""
    reward = "{\n"
    for diff in DIFFICULTIES:
        if 'lvl' in obj and diff in obj['lvl']:
            lvl += "|lvl" + diff + "=" + str(obj['lvl'][diff]) + "\n"
        if 'rarity' in obj and diff in obj['rarity']:
            rarity += "|rarity" + diff + "=" + str(obj['rarity'][diff]) + "\n"
        if 'stam' in obj and diff in obj['stam']:
            stam += "|stam" + diff + "=" + str(obj['stam'][diff]) + "\n"
        if 'reward' in obj and diff in obj['reward']:
            reward += "  " + diff + "=" + parseReward(obj['reward'][diff]) + ";\n"
    reward += "}"
    prevNext = ""

    name = obj['name'] if 'name' in obj else 'id_tag' in obj and 'MID_STAGE_' + obj['id_tag'] in DATA and DATA['MID_STAGE_' + obj['id_tag']] or ''
    title = obj['title'] if 'title' in obj else 'id_tag' in obj and 'MID_STAGE_TITLE_' + obj['id_tag'] in DATA and DATA['MID_STAGE_TITLE_' + obj['id_tag']] or ''
    epithet = obj['epithet'] if 'epithet' in obj else 'id_tag' in obj and 'MID_STAGE_HONOR_' + obj['id_tag'] in DATA and DATA['MID_STAGE_HONOR_' + obj['id_tag']] or ''

    return "{{Battle Infobox\n" + \
           (f"|bannerImage={'banner' in obj and obj['banner'] or ''}\n" if 'banner' in obj or not restricted else "") + \
           (f"|stageTitle={title}\n" if title != '' or not restricted else "") + \
           (f"|stageName={name}\n" if name != '' or not restricted else "") + \
           (f"|stageEpithet={epithet}\n" if epithet != '' or not restricted else "") + \
           (f"|mapName={obj['mapName']}\n" if 'mapName' in obj else "") + \
           (f"|bookGroup={obj['book']}\n" if 'book' in obj else "") + \
           (f"|mapGroup={'group' in obj and obj['group'] or ''}\n" if 'group' in obj or not restricted else "") + \
           (f"|mapMode={obj['mode']}\n" if 'mode' in obj and obj['mode'] else "") + \
           (f"|map={obj['id_tag']}\n" if not 'map' in obj and 'id_tag' in obj else "") + \
           (f"|mapImage={MapImage('map' in obj and obj['map'] or {})}\n" if 'map' in obj or not restricted else "") + \
           f"{lvl}{rarity}{stam}" + \
           f"|reward={reward}\n" + \
           (f"|winReq={'requirement' in obj and obj['requirement'] or ''}\n" if 'requirement' in obj or not restricted else "") + \
           (f"|BGM={'bgm' in obj and obj['bgm'] or ''}\n" if 'bgm' in obj or not restricted else "") + \
           (f"|BGM2={'bgm2' in obj and obj['bgm2'] or ''}\n" if 'bgm2' in obj else "") + \
           f"{prevNext}" + \
           "}}\n"

def MapAvailability(avail: dict, notification: str=None, type: str="map"):
    endTime = None
    if 'finish' in avail and avail['finish']:
        endTime = datetime.strptime(avail['finish'], '%Y-%m-%dT%H:%M:%SZ') - timedelta(seconds=1)

    return "==Map availability==\n" + \
          f"This {type} was made available on:\n" + \
          f"* {{{{MapDates|start={'start' in avail and avail['start'] or ''}" + \
          f"{endTime and ('|end=' + endTime.strftime('%Y-%m-%dT%H:%M:%SZ')) or ''}" + \
          f"{notification != None and ('|notification=' + notification) or ''}}}}}\n"

def UnitData(SRPGMap):
    s = ""

    for unit in SRPGMap['units']:
        props = 'is_ally,' if 'is_enemy' in unit and not unit['is_enemy'] else '' + \
                'use_ally_stats,' if 'is_enemy' in unit and unit['is_enemy'] and unit['id_tag'] in USE_ALLY_STATS else '' + \
                'use_enemy_stats,' if 'is_enemy' in unit and not unit['is_enemy'] and unit['id_tag'] in USE_ENEMY_STATS else ''
        if props != '' and props[-1] == ',':
            props = props[:-1]

        #if SRPGMap['field']['id'][0] == 'W' and unitsQuery[unit['id_tag']] and unitsQuery[unit['id_tag']].isGeneric != '':
        #    unitArgs = compact_hash {
        #        {'pos', string.char(unit['pos'].x + 97) + tostring(unit['pos'].y + 1)},
        #        {'rarity', unit['rarity']},
        #        {'slot', slot},
        #        {'level', unit['true_lv']},
        #        {'displaylevel', unit['true_lv'] != unit['lv'] and unit['lv']},
        #        {'ai', unit['is_enemy'] and compact_hash {
        #            {'turn', unit['start_turn'] != -1 and unit['start_turn']},
        #            {'group', unit['movement_group'] != -1 and unit['movement_group']},
        #            {'delay', unit['movement_delay'] != -1 and unit['delay']},
        #            {'break_walls', unit['break_terrain'] and '1'},
        #            {'tether', unit['tether'] and '1'},
        #        }},
        #        {'random', compact_hash {
        #            {'moves', unitsQuery[unit['id_tag']].Moves},
        #            {'weapons', unitsQuery[unit['id_tag']].Weapons},
        #            {'staff', unitsQuery[unit['id_tag']].Weapons == 'Ranged' and 'false'},
        #        }},
        #    }
        #else:
        s += "{"
        s += f"unit={util.getName(unit['id_tag'])};" if 'id_tag' in unit else "unit=;"
        s += f"pos={chr(unit['pos']['x'] + 97)}{unit['pos']['y'] + 1};" if 'pos' in unit else "pos=;"
        s += f"rarity={unit['rarity']};" if 'rarity' in unit else "rarity=;"
        s += f"slot={SRPGMap['units'].index(unit) + 1};" if 'pos' in unit else "slot=;"
        s += f"level={unit['true_lv']};" if 'true_lv' in unit else "level=;"
        s += f"stats=[{unit['stats']['hp']};{unit['stats']['atk']};{unit['stats']['spd']};{unit['stats']['def']};{unit['stats']['res']}];" if 'stats' in unit else "stats=[;;;;];"

        weapon = util.getName(unit['skills'][0]) if 'skills' in unit else None
        if weapon and weapon == unit['skills'][0]:
            weapon = util.getName(REFINED[unit['skills'][0]]['orig']) + ";refine="
            if unit['skills'][0][-3:] == "ATK":
                weapon += 'Atk'
            elif unit['skills'][0][-3:] == "AGI":
                weapon += 'Spd'
            elif unit['skills'][0][-3:] == "DEF":
                weapon += 'Def'
            elif unit['skills'][0][-3:] == "RES":
                weapon += 'Res'
            elif unit['skills'][0][-2:] == "_幻":
                weapon += 'Skill2'
            else:
                weapon += 'Skill1'
        elif not weapon and 'refine' in unit:
            weapon = ";refine="
        s += f"weapon={weapon or '-'};" if weapon else "weapon=;"
        s += f"assist={util.getName(unit['skills'][1]) or '-'};" if 'skills' in unit else "assist=;"
        s += f"special={util.getName(unit['skills'][2]) or '-'};" if 'skills' in unit else "special=;"
        s += f"cooldown={unit['cooldown_count'] or ''};" if 'cooldown_count' in unit and unit['cooldown_count'] != -1 else ''
        s += f"a={util.getName(unit['skills'][3]) or '-'};" if 'skills' in unit else "a=;"
        s += f"b={util.getName(unit['skills'][4]) or '-'};" if 'skills' in unit else "b=;"
        s += f"c={util.getName(unit['skills'][5]) or '-'};" if 'skills' in unit else "c=;"
        s += f"seal={util.getName(unit['skills'][6]) or '-'};" if 'skills' in unit else "seal=;"
        s += f"accessory={util.getName(unit['accessory'])};" if 'accessory' in unit and unit['accessory'] else ''
        s += f"properties={props};" if props != '' else ''

        if not 'is_enemy' in unit or unit['is_enemy']:
            s += "ai={"
            s += f"turn={unit['start_turn']};" if 'start_turn' in unit and unit['start_turn'] != -1 else ''
            s += f"group={unit['movement_group']};" if 'movement_group' in unit and unit['movement_group'] != -1 else ''
            s += f"delay={unit['movement_delay']};" if 'movement_delay' in unit and unit['movement_delay'] != -1 else ''
            s += "break_walls=1;" if 'break_terrain' in unit and unit['break_terrain'] else ''
            s += "tether=1;" if 'tether' in unit and unit['tether'] else ''
            s = (s[:-1] if s[-1] == ';' else s) + "};"
        if 'spawn_count' in unit and unit['spawn_count'] != -1:
            s += "spawn={"
            s += f"turn={unit['spawn_turns']+1};" if 'spawn_turns' in unit and unit['spawn_turns'] != -1 else ''
            s += f"count={unit['spawn_count']};" if 'spawn_count' in unit and unit['spawn_count'] > 1 else ''
            s += f"target={util.getName(unit['spawn_check'])};" if 'spawn_check' in unit and unit['spawn_check'] else ''
            s += f"remain={unit['spawn_target_remain']};" if 'spawn_target_remain' in unit and unit['spawn_target_remain'] != -1 else ''
            s += f"kills={unit['spawn_target_kills']};" if 'spawn_target_kills' in unit and unit['spawn_target_kills'] != -1 else ''
            s = (s[:-1] if s[-1] == ';' else s) + "};"

        s = (s[:-1] if s[-1] == ';' and s[-2] != '}' else s) + "};\n"

    return f"[\n{s}]"

allLanguages = util.otherLanguages()
def InOtherLanguage(ids, mapName: str=None, reorder: bool=True):
    if type(ids) is str:
        ids = [ids]
    usen = ""
    jpja = ""
    eude = ""
    eues = ""
    uses = ""
    eufr = ""
    euit = ""
    twzh = ""
    uspt = ""
    for id in ids:
        languages = allLanguages[id]
        usen += languages['USEN'] if usen == "" else (": " + languages['USEN'])
        jpja = languages['JPJA'] if jpja == "" else (languages['JPJA'] + '　' + jpja) if reorder else (jpja + '　' + languages['JPJA'])
        eude += languages['EUDE'] if eude == "" else (': ' + languages['EUDE'])
        eues += languages['EUES'] if eues == "" else (': ' + languages['EUES'])
        uses += languages['USES'] if uses == "" else (': ' + languages['USES'])
        eufr += languages['EUFR'] if eufr == "" else (' : ' + languages['EUFR'])
        euit = languages['EUIT'] if euit == "" else (languages['EUIT'] + ': ' + euit) if reorder else (euit + ", " + languages['EUIT'])
        twzh = languages['TWZH'] if twzh == "" else (languages['TWZH'] + '　' + twzh) if reorder else (twzh + '　' + languages['TWZH'])
        uspt += languages['USPT'] if uspt == "" else (': ' + languages['USPT'])

    en = f"|english={usen}\n"
    return "==In other languages==\n{{OtherLanguages\n" + \
        f"{mapName and mapName != usen and en or ''}" + \
        f"|japanese={jpja}\n" + \
        f"|german={eude}\n" + \
        f"|spanishEU={eues}\n" + \
        f"|spanishLA={uses}\n" + \
        f"|french={eufr}\n" + \
        f"|italian={euit}\n" + \
        f"|chineseTW={twzh}\n" + \
        f"|portuguese={uspt}\n" + \
        "}}\n"

from sys import argv

if __name__ == '__main__':
    #for i in range(75,30,-1):
    #    print(InOtherLanguage(["MID_STAGE_T00"+str(i),"MID_STAGE_HONOR_T00"+str(i)], "a"))
    print(InOtherLanguage([argv[1],argv[2]] if len(argv) > 2 else argv[1], "a"))