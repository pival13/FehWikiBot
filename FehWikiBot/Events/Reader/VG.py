#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail, InvalidReaderError
from ...Utility.Reader.Reward import readReward

class VotingGauntletReader(IReader):
    _basePath = 'Common/Tournament/'
    XOR = [
        0x9A, 0xEC, 0xEE, 0x29, 0x81, 0x9E, 0xC2, 0x42,
        0xA1, 0x8D, 0xF3, 0xBD, 0x7B, 0x77, 0xE3, 0xF6,
        0x8C, 0xEC, 0x3B, 0x4D, 0x4F, 0x88, 0x20, 0x3F,
        0x63, 0xE3, 0x00, 0x2C, 0x52, 0x1C, 0xDA, 0xD6,
        0x42, 0x57, 0x2D, 0x4D
    ]

    @classmethod
    def fromUnique(cls):
        return cls.fromAssets('04_spring01')

    def parse(self):
        self.skip(0x08)
        nb = self.getLong()
        self.prepareArray()
        for _ in range(nb):
            self.readObject()
            self.readString('id_tag', self.XOR)
            self.prepareArray('units')
            for _ in range(8):
                self.readString(xor=self.XOR)
            self.end()
            cReward = self.getInt()
            cMults = self.getInt()
            self.skip(0x10)
            readAvail(self, 'avail')
            self.prepareArray('avail_rounds')
            for _ in range(3):
                readAvail(self)
            self.end()
            self.skip(0x10)
            self.readArray('rewards')
            for _ in range(cReward):
                self.prepareObject()
                self.readInt('kind')
                self.readInt('round',signed=True)
                self.readInt('army',signed=True)
                self.readInt('rank_lo',signed=True)
                self.readInt('rank_hi',signed=True)
                self.skip(0x0C)
                readReward(self, 'reward', offSize=-8)
                self.end()
            self.end()
            self.readArray('multipliers')
            for _ in range(cMults):
                self.prepareObject()
                self.readInt('flags')
                self.readInt('multiplier')
                self.end()
            self.end()
            self.end()
        self.end()

VGReader = VotingGauntletReader
TournamentReader = VotingGauntletReader