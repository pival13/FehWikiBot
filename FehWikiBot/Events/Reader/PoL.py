#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from ...Utility.Reader.Reward import readReward

class PawnsOfLokiReader(IReader):
    _basePath = 'Common/SRPG/BoardGame/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x8C04448B9C6192D6)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            readAvail(self, 'avail')
            count = self.overviewByte(0x48, 0xEF)
            self.readArray('round_avails')
            for _ in range(count):
                readAvail(self)
            self.end()
            self.readArray('rounds')
            for _ in range(3):
                if not self.readObject(): continue
                self.readString('id')
                self.assertBytes(8, 0xA384B52D, '_rounds_1')
                self.readMask('weapons', 4, 0x818A089F)
                self.readMask('weapon_groups', 2, 0xFBC0)
                self.assertBytes(2, 0x130C, '_rounds_2')
                self.end()
            self.end()
            self.skip(0x08) # 0x20
            count = self.readList('bonus_definition', 0xC87BBD8B)
            for _ in range(count):
                self.prepareObject()
                self.assertBytes(8, 0x00601C756E18F7E5, 'bonus_definition::movement')
                self.readMask('weapons', 4, 0x513D6037)
                self.assertPadding(4)
                self.end()
            self.end()
            count = self.readList('pve_definition', 0xE237DACF)
            for _ in range(count):
                self.prepareObject()
                self.readArray('units')
                for _ in range(2): self.readString()
                self.end()
                self.readMask('series', 2, 0x4F8B)
                self.assertBytes(6, 0x2AE846, 'pve_defintion::_')
                self.end()
            self.end()
            self.skip(0x08)
            # count = self.readList('_unknow2', 0x84054BEC) # 0x20
            count = self.readList('score_rewards', 0xDFF84DE4)
            for _ in range(count):
                self.prepareObject()
                readReward(self, 'reward', 0xCC34B2C1)
                self.readInt('score', 0x610A90E7)
                self.prepareArray('reward_ids')
                for _ in range(3): self.readString()
                self.end()
                self.end()
            self.end()
            count = self.readList('tier_rewards', 0xEF13BB46)
            for _ in range(count):
                self.prepareObject()
                readReward(self, 'reward', 0x04B8F8FE)
                self.readByte('tier', 0x39)
                self.assertPadding(3)
                self.prepareArray('reward_ids')
                for _ in range(3): self.readString()
                self.end()
                self.end()
            self.end()
            count = self.readList('tiers', 0x58902F22)
            for _ in range(count):
                self.prepareObject()
                self.prepareArray('move_condition')
                for _ in range(4):
                    self.prepareObject()
                    self.readShort('new_tier', 0xE324, signed=True)
                    self.readShort('percent_to', 0x6DA5, signed=True)
                    self.readShort('percent_from', 0x5C75, signed=True)
                    self.assertPadding(2)
                    self.end()
                self.end()
                self.readShort('tier', 0xC476)
                self.assertPadding(6)
                self.end()
            self.end()
            self.skip(0x01) # nbRound
            self.assertBytes(7, 0x000000000000F9)
            self.end()
        self.end()

POLReader = PawnsOfLokiReader
BoardGameReader = PawnsOfLokiReader
