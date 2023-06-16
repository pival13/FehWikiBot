#! /usr/bin/env python3

__all__ = 'Sound', 'BGM'

from typing_extensions import Self
from ..Tool import Container, classproperty
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
    def HO(self) -> dict:
        if 'HO' not in self._DATA:
            self._DATA['HO'] = {int(o['origin']): o for o in HOBGMReader.fromUnique().object}
        return self._DATA['HO']

    def bgms(self, map_id) -> list[str]:
        if map_id[0] in range(10): return self.HO[map_id]
        o = self.get(map_id)
        if o is None: return []
        if o.data['unknow_id'] is not None: print(o.data)
        bgms = [o.data['bgm_id'], o.data['bgm2_id']] + [b['bgm'] for b in o.data['boss_bgms']]
        bgms = list({bgm for bgm in bgms if bgm})
        return [Sound.get(v).file for v in bgms]
