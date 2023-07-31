#! /usr/bin/env python3

from typing import Any
from typing_extensions import Self
from ..Tool.Reader import IReader

__all__ = 'Container'

class _ContainerMeta(type):
    def __repr__(cls) -> str:
        return f"<class {cls.__name__} ({len(cls._DATA)} files, {len([o for os in cls._DATA.values() for o in os])} objects)>"

class Container(metaclass=_ContainerMeta):
    """Base class for any Container-like class.
    
    A Container class will use a Reader class and cache all its
    results for a quicker use without the need of local copy.

    Provides two methods to retrieve a class:
    - `get`: Return the object with the given key
    - `fromAssets`: Return all objects listed on the given asset
    Provide also the `load` method to load all the object on a given asset
    without returning them. Useful to restrict useless load of `get`.

    Any child need to overload `_reader` with the Reader class in use,
    and optionnaly `_key` if `id_tag` is not used for ordering.
    """

    _key = 'id_tag'
    _reader: IReader = None

    def __init_subclass__(cls):
        cls._DATA = {}

    def __init__(self):
        self.data = None

    def __repr__(self) -> str:
        if self._key is None:
            for n,f in self._DATA.items():
                for o in (f.values() if isinstance(f, dict) else f):
                    if self.data == o:
                        return '<' + type(self).__name__ + ' (' + n + ')>'
            k = ''
        else:
            k = self._getAt(self.data, [self._key] if isinstance(self._key, (int,str)) else self._key) or ''
        return '<' + type(self).__name__ + ' (' + str(k) + ')>'

    @classmethod
    def get(cls, key: str, at:list=None) -> Self | None:
        if key is None: return None
        if at is None: at = cls._key
        if isinstance(at, (int,str)):
            at = [at]
        elif not isinstance(at, (list,tuple)) or len(at) == 0:
            raise TypeError("`at` must be a non-empty list of key/index")

        for f in cls._DATA.values():
            for o in (f.values() if isinstance(f, dict) else f):
                if cls._getAt(o, at) == key:
                    ret = cls()
                    ret.data = o
                    return ret

        from ..PersonalData import BINLZ_ASSETS_DIR_PATH
        from os import listdir
        for f in listdir(BINLZ_ASSETS_DIR_PATH + cls._reader._basePath)[::-1]:
            if f[-7:] != '.bin.lz' or not cls.load(f[:-7]): continue
            for o in (cls._DATA[f[:-7]].values() if isinstance(cls._DATA[f[:-7]], dict) else cls._DATA[f[:-7]]):
                if cls._getAt(o, at) == key:
                    ret = cls()
                    ret.data = o
                    return ret

    @classmethod
    def getAll(cls, key: str, at:list=None) -> list[Self]:
        if key is None: return []
        if at is None: at = cls._key
        if isinstance(at, (int,str)):
            at = [at]
        elif not isinstance(at, (list,tuple)) or len(at) == 0:
            raise TypeError("`at` must be a non-empty list of key/index")

        rets = []
        for f in cls._DATA.values():
            for o in (f.values() if isinstance(f, dict) else f):
                if cls._getAt(o, at) == key:
                    ret = cls()
                    ret.data = o
                    rets.append(ret)

        from ..PersonalData import BINLZ_ASSETS_DIR_PATH
        from os import listdir
        for f in listdir(BINLZ_ASSETS_DIR_PATH + cls._reader._basePath)[::-1]:
            if f[-7:] != '.bin.lz' or not cls.load(f[:-7]): continue
            for o in (cls._DATA[f[:-7]].values() if isinstance(cls._DATA[f[:-7]], dict) else cls._DATA[f[:-7]]):
                if cls._getAt(o, at) == key:
                    ret = cls()
                    ret.data = o
                    rets.append(ret)

        return rets


    @classmethod
    def fromAssets(cls, file: str) -> list[Self]:
        datas = cls._DATA.get(file)
        if datas is None:
            cls.load(file)
            datas = cls._DATA.get(file)
        os = []
        for data in (datas.values() if isinstance(datas, dict) else datas or []):
            o = cls()
            o.data = data
            os.append(o)
        return os

    @classmethod
    def load(cls, name: str) -> bool:
        # if isinstance(cls._key, (int,str)): cls._key = [cls._key]
        if name in cls._DATA: return False

        # print('Container parsed', cls._reader._basePath+name)
        reader = cls._reader.fromAssets(name)
        if not reader.isValid() or reader.object is None: return False

        objs = reader.object if isinstance(reader.object, list) else [reader.object]
        if cls._key is None:
            cls._DATA[name] = objs
        elif len(objs) > 0 and cls._key not in objs[0]:
            raise KeyError("Container class use an incorrect sort key")
        else:
            cls._DATA[name] = {o[cls._key]: o for o in objs}
        # else:
        #     try:
        #         keys = objs
        #         for k in cls._key:
        #             keys = [o[k] for o in keys]
        #         cls._DATA[name] = {o[cls._key]: o for o in objs}
        return True
    
    @staticmethod
    def _getAt(object: list|dict, keys: list[str|int]) -> Any | None:
        for k in keys:
            if isinstance(object, dict): object = object.get(k)
            elif isinstance(object, list) and isinstance(k, int) and len(object) > k: object = object[k]
            else: object = None
            if object is None: return
        return object