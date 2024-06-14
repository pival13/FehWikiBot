#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail, readReward
from ...Stages.Reader.Stage import StageReader
from ...Tool.globals import WEAPON_TYPE

class UnitedWarfrontReader(IReader):
    _basePath = 'Common/CoopTrial/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x20156DC9)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readArray('stages')
            for _ in range(5):
                self.prepareObject()
                self.readString('map_id')
                self.readString('unit_id')
                self.readObject('maps')
                arrPtr = self.getLong()
                for i in range(3):
                    o = StageReader(self._buff, arrPtr + i*0x78).object
                    self.insert(o['diff'], o)
                self.end()
                self.end()
            self.end()
            self.readArray('_obj2')
            for _ in range(3):
                self.prepareObject()
                self.readInt('_1', 0xECE3DEF9)
                self.readByte('_2', 0xB0)
                self.assertPadding(0x03)
                self.end()
            self.end()
            self.readArray('clear_rewards')
            for _ in range(1):
                self.prepareObject()
                readReward(self, 'reward', 0xDF0FEECD)
                self.assertPadding(0x04)
                self.prepareArray('reward_ids')
                for _ in range(3): self.readString()
                self.end()
                self.end()
            self.end()
            self.readArray('stage_rewards')
            for _ in range(15):
                self.prepareObject()
                readReward(self, 'reward', 0x7DEE74A6)
                self.assertPadding(0x04)
                self.prepareArray('reward_ids')
                for _ in range(3): self.readString()
                self.end()
                self.end()
            self.end()
            readAvail(self, 'avail')
            self.assertBytes(0x08, 0xCE2DB317D087BA10)
            self.assertBytes(0x08, 0x90B10F7AB2A75BDA)
            self.assertBytes(0x08, 0x45CBD9F08F5BCD74)
            self.end()
        self.end()
