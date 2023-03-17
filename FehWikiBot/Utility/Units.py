#! /usr/bin/env python3

__all__ = ['Units', 'Heroes', 'Enemies']

from .Reader.Unit import HeroReader, EnemyReader
from ..Tool.Container import Container
from .Messages import Messages

class _UnitMeta(type):
    def __repr__(cls):
        return f"<class {cls.__name__} ({len(Enemies._DATA)+len(Heroes._DATA)} files, {len([o for os in Heroes._DATA.values() for o in os])+len([o for os in Enemies._DATA.values() for o in os])} objects)>"

class Units(metaclass=_UnitMeta):
    @staticmethod
    def get(key: str):
        if not isinstance(key, str) or len(key) == 0:
            return None
        elif key[0] == 'E':
            return Enemies.get(key)
        else:
            return Heroes.get(key)

    @staticmethod
    def fromAssets(file: str) -> list:
        return Heroes.fromAssets(file) + Enemies.fromAssets(file)
    
    @staticmethod
    def load(name: str) -> bool:
        ret1 = Heroes.load(name)
        ret2 = Enemies.load(name)
        return ret1 or ret2

class Enemies(Container):
    _reader = EnemyReader

    @property
    def name(self): return Messages.EN(self.data['id_tag']) + ': ' + Messages.EN(self.data['id_tag'].replace('ID_','ID_HONOR_'))

class Heroes(Container):
    _reader = HeroReader

    @property
    def name(self): return Messages.EN(self.data['id_tag']) + ': ' + Messages.EN(self.data['id_tag'].replace('ID_','ID_HONOR_'))