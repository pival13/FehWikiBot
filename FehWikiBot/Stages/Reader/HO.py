#! /usr/bin/env python3

from ...Tool.Reader import IReader
from ...Tool.globals import DIFFICULTIES

class HeroicOrdealsReader(IReader):
    _basePath = 'Common/HeroTrial/'

    @classmethod
    def fromUnique(cls):
        return cls.fromAssets('00_first')

    def parse(self):
        nb = int.from_bytes(self._header[0x0C:0x10], 'little')
        if 0 not in self._strTbl: self.skip(0x08)
        self.prepareArray()
        for _ in range(nb):
            self.prepareObject()
            self.readStringHeader('id_tag')
            self.insert('diff', DIFFICULTIES[self.getInt(0x7CBD6A60)])
            self.readInt('dragonflowers', 0x292C2039)
            self.end()
        self.end()

HOReader = HeroicOrdealsReader
HeroTrialReader = HeroicOrdealsReader