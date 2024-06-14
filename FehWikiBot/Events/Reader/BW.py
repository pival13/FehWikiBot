#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from ...Utility.Reader.Reward import readReward

class BindingWorldsReader(IReader):
    _basePath = 'Common/SRPG/ConnectBonds/'

    def parse(self):
        nb = self.overviewLong(0x08, 0xA2233D21B59538BB)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            readAvail(self, 'avail')
            self.readObject('init_heroes')
            self.prepareArray('heroes')
            for _ in range(4):
                self.readString()
            self.end()
            self.readByte('lv', 0x7D)
            self.end()
            self.readObject('_unknow1')
            # TODO
            self.end()
            count = self.readList('stages', 0x50C874CC)
            for _ in range(count):
                self.prepareObject()
                self.readString('id_tag')
                self.readInt('id_num', 0x476A7493)
                self.readInt('hp_factor', 0xEB36D398)
                self.readInt('min_hero_id', 0x74C67B3D) #0,200,300,400,500
                self.readInt('max_hero_id', 0x33F7264A)
                self.readByte('difficulty', 0x53)
                self.readByte('rarity', 0x3B)
                self.readByte('lv', 0x65)
                self.readBool('generic_foes', 0x1E)
                self.readBool('_unknow1', 0x30)
                self.readBool('allow_refines', 0xDB)
                self.readByte('_unknow2', 0x41) #CD 83
                self.readByte('max_level', 0x10)
                readReward(self, 'reward', 0xEB36D398)
                self.assertPadding(4)
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
                self.assertPadding(4)
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            self.end()
        self.end()

BWReader = BindingWorldsReader
ConnectBondsReader = BindingWorldsReader
