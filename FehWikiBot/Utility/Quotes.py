#! /usr/bin/env python3

from .Reader.Message import MessageReader

from .Units import Heroes

class _QuoteMeta(type):
    def __repr__(cls) -> str:
        return f"<class {cls.__name__} ({len(cls._DATA['USEN'])} EN, {len(cls._DATA['JPJA'])} JP)>"

class Quotes(metaclass=_QuoteMeta):
    _DATA = {'USEN':{}, 'JPJA':{}}

    @classmethod
    def get(cls, key, lang='USEN') -> str:
        if key is None or key == '' or lang not in cls._DATA: return ''
        unit = key[key.find('_')+1:key.rfind('_')]
        v = cls._DATA[lang].get(unit)
        if v is None:
            cls.load(lang, unit)
            v = cls._DATA[lang].get(unit)
            if v is None: return ''
        return v.get(key)

    @classmethod
    def load(cls, lang, unit: str|Heroes):
        if isinstance(unit, Heroes): unit = unit.data['character_file']
        parser = MessageReader.fromAssets(lang + '/Message/Character/' + unit + '.bin.lz')
        if not parser.isValid(): return False
        cls._DATA[lang][unit] = {o['key']: o['value'] for o in parser.object}
        return True
