#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool.Container import Container
from .Reader.Terrain import MapReader, EnvironmentReader, CellEnvironmentReader, TerrainReader

class CellEnvironment(Container):
    _reader = CellEnvironmentReader

class Environment(Container):
    _reader = EnvironmentReader

    @classmethod
    def load(cls, name: str) -> bool:
        if not super().load(name):
            return False
        CellEnvironment.load(name)

        datas = cls._DATA.get(name)
        for data in (datas.values() if isinstance(datas, dict) else datas or []):
            data['@Cell'] = CellEnvironment.get(data['cell_env_id']).data if CellEnvironment.get(data['cell_env_id']) else None
        return True

class Terrain(Container):
    _reader = TerrainReader
    _key = 'index'

    @classmethod
    def load(cls, name: str) -> bool:
        return name == 'Terrain' and super().load(name)

    @classmethod
    def fromUnique(cls): return cls.fromAssets('Terrain')

class Map(Container):
    _reader = MapReader
    _key = None

    @classmethod
    def load(cls, name: str) -> bool:
        if not super().load(name):
            return False
        Environment.load('')

        datas = cls._DATA.get(name)
        for data in (datas.values() if isinstance(datas, dict) else datas or []):
            if data['terrain']['type'] == None:
                env = Environment.get(data['terrain']['map_id']).data if Environment.get(data['terrain']['map_id']) else None
            else:
                i = {v:k for k,v in MapReader.TERRAIN_TYPE.items()}[data['terrain']['type']]
                env = Environment.get(f'CHIP{i}').data if Environment.get(f'CHIP{i}') else None
            data['terrain']['@Environment'] = env
        
        return True

    @classmethod
    def get(cls, key: str):
        ret = cls.fromAssets(key)
        if len(ret) > 0: return ret[0]
        ret = cls.getAll(key)
        if len(ret) > 0: return ret[-1]
        return None

    @classmethod
    def getAll(cls, mapId):
        maps = cls.fromAssets(mapId)
        for l in ['A','B','C','D','E','F','G','H']:
            maps += cls.fromAssets(mapId+l)
        return maps

    PLACEHOLDER_UNIT = {'unit': '', 'pos': '', 'rarity': '', 'true_lv': '', 'stats': {'hp':'','atk':'','spd':'','def':'','res':''}, 'weapon': None, 'assist': None, 'special': None, 'init_cooldown': 0, 'a': None, 'b': None, 'c': None, 'attuned': None, 'seal': None, 'accessory': None, 'playable': False, 'nb_spawn': 0}

    @classmethod
    def create(cls, mapId, placeholderEnemy=1):
        Environment.load('')
        o = cls()
        mapId2 = mapId if mapId[-1] not in 'ABCDEFG' else mapId[:-1]
        o.data = {
            'terrain': {'type': None, 'map_id': mapId2, 'ground': [['']*6]*8},
            'units': [], 'starting_pos': [''], 'enemy_pos': ['']
        }
        o.data['terrain']['@Environment'] = Environment.get(mapId2).data if Environment.get(mapId2) else None
        for _ in range(placeholderEnemy):
            o.data['units'].append(cls.PLACEHOLDER_UNIT.copy())
        cls._DATA[mapId] = o.data
        return o

    @property
    def baseMap(self) -> str:
        return self.data['terrain']['map_id']

    @property
    def background(self) -> str:
        if (self.data['terrain'].get('@Environment') or {}).get('underlay') is None: return ''
        if self.data['terrain']['@Environment']['underlay']['file'] == 'WavePattern.jpg': return 'Wave'
        if self.data['terrain']['@Environment']['underlay']['file'] == 'LavaPattern.jpg': return 'Lava'
        return self.data['terrain']['@Environment']['underlay']['file'][:-4]

    @property
    def wallStyle(self) -> str:
        if (self.data['terrain'].get('@Environment') or {}).get('walls') is None: return ''
        elif self.data['terrain']['@Environment']['walls']['file'] == 'Wallpattern.png': return 'normal'
        elif self.data['terrain']['@Environment']['walls']['file'] == 'Boxpattern.png': return 'Box'
        elif self.data['terrain']['@Environment']['walls']['file'] == 'IcePattern.png': return 'IceBox'
        else: return self.data['terrain']['@Environment']['walls']['file'][12:-4]

    def Image(self, useDebris: bool=False, shortest: bool=False):
        mapType = None
        if self.baseMap[:2] in ('PA','PB','PC'):
            mapType = 'TD'
        elif self.baseMap[0] in ('H'):
            mapType = 'HO'
        elif self.baseMap[0] in ('Q','O','Y'):
            mapType = 'RD'
        elif self.baseMap[:2] in ('ZR'):
            mapType = 'SD'

        terrain = []
        if self.needWall():
            for y,row in enumerate(self.data['terrain']['ground']):
                terrain.append([])
                for x in range(len(row)):
                    terrain[y].append(self.mapCell(x,y,useDebris))
        elif not shortest:
            terrain = [['']*len(row) for row in self.data['terrain']['ground']]

        s =  '{{#invoke:MapLayout|initTabber\n' if not shortest else ('{{MapLayout' + ('\n' if terrain != [] else ''))
        s +=  '|baseMap=' + self.baseMap + ('\n' if not shortest else '')
        if self.needBackground():
            s += '|backdrop=' + self.background + ('\n' if not shortest else '')
        elif not shortest:
            s += '|backdrop=\n'
        if mapType is not None:
            s += '|type=' + mapType + ('\n' if not shortest else '')
        if len(self.data.get('starting_pos') or []) > 0:
            s += '|allyPos=' + ','.join(self.data['starting_pos']) + ('\n' if not shortest else '')
        if len(self.data.get('enemy_pos') or []) > 0:
            s += '|enemyPos=' + ','.join(self.data['enemy_pos']) + ('\n' if not shortest else '')
        if shortest and terrain != []: s += '\n'
        for y,row in list(enumerate(terrain))[::-1]:
            for x,cell in enumerate(row):
                s += '| ' + chr(x+97) + str(y+1) + '=' + cell + ' '
            s = s[:-1] + '\n'
        s += '}}'
        return s

    def needWall(self):
        if self.data['terrain'] is None: return False
        # /Chip maps
        if self.data['terrain']['type'] is not None: return True
        # Contains breakable walls
        for row in self.data['terrain']['ground']:
            for cell in row:
                if cell in [9,11,13,19,33,10,12,14,20,34]:
                    return True
        return False

    def needBackground(self):
        from os.path import exists
        from ..PersonalData import WEBP_ASSETS_DIR_PATH
        from PIL import Image
        if self.data['terrain'] is None: return False
        
        filepath = WEBP_ASSETS_DIR_PATH + 'Common/Field/' + ('Chip/' if self.data['terrain']['type'] is not None else '') + self.baseMap + '.png'
        if not exists(filepath): return False
        with Image.open(filepath) as img:
            if ('a' in img.mode or 'A' in img.mode) and img.getextrema()[-1][0] < 0xF0:
                return True
        return False

    def mapCell(self, x, y, useDebris:bool=False) -> str:
        if not (self.data['terrain'] or {'ground':None})['ground'] or y >= len(self.data['terrain']['ground']) or x >= len(self.data['terrain']['ground'][y]): return ''

        WALLS = [8,9,10,11,12,13,14,19,20,33,34]
        DEBRIS = [[8],[9,11,13,19,33],[10,12,14,20,34]] # Wall, 1HP, 2HP
        OTHERS = {
            36: '{{RBTerrain}}', 37: '{{RBTerrain}}', 38: '{{RBTerrain}}', 39: '{{RBTerrain}}',
        }

        map = self.data['terrain']['ground']
        if map[y][x] in OTHERS: return OTHERS[map[y][x]]
        if map[y][x] not in WALLS: return ''

        style = self.wallStyle
        type = ''
        if y != len(map)-1 and map[y+1][x] in WALLS and (not useDebris or map[y+1][x] in DEBRIS[0]):
            type += 'N'
        if x != len(map[y])-1 and map[y][x+1] in WALLS and (not useDebris or map[y][x+1] in DEBRIS[0]):
            type += 'E'
        if y != 0 and map[y-1][x] in WALLS and (not useDebris or map[y-1][x] in DEBRIS[0]):
            type += 'S'
        if x != 0 and map[y][x-1] in WALLS and (not useDebris or map[y][x-1] in DEBRIS[0]):
            type += 'W'
        if type == '':
            type = 'Pillar'

        if style[:3] == 'Box':
            s = '{{Box'
            style = 'Normal' if style == 'Box' else style
            type = 'Regular'
        elif style not in ['normal','inside','BraveBoss','insideJP','desert','Easter','Souen','wedding','Muspel','Hell']:
            s = '{{#invoke:MapLayout|wall'
        else:
            s = '{{Wall'
        s += '|style=' + style
        if useDebris and map[y][x] not in DEBRIS[0]:
            s += '|type=Debris_' + ((x+y) % 2 == 0 and 'A' or 'B')
            s += '|hp=0'
        else:
            s += '|type=' + type
            s += '|hp=' + ('1' if map[y][x] in DEBRIS[1] else '2' if map[y][x] in DEBRIS[2] else 'U')
        return s + '}}'

    def CombatBackgrounds(self) -> list[list[str]]:
        ground = []
        for row in self.data['terrain']['ground']:
            ground.append([])
            for cell in row:
                ground[-1].append(self.data['terrain']['@Environment']['@Cell'][Terrain.get(cell).data['category']]['background'])
        return ground


    @classmethod
    def UnitData(cls, maps: dict[str,Self]):
        s =  '==Unit data==\n'
        s += '{{#invoke:UnitData|main\n'
        if any(map.hasReinforcements() for map in maps.values()):
            s += '|mapImage=' + list(maps.values())[0].Image(True, True) + '\n'
        for diff,map in maps.items():
            s += '|' + diff + '=' + map.Units() + '\n'
        s += '}}'
        return s

    @classmethod
    def Unit(cls, unit, i=None):
        from ..Utility.Units import Units, Heroes, Enemies
        from ..Skills import Weapon, Assist, Special, Passive
        from ..Others.Accessory import Accessories
        s =  '{'
        s += f"unit={Units.get(unit['unit']).name if Units.get(unit['unit']) else ''};"
        s += f"pos={unit['pos']};"
        s += f"slot={i+1};" if unit['pos'] and i != None else "slot=;"
        s += f"rarity={unit['rarity']};"
        s += f"level={unit['true_lv']};"
        s += f"stats=[{unit['stats']['hp']};{unit['stats']['atk']};{unit['stats']['spd']};{unit['stats']['def']};{unit['stats']['res']}];"
        if isinstance(unit['weapon'],Weapon):
            s += f"weapon={unit['weapon'].name};"
            if unit['weapon'].refine: s += f"refine={unit['weapon'].refine};"
        else:
            wep = Weapon.get(unit['weapon'])
            if wep and wep.refine: s += f"weapon={wep.name};refine={wep.refine};"
            else:                  s += f"weapon={wep.name if wep else '-'};"
        s += f"assist={unit['assist'].name if isinstance(unit['assist'],Assist) else Assist.get(unit['assist']).name if unit['assist'] else '-'};"
        s += f"special={unit['special'].name if isinstance(unit['special'],Special) else Special.get(unit['special']).name if unit['special'] else '-'};"
        s += f"cooldown={unit['init_cooldown'] or ''};" if unit['init_cooldown'] != -1 else ''
        s += f"a={unit['a'].name if isinstance(unit['a'],Passive) else Passive.get(unit['a']).name if unit['a'] else '-'};"
        s += f"b={unit['b'].name if isinstance(unit['b'],Passive) else Passive.get(unit['b']).name if unit['b'] else '-'};"
        s += f"c={unit['c'].name if isinstance(unit['c'],Passive) else Passive.get(unit['c']).name if unit['c'] else '-'};"
        s += f"seal={unit['seal'].name if isinstance(unit['seal'],Passive) else Passive.get(unit['seal']).name if unit['seal'] else '-'};"
        if unit['attuned']:
            s += f"attuned={Passive.get(unit['attuned']).name};"
        s += f"accessory={Accessories.get(unit['accessory']).name};" if unit['accessory'] else ''
        props = 'is_ally,' if unit['playable'] else '' + \
                'use_ally_stats,' if unit['unit'][:4] == 'PID_' and unit['unit'][-2:] == '味方' and Enemies.get('E'+unit['unit'][1:-2]) else '' + \
                'use_enemy_stats,' if unit['unit'][:4] == 'PID_' and Heroes.get('P'+unit['unit'][1:]+'味方') else ''
        s += f"properties={props[:-1]};" if props != '' else ''

        if not unit['playable']:
            s += 'ai={'
            s += f"turn={unit['start_turn']};" if 'start_turn' in unit and unit['start_turn'] != -1 else ''
            s += f"group={unit['start_group']};" if 'start_group' in unit and unit['start_group'] != -1 else ''
            s += f"delay={unit['start_delay']};" if 'start_delay' in unit and unit['start_delay'] != -1 else ''
            s += 'break_walls=1;' if unit.get('break_wall') else ''
            s += 'tether=1;' if unit.get('return_base') else ''
            s = (s[:-1] if s[-1] == ';' else s) + '};'
        if unit['nb_spawn'] > 0:
            s += 'spawn={'
            s += f"turn={unit['spawn_turns']+1};" if 'spawn_turns' in unit and unit['spawn_turns'] != -1 else ''
            s += f"count={unit['nb_spawn']};" if unit['nb_spawn'] > 1 else ''
            s += f"target={Units.get(unit['spawn_target']).name};" if unit.get('spawn_target') else ''
            s += f"remain={unit['spawn_target_remain']};" if 'spawn_target_remain' in unit and unit['spawn_target_remain'] != -1 else ''
            s += f"kills={unit['spawn_target_kills']};" if 'spawn_target_kills' in unit and unit['spawn_target_kills'] != -1 else ''
            s = (s[:-1] if s[-1] == ';' else s) + '};'
        return (s[:-1] if s[-2:] != '};' else s) + '};'

    def Units(self):
        s = '[\n'
        for i,unit in enumerate(self.data['units']):
            s += self.Unit(unit, i) + '\n'
        s += ']'
        return s

    def hasReinforcements(self):
        return any(u['nb_spawn'] > 0 for u in self.data['units'])
