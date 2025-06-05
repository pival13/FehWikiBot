#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail, readReward
from ...Stages.Reader.Stage import StageReader
from ...Tool.globals import DIFFICULTIES

class UnitedWarfrontReader(IReader):
    _basePath = 'Common/CoopTrial/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x20156DC9)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            nDiff = self.overviewInt(0x4C, 0xCE2DB314)
            self.readArray('stages')
            for _ in range(5):
                self.prepareObject()
                self.readString('map_id')
                self.readString('unit_id')
                self.readObject('maps')
                arrPtr = self.getLong()
                for i in range(nDiff):
                    o = StageReader(self._buff, arrPtr + i*0x78).object
                    self.insert(o['diff'], o)
                self.end()
                self.end()
            self.end()
            self.readArray('_obj2')
            for _ in range(nDiff):
                self.prepareObject()
                self.insert('diff', DIFFICULTIES[self.getInt(0xECE3DEF9)])
                self.readBool('altered_data', 0xB0)
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
            for _ in range(5*nDiff):
                self.prepareObject()
                readReward(self, 'reward', 0x7DEE74A6)
                self.assertPadding(0x04)
                self.prepareArray('reward_ids')
                for _ in range(3): self.readString()
                self.end()
                self.end()
            self.end()
            readAvail(self, 'avail')
            self.assertBytes(0x04, 0xD087BA10, '&_nStages[0:4]')
            self.skip(0x01) # nDiff
            self.assertBytes(0x07, 0xB2A75BDACE2DB3, '&nDiffs[1:8]')
            self.assertBytes(0x04, 0x90B10F7A, '&nDiffs[8,12]')
            self.assertBytes(0x04, 0x8F5BCD74, '&nDiffs[12:16]')
            self.assertBytes(0x04, 0x45CBD9F0, '&nDiffs[16:20]')
            self.end()
        self.end()

UWReader = UnitedWarfrontReader
CoopTrialReader = UnitedWarfrontReader
