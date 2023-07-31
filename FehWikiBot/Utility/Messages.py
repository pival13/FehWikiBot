#! /usr/bin/env python3

from .Reader.Message import MessageReader

# git fetch && git checkout <update_tag> -- files/assets/JPJA/* files/assets/EUDE/* files/assets/EUEN/* files/assets/EUES/* files/assets/EUFR/* files/assets/EUIT/* files/assets/TWZH/* files/assets/USES/* files/assets/USPT/*

class _MessageMeta(type):
    def __repr__(cls) -> str:
        return f"<class {cls.__name__} ({len(cls._loaded)} files, {len(cls._DATA['USEN'])} EN, {len(cls._DATA['JPJA'])} JP, {len(cls._DATA['EUDE'])} others)>"

class Messages(metaclass=_MessageMeta):
    _DATA = {'USEN':{},'JPJA':{},'EUDE':{},'EUEN':{},'EUES':{},'EUFR':{},'EUIT':{},'TWZH':{},'USES':{},'USPT':{}}
    _loaded = set()

    @classmethod
    def USEN(cls, key): return cls.get(key, 'USEN')
    EN = USEN

    @classmethod
    def JPJA(cls, key): return cls.get(key, 'JPJA')
    JA = JPJA
    JP = JPJA

    @classmethod
    def EUDE(cls, key): return cls.get(key, 'EUDE')
    DE = EUDE

    @classmethod
    def EUEN(cls, key): return cls.get(key, 'EUEN')

    @classmethod
    def EUES(cls, key): return cls.get(key, 'EUES')
    ES = EUES

    @classmethod
    def EUFR(cls, key): return cls.get(key, 'EUFR')
    FR = EUFR

    @classmethod
    def EUIT(cls, key): return cls.get(key, 'EUIT')
    IT = EUIT

    @classmethod
    def TWZH(cls, key): return cls.get(key, 'TWZH')
    CH = TWZH

    @classmethod
    def USES(cls, key): return cls.get(key, 'USES')

    @classmethod
    def USPT(cls, key): return cls.get(key, 'USPT')
    PT = USPT

    @classmethod
    def get(cls, key, lang) -> str:
        if key is None or key == '' or lang not in cls._DATA: return ''
        if key[0] != 'M': key = 'M'+key
        v = cls._DATA[lang].get(key)
        if v is None: v = cls._search(key, lang)
        return v or ''

    @classmethod
    def _search(cls, key, lang):
        from ..PersonalData import BINLZ_ASSETS_DIR_PATH
        from os import listdir
        for f in listdir(BINLZ_ASSETS_DIR_PATH + 'USEN/Message/Data/'):
            if cls._load(lang + '/Message/Data/' + f):
                v = cls._DATA[lang].get(key)
                if v: return v
            if cls._load(lang + '/Message/Menu/Menu_' + f[5:]):
                v = cls._DATA[lang].get(key)
                if v: return v

    @classmethod
    def load(cls, lang, kind, name):
        if kind in ('Data','Menu'): name = kind + '_' + name
        return cls._load(lang + '/Message/' + kind + '/' + name + '.bin.lz')

    @classmethod
    def _load(cls, path):
        from os.path import exists, getmtime
        from json import load, dump
        from ..PersonalData import JSON_ASSETS_DIR_PATH as jsonPath, BINLZ_ASSETS_DIR_PATH as assetsPath
        if path in cls._loaded: return False

        lang = path[:4]
        jsonPath += path.replace('.bin.lz','.json')
        assetsPath += path

        if exists(assetsPath) and (not exists(jsonPath) or getmtime(assetsPath) >= getmtime(jsonPath)):
            parser = MessageReader.fromAssets(path)
            if parser.isValid():
                dump(parser.object, open(jsonPath, mode='w', encoding='utf8'), ensure_ascii=False, indent=2)
                for o in parser.object:
                    cls._DATA[lang][o['key']] = o['value']
                cls._loaded.add(path)
                return True

        if not exists(jsonPath): return False
        for o in load(open(jsonPath, encoding="utf-8")):
            cls._DATA[lang][o['key']] = o['value']
        cls._loaded.add(path)
        return True

def EN(key): return Messages.EN(key)
def JP(key): return Messages.JP(key)