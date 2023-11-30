#! /usr/bin/env python3

__all__ = 'Sound', 'BGM'

from typing_extensions import Self
from ..Tool import Container, JsonContainer, classproperty
from .Reader.Sound import SoundReader, MapBGMReader, HOBGMReader

class Sound(Container):
    _reader = SoundReader

    @property
    def file(self):
        o = self
        while o and o.data['type'] == 'Alias':
            o = self.get(o.data['list'][0]['original'])
        if not o: return ''
        if o.data['type'] != 'Simple': print('Invalid sound: '+o.data['name'])
        s = o.data['list'][0]['file']
        if   o.data['kind'] == 'BGM': s += '.ogg'
        elif o.data['kind'] == 'Sound': s += '.ckb'
        elif o.data['kind'] == 'Voice': s += '.wav'
        return s


class BGM(Container):
    _reader = MapBGMReader

    @classproperty
    def HO(cls) -> dict:
        if 'HO' not in cls._DATA:
            cls._DATA['HO'] = {int(o['origin']): o for o in HOBGMReader.fromUnique().object}
        return cls._DATA['HO']

    @classmethod
    def bgms(cls, map_id) -> list[str]:
        if map_id[0] in range(10): return cls.HO[map_id]
        o = cls.get(map_id)
        if o is None: return []
        if o.data['unknow_id'] is not None: print(o.data)
        bgms = [o.data['bgm_id'], o.data['bgm2_id']] + [b['bgm'] for b in o.data['boss_bgms']]
        return [Sound.get(bgms[i]).file for i in range(len(bgms)) if bgms[i] and bgms[i] not in bgms[:i]]
