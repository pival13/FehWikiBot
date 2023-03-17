#! /usr/bin/env python3

from ...Tool.Reader import IReader

class MapBGMReader(IReader):
    _basePath = 'Common/SRPG/StageBgm/'

    XOR = [
        0x6F, 0xC0, 0x37, 0xBC, 0xC7, 0x6F, 0x04, 0x3B,
        0x6E, 0x7B, 0x76, 0xB8, 0xC7, 0x2E, 0x0E, 0x01,
        0xE6, 0x64, 0x84, 0x2B, 0xDC, 0x57, 0x2C, 0x84,
        0xEF, 0xD0, 0x85, 0x90, 0x9D, 0x53, 0x2C, 0xC5,
        0xE5, 0xEA, 0x0D, 0x8F
    ]

    def parse(self):
        nb = self.overviewLong(0x08)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readStringHeader('id_tag')
            self.readString('bgm_id', self.XOR)
            self.readString('bgm2_id', self.XOR)
            self.readString('unknow_id', self.XOR)
            self.readBool('genericBossMusic')
            count = self.getInt()
            self.skip(0x03)
            self.prepareArray('boss_bgms')
            for _ in range(count):
                self.prepareObject()
                self.readString('boss', self.XOR)
                self.readString('bgm', self.XOR)
                self.end()
            self.end()
            self.end()
        self.end()

StageBgmReader = MapBGMReader


class HOBGMReader(MapBGMReader):
    _basePath = MapBGMReader._basePath + 'HeroTrial/'

    @classmethod
    def fromUnique(cls):
        return cls.fromAssets('00_first')

    def parse(self):
        nb = self.overviewInt(0x08)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readStringHeader('origin')
            self.readString('bgm_map', self.XOR)
            self.readString('bgm_battle', self.XOR)
            self.end()
        self.end()

StageBgmHeroTrialReader = HOBGMReader