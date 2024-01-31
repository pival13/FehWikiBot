#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail, readReward, getAllStrings, getAllRewards

class AffinityAutoBattlesReader(IReader):
    _basePath = 'Common/AutoCoop/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x747094F0BFBE7E38)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('map_id')
            self.readArray('rewards')
            for _ in range(10):
                self.prepareObject()
                readReward(self, 'reward', 0x4A0E84C3)
                self.readInt('score', 0x46965D28)
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            self.readArray('stages')
            for _ in range(3):
                self.prepareObject()
                self.readInt('diff',0x32C4A2FF)
                self.readInt('base_score',0xDC95390F)
                self.readInt('rarity',0x7B2B5CC2)
                self.readInt('level',0x26B85FAE)
                self.assertBytes(0x08, 0xA8F9D1B3E9293058, 'extra')
                self.end()
            self.end()
            self.assertBytes(0x10, 0xA7BE5310ABCA4C44F16F2B02ECA0000E, 'block1')
            for _ in range(2):
                self.assertBytes(0x10, 0x00000000CE381B856F4162ACC24EFDEB, 'block2')
            for _ in range(2):
                self.assertBytes(0x08, 0x66E55F3C841AA60A, 'block3')
            self.assertBytes(0x04, 0xAE23FD90, 'int1')
            self.assertPadding(0x04)
            # Mult: x3
            # stamina: 15
            # max: 10000
            # no 2 successive battle with same support
            # Any change on team/unit after are ignored
            self.readArray('daily_rewards')
            for _ in range(6):
                self.prepareObject()
                readReward(self, 'reward', 0x33287F60)
                self.assertPadding(0x04)
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            self.assertBytes(0x04, 0x35F7601C, 'int2')
            self.assertPadding(0x04)
            readAvail(self, 'avail')
            self.assertBytes(0x10, 0x20BE28C5E8A04E3E641861218D8C2487, 'block4')
            self.end()
        self.end()

AABReader = AffinityAutoBattlesReader
AutoCoopReader = AffinityAutoBattlesReader
