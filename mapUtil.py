#! /usr/bin/env python3

from PIL import Image
import re

from util import DATA, DIFFICULTIES, TIME_FORMAT
from reward import parseReward
import util

USE_ALLY_STATS = ['PID_ヘルビンディ味方', 'PID_レーギャルン味方', 'PID_レーヴァテイン味方', 'PID_ロキ味方', 'PID_スルト味方', 'PID_スラシル味方', 'PID_リーヴ味方', 'PID_ヘル味方', 'PID_プルメリア味方']
USE_ENEMY_STATS = ['EID_ヘルビンディ', 'EID_レーギャルン', 'EID_レーヴァテイン', 'EID_ロキ', 'EID_スルト', 'EID_スラシル', 'EID_リーヴ', 'EID_ヘル', 'EID_プルメリア']

WEAPONS = util.fetchFehData("Common/SRPG/Skill")
WEAPONS = {skillTag: WEAPONS[skillTag] for skillTag in WEAPONS if WEAPONS[skillTag]['might'] != 0}
REFINED = [n for n in WEAPONS if WEAPONS[n]['refine_sort_id'] != 0]

REFINED_TYPE = {1: 'Skill1', 2: 'Skill2', 101: 'Atk', 102: 'Spd', 103: 'Def', 104: 'Res'}

def mapTerrain(terrain: list, wallStyle: str, x: int, y: int, useDebris: bool):
    """Return the content of a cell on a terrain, as a string

    Args:
        terrain (list of list of int): The information about content of a map.
        wallStyle (str): The style of walls/box
        x, y (int): The x-y coordinate of the object wanted
        useDebris (bool): Whether to use debris when a wall is desctructible.
    """
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
        template = "Wall"
        if wallStyle[:3] == 'Box':
            template = "Box"
            wallStyle = wallStyle[3:] or "Normal"
            wallType = 'Regular'
        if useDebris:
            return "{{"+template+"|style=" + wallStyle + "|type=" + (t in debris[0] and wallType or ("Debris_" + ((x+y) % 2 == 0 and "A" or "B"))) + "|hp=" + (t in debris[0] and "U" or "0") + "}}"
        else:
            return "{{"+template+"|style=" + wallStyle + "|type=" + wallType + "|hp=" + (t in debris[1] and "1" or t in debris[2] and "2" or "U") + "}}"
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

    path = util.WEBP_ASSETS_DIR_PATH + 'Common/Field/'
    if not mapId in util.fetchFehData("Common/SRPG/Field", 'map_id'):
        path += 'Chip/'

    with Image.open(path + mapId + '.png') as im:
        if 'a' in im.mode or 'A' in im.mode:
            mina, maxa = im.getextrema()[-1]
            if (maxa-mina)/256 > 0.1:
                return True
    return False

def MapImage(field: dict, simpleMap: bool=False, useDebris: bool=False, units: dict=None):
    """
    Args:
        field {
            id (str): The id of the map
            base_terrain (int): The base terrain. 0 is Normal, 1 is Inside, 2 is Desert
            terrain (list of list of int): The content of the cell of the map
            ally_pos, enemy_pos (list of {'x': int, 'y': int}): The position of ally and enemy units
        },
        simpleMap (bool) (False): Use {{MapLayout}} instead of {{#invoke:MapLayout|initTabber}}
        useDebris (bool) (False): Whether to use debris on destructible walls.
        units (dict) (None): Content of a SRPGMap.
    
    Return:
        The map image of a level, as follow:
            "{{#invoke:MapLayout|initTabber
            |baseMap=|backdrop=
            |type=
            |allyPos=
            |enemyPos=
            |f1=|...|f6=
             ...
            |a1=|...|a6=
            }}"
    """
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
            wallStyle = 'normal' if extraField['wall']['filename'] == 'Wallpattern.png' else \
                        'Box' if extraField['wall']['filename'] == 'Boxpattern.png' else \
                        extraField['wall']['filename'][11:-4] if extraField['wall']['filename'][:4] != 'Wall' else \
                        extraField['wall']['filename'][12:-4]
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

    terrain = [['']*6]*8
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
    """
    Args:
        obj: {
            'id_tag',
            'name', 'title', 'epiteth',
            'banner', 'book', 'group', 'mode',
            'map': SRPGMap(['field']+['allypos']),
            'lvl': {diff: ..., ...},
            'rarity': {diff: ..., ...},
            'stam': {diff: ..., ...},
            'reward': {diff: ..., ...},
            'bgms': [...]
        }
        restricted (bool) (False): If True, display only present informations
    
    Returns:
        "{{Battle Infobox
          |bannerImage=
          |stageTitle=
          |stageName=
          |stageEpithet=
          |mapName=
          |bookGroup=
          |mapGroup=
          |mapMode=
          |map=
          |mapImage=
          |lvl=
          |rarity=
          |stam=
          |reward=
          |winReq=
          |bgms=
          |prev=|next=
          }}
        "
        """
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
    bgms = "|BGM="
    for i in range(len(obj["bgms"] if "bgms" in obj else [])):
        if i == 0: bgms += obj["bgms"][i]
        else: bgms += f"\n|BGM{i+1}=" + obj["bgms"][i]
    bgms += "\n"
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
           f"{bgms}" + \
           f"{prevNext}" + \
           "}}\n"

def Availability(avail: dict, notification: str='', type: str="event"):
    """Return an Availabily section.
    
    Args:
        avail {'start', 'finish'}: The start and end time of the event.
        notification (str) (''): The Notification of the event.
        type (str) ("event"): The name of the type of event.
    """
    return "==Availability==\n" + \
          f"This {type} was made available:\n" + \
          "* {{HT|" + avail['start'] + "}} – {{HT|" + util.timeDiff(avail['finish']) + "}} " + \
          "([[" + notification + "|Notification]])"

def MapAvailability(avail: dict, notification: str=None, type: str="map"):
    """Return a Map availabily section. This will store a MapDates.

    Args:
        avail {'start', 'finish'}: The start and end time of the map.
        notification (str) (None): The Notification of the map.
        type (str) ("map"): The name of the type of map.
    """
    endTime = None
    if 'finish' in avail and avail['finish']:
        endTime = util.timeDiff(avail['finish'])

    return "==Map availability==\n" + \
          f"This {type} was made available on:\n" + \
          f"* {{{{MapDates|start={'start' in avail and avail['start'] or ''}" + \
          f"{endTime and ('|end=' + endTime) or ''}" + \
          f"{notification != None and ('|notification=' + notification) or ''}}}}}\n"

def UnitData(SRPGMap):
    """Return the content for a single parameter of Module:UnitData, using a SRPGMap object"""
    s = ""

    for unit in SRPGMap['units']:
        props = 'is_ally,' if 'is_enemy' in unit and not unit['is_enemy'] else '' + \
                'use_ally_stats,' if 'is_enemy' in unit and unit['is_enemy'] and unit['id_tag'] in USE_ALLY_STATS else '' + \
                'use_enemy_stats,' if 'is_enemy' in unit and not unit['is_enemy'] and unit['id_tag'] in USE_ENEMY_STATS else ''
        if props != '' and props[-1] == ',':
            props = props[:-1]

        s += "{"
        s += f"unit={util.getName(unit['id_tag'])};" if 'id_tag' in unit else "unit=;"
        s += f"pos={chr(unit['pos']['x'] + 97)}{unit['pos']['y'] + 1};" if 'pos' in unit else "pos=;"
        s += f"rarity={unit['rarity']};" if 'rarity' in unit else "rarity=;"
        s += f"slot={SRPGMap['units'].index(unit) + 1};" if 'pos' in unit else "slot=;"
        s += f"level={unit['true_lv']};" if 'true_lv' in unit else "level=;"
        s += f"stats=[{unit['stats']['hp']};{unit['stats']['atk']};{unit['stats']['spd']};{unit['stats']['def']};{unit['stats']['res']}];" if 'stats' in unit else "stats=[;;;;];"

        weaponId = unit['skills'][0] if 'skills' in unit else unit['weapon'] if 'weapon' in unit else ''
        weapon = util.getName(WEAPONS[weaponId]['name_id']) if weaponId in WEAPONS else None
        if weaponId in REFINED: weapon += ';refine=' + REFINED_TYPE[WEAPONS[weaponId]['refine_sort_id']]

        s += f"weapon={weapon or '-'};" if weapon else "weapon=;refine=;" if 'refine' in unit else "weapon=;"
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

allLanguages = None
def InOtherLanguage(ids, mapName: str=None, reorder: bool=True):
    """Return the In other languages section.

    Args:
        ids (str/list of str): The id or ids of the object.
        mapName (str) (None): The name of the map. If it is different to the english name, add the english name to the table.
        reorder (bool) (True): Whether Japanese, Italian and Taiwan reverse elements when there is several of them
    """
    global allLanguages
    if not allLanguages:
        allLanguages = util.otherLanguages()
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
    print(InOtherLanguage([argv[1],argv[2]] if len(argv) > 2 else argv[1], "a"))