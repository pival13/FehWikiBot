#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from ...Utility.Reader.Reward import readReward

class HallOfFormsReader(IReader):
    _basePath = 'Common/SRPG/IdolTower/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x037CFEE6C5195437)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            readAvail(self, 'avail')
            readAvail(self, 'forma_avail')
            if  self.readObject('formas'):
                self.prepareArray('units')
                for _ in range(4):
                    self.readString()
                self.end()
                self.readByte('rarity', 0x9E)
                self.readByte('lv', 0x2A)
                self.end()
            count = self.readList('chambers', 0x6AC1C456)
            for i in range(count):
                self.prepareObject()
                self.readString('id_tag')
                self.assertBytes(0x08, 0x4E8E152E24BAEA69, f'&chambers[{i}][0x08]')
                self.readInt('num_id', 0xAC3AB736)
                self.readByte('difficulty', 0xCB)
                self.readByte('rarity', 0x69)
                self.readShort('lv', 0x6E)
                self.readShort('hp_factor', 0x1618)
                self.assertBytes(0x06, 0x36D1A8ED4B80, f'&chambers[{i}][0x1A]')
                self.readBool('generic', 0xd3)
                self.readBool('fixed_classes', 0x3B)
                self.readBool('refines', 0x7F)
                self.readByte('passive', 0x42)
                self.readInt('passive_min_sp', 0x4B722738)
                self.readInt('min_skill_id', 0x00138A93, signed=True)
                self.assertPadding(4)
                readReward(self, 'reward', 0xAE4D663F)
                self.skip(0x04)
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            count = self.readList('daily_rewards', 0x35F7601A)
            for _ in range(count):
                self.prepareObject()
                readReward(self, 'reward', 0x33287F60)
                self.skip(0x04)
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            self.readInt('max_skill', 0x8c641adc)
            self.readByte('_unknow1', 0x56)
            self.readBool('revival', 0x04)
            self.assertPadding(0x02)
            self.end()
        self.end()

HoFReader = HallOfFormsReader
IdolTowerReader = HallOfFormsReader