#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from ...Utility.Reader.Reward import readReward

class HeroesJourneyReader(IReader):
    _basePath = 'Common/Journey/Terms/'

    XOR = [
        0x2F, 0x08, 0x66, 0xED, 0x7C, 0x98, 0x34, 0x2A,
        0xE4, 0xAC, 0x41, 0xD1, 0xE5, 0x1F, 0xD2, 0x5E,
        0x28, 0x32, 0x76, 0xDE, 0x87, 0x0A, 0xA7, 0xF9,
        0x44, 0x28, 0x26, 0xC7, 0x25
    ]

    def parse(self):
        nb = self.getLong(0x00)
        self.readArray()
        for _ in range(nb):
            self.prepareObject() # 0x68
            self.readString('id_tag', self.XOR)
            count = self.overviewInt(0x50, 0x148AE2CB)
            self.readArray('stages')
            for _ in range(count):
                self.prepareObject()
                self.readInt('base_memento', 0x409A5DE6)
                self.readShort('stamina', 0x43B8)
                self.readShort('difficulty', 0x4AD8)
                self.readShort('rarity', 0x978E)
                self.readShort('level', 0x61CA, signed=True)
                self.readShort('nb_enemy', 0x3AE3)
                self.readShort('requirement', 0xA1D1)
                self.readInt('useHeroicOrdeals', 0x3552B9A6)
                self.assertBytes(4, 0x08C74FB4, f'stages[{len(self._stack[-2][0])-1}][0x14-0x18]')
                self.skip(0x08) # payload
                readReward(self, 'reward', 0xB6FBEEDD, -8)
                self.prepareArray('reward_ids')
                for _ in range(2):
                    self.readString(None, self.XOR)
                self.end()
                self.end()
            self.end()
            count = self.overviewInt(0x4C, 0xA9124C19)
            self.readArray('memento_mulptiplier')
            for _ in range(count):
                self.prepareObject()
                self.readInt('drop', 0x5ACB4499)
                self.readInt('mult', 0xB4CF8F08)
                self.end()
            self.end()
            count = self.overviewInt(0x48, 0x87071ACC)
            self.readArray('rewards')
            for _ in range(count):
                self.prepareObject()
                self.readInt('points', 0xB5898082)
                readReward(self, 'reward', 0x0F1649E1, 0)
                self.prepareArray('reward_ids')
                for _ in range(2):
                    self.readString(None, self.XOR)
                self.end()
                self.end()
            self.end()
            count = self.overviewInt(0x44, 0x338F7D50)
            self.readArray('memento_events')
            for _ in range(count):
                self.readString(None, self.XOR)
                self.skip(0x08)
                # self.prepareObject()
                # self.readString('id_tag', self.XOR)
                # self.assertBytes(4, 0xBE654E36, f'memento[{len(self._stack[-2][0])-1}][0x08-0C]')
                # self.assertPadding(4)
                # self.end()
            self.end()
            self.readObject('unknow1')
            self.assertBytes(0x20, 0x225843ec818cf25cdb713f15e9799086ae81013f8ae047f6973761a1377e8ac3)
            self.end()
            readAvail(self, 'avail')
            self.skip(0x10) # counts
            self.end()
        self.end()

HJReader = HeroesJourneyReader
JourneyReader = HeroesJourneyReader
