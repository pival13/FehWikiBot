#! /usr/bin/env python3

from PIL import Image
from datetime import datetime, timedelta
import re

from util import DATA, DIFFICULTIES
from reward import parseReward
import util

USE_ALLY_STATS = ['PID_ヘルビンディ味方', 'PID_レーギャルン味方', 'PID_レーヴァテイン味方', 'PID_ロキ味方', 'PID_スルト味方', 'PID_スラシル味方', 'PID_リーヴ味方']
USE_ENEMY_STATS = ['EID_ヘルビンディ', 'EID_レーギャルン', 'EID_レーヴァテイン', 'EID_ロキ', 'EID_スルト', 'EID_スラシル', 'EID_リーヴ']

REFINED = util.fetchFehData("Common/SRPG/WeaponRefine", "refined")
SKILLS = util.fetchFehData("Common/SRPG/Skill")

def mapTerrain(terrain: list, wallStyle: str, x: int, y: int, useDebris: bool):
    walls = [8,9,10,11,12,13,14,19,20,33,34]
    debris = [[8],[9,11,13,19,33],[10,12,14,20,34]]
    other = {
        36: "{{RBTerrain}}", 37: "{{RBTerrain}}", 38: "{{RBTerrain}}", 39: "{{RBTerrain}}",
    }
    if not terrain or len(terrain) < y or len(terrain[y]) < x:
        return ""
    t = terrain[y][x]
    if t in other:
        return other[t]

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
        elif 'id' in field and field['id'][0] == 'Y':
            mapType = "\n|type=RD"
            backdrop = 'Wave'
    elif 'id' in field and field['id'][0] != 'V':
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

    terrain = [[]]
    if 'terrain' in field:
        terrain = list(['' for _ in range(len(field['terrain'][i]))] for i in range(len(field['terrain'])))
        for i in range(len(field['terrain'])):
            for j in range(len(field['terrain'][i])):
                terrain[i][j] += mapTerrain(field['terrain'], wallStyle, j, i, useDebris) if wallStyle != '' else ''
    if units and terrain:
        for unit in units:
            if unit['spawn_count'] == -1:
                name = util.getName(unit['id_tag'])
                terrain[unit['pos']['y']][unit['pos']['x']] += ('{{Enemy|' if unit['is_enemy'] else '{{Ally|') + \
                                                                ('generic=' if name.find(':') == -1 else 'hero=') + \
                                                                name + '}}'

    s = f"{{{{{simpleMap and 'MapLayout' or '#invoke:MapLayout|initTabber'}" + \
        f"\n|baseMap={'id' in field and field['id'] or ''}\n|backdrop={backdrop if backdrop != '' and 'id' in field and needBackdrop(field['id']) else ''}{mapType}".replace("\n", "" if simpleMap else "\n") + \
        f"{allyPos}{enemyPos}\n"
    for y in range(len(terrain)-1, -1, -1):
        for x in range(len(terrain[y])):
            s += "| " + chr(x+97) + str(y+1) + "=" + terrain[y][x] + " "
        s = s[:-1] + "\n"
    s += "}}"
    return s

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

        weaponId = unit['skills'][0] if 'skills' in unit else unit['weapon'] if 'weapon' in unit else ''
        weapon = util.getName(SKILLS[weaponId]['name_id']) if weaponId in SKILLS else None
        if weapon and "M" + weaponId != SKILLS[weaponId]['name_id']:
            weapon += ';refine=' + ("Atk" if weaponId[-3:] == 'ATK' else
                                    "Spd" if weaponId[-3:] == 'SPD' else
                                    'Def' if weaponId[-3:] == 'DEF' else
                                    'Res' if weaponId[-3:] == 'RES' else
                                    'Skill2' if weaponId[-2:] == "_幻" else 'Skill1')

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
    if len(argv) == 2 and len(argv[1]) == 5 and argv[1][0] == 'Y':
        maps = util.fetchFehData('Common/SRPGMap')
        for m in maps:
            if m['field']['id'] == argv[1]:
                m['field']['player_pos'] = m['player_pos']
                print(re.sub("hero=[^}]+", "hero=", MapImage(m['field'], simpleMap=True, units=m['units'])).replace("Red Thief", "Thief").replace("Blue Thief", "Thief").replace("Green Thief", "Thief"))
    else:
        print(InOtherLanguage([argv[1],argv[2]] if len(argv) > 2 else argv[1], "a"))