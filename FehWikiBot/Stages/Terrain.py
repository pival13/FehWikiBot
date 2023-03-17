#! /usr/bin/env python3

from ..Tool.Container import Container
from .Reader.Terrain import MapReader, EnvironmentReader, CellEnvironmentReader

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

class Map(Container):
    _reader = MapReader
    _key = None

    @classmethod
    def load(cls, name: str) -> bool:
        if not super().load(name):
            return False
        Environment.load(name)

        datas = cls._DATA.get(name)
        for data in (datas.values() if isinstance(datas, dict) else datas or []):
            if data['terrain'] is not None:
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
        if len(ret) > 0:
            return ret[0]
        ret = super().getAll(key, ('terrain','map_id'))
        return ret[0] if len(ret) > 0 else None

    @classmethod
    def getAll(cls, mapId):
        maps = cls.fromAssets(mapId)
        for l in ['A','B','C','D','E','F','G','H']:
            maps += cls.fromAssets(mapId+l)
        return maps
    
    @property
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

    @property
    def wallStyle(self):
        if ((self.data['terrain'] or {'@Environment':{}})['@Environment'] or {}).get('walls') is None: return ''
        if self.data['terrain']['@Environment']['walls']['file'] == 'Wallpattern.png': return 'normal'
        if self.data['terrain']['@Environment']['walls']['file'] == 'Boxpattern.png': return 'Box'
        if self.data['terrain']['@Environment']['walls']['file'] == 'IcePattern.png': return 'IceBox'
        return self.data['terrain']['@Environment']['walls']['file'][12:-4]

    @property
    def needBackground(self):
        from os.path import exists
        from ..PersonalData import WEBP_ASSETS_DIR_PATH
        from PIL import Image
        if self.data['terrain'] is None: return False
        
        filepath = WEBP_ASSETS_DIR_PATH + 'Common/Field/' + ('Chip/' if self.data['terrain']['type'] is not None else '') + self.data['terrain']['map_id'] + '.png'
        if not exists(filepath): return False
        with Image.open(filepath) as img:
            if ('a' in img.mode or 'A' in img.mode) and img.getextrema()[-1][0] < 0xF0:
                return True
        return False

    @property
    def background(self):
        if ((self.data['terrain'] or {'@Environment':{}})['@Environment'] or {}).get('underlay') is None: return ''
        if self.data['terrain']['@Environment']['underlay']['file'] == 'WavePattern.jpg': return 'Wave'
        if self.data['terrain']['@Environment']['underlay']['file'] == 'LavaPattern.jpg': return 'Lava'
        return self.data['terrain']['@Environment']['underlay']['file'][:-4]
