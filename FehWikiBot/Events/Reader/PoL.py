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
                self.assertBytes(4, 0xA384B52D, f'rounds[{len(self._stack[-2][0])-1}][0:4]')
                self.assertPadding(4)
                self.readMask('weapons', 4, 0x818A089F)
                self.readMask('weapon_groups', 2, 0xFBC0)
                self.assertBytes(2, 0x130C, f'rounds[{len(self._stack[-2][0])-1}][14:16]')
                self.end()
            self.end()
            self.skip(0x08)
            # if self.readObject('_1'):
            #     self.readArray('_1')
            #     for _ in range(7):
            #         self.prepareObject()
            #         self.readByte('id',0xCA)
            #         self.readShort('_1', 0xB1AE)
            #         self.assertPadding(5)
            #         self.end()
            #     self.end()
            #     self.readArray('_2') # range(3)
            #     self.readArray('_3') # range(3)
            #     self.readArray('_4') # range(3)
            #     self.readArray('_5') # range(3)
            #     self.assertBytes(0x18, 0x00EC2F1E309C3B58_8B3C18E12FB75BC9_3357B43E186B34A6)
            #     self.assertPadding(1)
            #     pass
            # self.end()
            count = self.readList('bonus_definition', 0xC87BBD8B)
            for _ in range(count):
                self.prepareObject()
                self.assertBytes(8, 0x00601C756E18F7E5, f'bonus_definition[{len(self._stack[-2][0])-1}][0:8]')
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
                self.assertBytes(2, 0xE846, f'pve_defintion[{len(self._stack[-2][0])-1}][10:12]')
                self.readBool('_bool', 0x2A)
                self.assertPadding(3)
                self.end()
            self.end()
            count = self.readList('_unknow2', 0x84054BEC)
            for _ in range(0):
                self.prepareObject()
                self.readShort('_1', 0x0167)
                self.prepareArray('_2')
                for _ in range(3):
                    self.prepareObject()
                    self.assertBytes(4, 0xF0483650)
                    self.readByte('_1', 0x50)
                    self.readByte('_2', 0xB7)
                    self.readShort('_3', 0x0167)
                    self.end()
                self.end()
                self.assertPadding(0x06)
                self.end()
            self.end()
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
