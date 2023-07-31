#! /usr/bin/env python3

from ...Tool.Reader import IReader

class SoundReader(IReader):
    _basePath = 'Common/Sound/arc/'

    XOR = [
        0x5A, 0x60, 0x70, 0x80, 0xA1, 0x92, 0x0C, 0xF5,
        0x27, 0x82, 0x92, 0x58, 0x1A, 0x8A, 0x56, 0x7A,
        0x46, 0xC7, 0xF7, 0xCD, 0xDD, 0x2D, 0x0C, 0x3F,
        0xA1, 0x58, 0x8A, 0x2F, 0x3F, 0xF5, 0xB7, 0x27,
        0xFB, 0xD7, 0xEB, 0x6A
    ]

    TYPE = {0x00: 'Simple', 0x02: 'Compound', 0x04: 'Random', 0x10: 'Alias', 0x18: 'Alias',92:''}
    KIND = ['BGM', 'Sound', 'Voice']

    def parse(self):
        nb = self.overviewLong(0x08, 0x00)
        self.readArray()
        for _ in range(nb):
            self.readObject()
            # self.insert('off', hex(self._i+0x20))
            self.readStringHeader('id_tag')
            self.readString('name', self.XOR)
            count = self.getByte()
            type = self.TYPE[self.getByte(0x08)]
            self.insert('type', type)
            self.skip(0x02)
            self.insert('kind', self.KIND[self.getInt()])
            self.prepareArray('list')
            for _ in range(count):
                self.readObject()
                if type == 'Alias':
                    self._i = self.getLong()
                    self.readString('original', self.XOR)
                else:
                    # self.insert('off', hex(self._i+0x20))
                    self.readString('file', self.XOR)
                    self.readString('archive', self.XOR)
                    # More
                self.end()
            self.end()
            self.end()
        self.end()


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
            count = self.getByte()
            self.readBool('_unknow1')
            self.skip(0x05)
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
        # TODO Check whenever both are merge
        o1 = cls.fromAssets('00_first')
        o2 = cls.fromAssets('v0701b_engage')
        o1._obj = o1.object + o2.object
        return o1

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