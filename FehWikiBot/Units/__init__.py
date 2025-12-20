#! /usr/bin/env python3

__all__ = ['Units', 'Heroes', 'Enemies']

from .Heroes import Heroes
from .Enemies import Enemies
from .NPC import NPC

class _UnitMeta(type):
    def __repr__(cls):
        return f"<class {cls.__name__} ({len(Enemies._DATA)+len(Heroes._DATA)} files, {len([o for os in Heroes._DATA.values() for o in os])+len([o for os in Enemies._DATA.values() for o in os])} objects)>"

class Units(metaclass=_UnitMeta):
    @staticmethod
    def get(key: str):
        if not isinstance(key, str) or len(key) == 0:
            return None
        elif key[1:] == 'ID_アバター':
            o = NPC()
            o.data = {
                'id_tag': key,
                'name': 'Kiran: Hero Summoner'
            }
            return o
        elif key[0] == 'E':
            return Enemies.get(key)
        else:
            return Heroes.get(key)

    @staticmethod
    def fromAssets(file: str):
        return Heroes.fromAssets(file) + Enemies.fromAssets(file)

    @staticmethod
    def fromName(name: str):
        return Heroes.fromName(name) or Enemies.fromName(name)

    @staticmethod
    def fromFace(name: str):
        return Heroes.fromFace(name) or Enemies.fromFace(name) or NPC.fromFace(name)

    @staticmethod
    def load(name: str) -> bool:
        ret1 = Heroes.load(name)
        ret2 = Enemies.load(name)
        return ret1 or ret2
