#! /usr/bin/env python3

from typing_extensions import Self
from .Container import Container

class JsonContainer(Container):
    """Derivative class of `Container`, saving data into JSON files.
    
    An instance of `JsonContainer` will prefer to read data from JSON files instead
    of the assets. These files are automatically generated when they do not exist or
    are obsolete. Behaves similarly to a `Container` otherwise.

    Provides two methods to retrieve a class:
    - `get`: Return the object with the given key
    - `fromAssets`: Return all objects listed on the given asset
    Provide also the `load` method to load all the object on a given asset
    without returning them. Useful to restrict useless load of `get`.

    Any child need to overload `_reader` with the Reader class in use,
    and optionnaly `_key` if `id_tag` is not used for ordering.
    """

    @classmethod
    def load(cls, name: str) -> bool:
        from os.path import exists, getmtime
        import json
        from ..PersonalData import JSON_ASSETS_DIR_PATH as jsonPath, BINLZ_ASSETS_DIR_PATH as assetsPath

        if name in cls._DATA: return False

        assetsPath += cls._reader._basePath + name + '.bin.lz'
        jsonPath += cls._reader._basePath + name + '.json'

        if exists(assetsPath) and (not exists(jsonPath) or getmtime(assetsPath) >= getmtime(jsonPath)):
            # print('Json parsed', cls._reader._basePath+name)
            reader = cls._reader.fromAssets(name)
            if not reader.isValid(): return False
            obj = reader.object
            json.dump(obj, open(jsonPath, mode='w', encoding='utf-8'), ensure_ascii=False, indent=2)
        elif exists(jsonPath):
            # print('Json loaded', cls._reader._basePath+name)
            obj = json.load(open(jsonPath, mode='r', encoding='utf-8'))
        else:
            return False

        if cls._key is None:
            cls._DATA[name] = obj
        elif len(obj) > 0 and cls._key not in obj[0]:
            raise KeyError("Container class use an incorrect sort key")
        else:
            cls._DATA[name] = {o[cls._key]: o for o in obj}
        return True
