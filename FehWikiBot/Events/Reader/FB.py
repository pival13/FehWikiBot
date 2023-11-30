#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from ...Utility.Reader.Reward import readReward

class ForgingBondsReader(IReader):
    _basePath = 'Common/Portrait/'

    XOR = [
        0x2F, 0x08, 0x66, 0xED, 0x7C, 0x98, 0x34, 0x2A,
        0xE4, 0xAC, 0x41, 0xD1, 0xE5, 0x1F, 0xD2, 0x5E,
        0x28, 0x32, 0x76, 0xDE, 0x87, 0x0A, 0xA7, 0xF9,
        0x44, 0x28, 0x26, 0xC7, 0x25, 0x21, 0x06, 0x68,
        0xE3, 0x72, 0x96, 0x3A, 0x24, 0xEA, 0xA2, 0x4F,
        0xDF, 0xEB, 0x11, 0xDC, 0x50, 0x26, 0x3C, 0x78,
        0xD0, 0x89, 0x04, 0xA9, 0xF7, 0x4A, 0x26, 0x28,
        0xC9, 0x2B
    ]

    def parse(self):
        nb = self.getLong()
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag', xor=self.XOR)
            self.readString('id_tag2', xor=self.XOR)
            self.readString('title_id', xor=self.XOR)
            self.readString('scenario_id', xor=self.XOR)
            self.skip(0x08) # self.readString('hearts_path', xor=self.XOR)
            unitcount = self.overviewInt(0x90, 0xBA6E2D66)
            self.readArray('units')
            for _ in range(unitcount):
                self.readString(xor=self.XOR)
            self.end()
            count = self.overviewInt(0x8C, 0xECA8A241)
            self.readArray('_unknow1')
            for _ in range(count):
                self.readLong(xor=0x88DBEFAC)
            self.end()
            count = self.overviewInt(0x88, 0xE8559E6C)
            self.readArray('stages')
            for _ in range(count):
                self.prepareObject()
                self.readInt('base_point', 0x615CDAF3)
                self.readInt('unknow1', 0x09B40F9D)
                self.readShort('difficulty', 0x5B22)
                self.readShort('rarity', 0x471D)
                self.readShort('delta_level', 0xA671, True)
                self.readShort('unknow2', 0xD84B)
                self.end()
            self.end()
            count = self.overviewInt(0x84, 0x6F889C0D)
            self.readArray('_unknow2')
            for _ in range(count):
                self.prepareObject()
                # TODO
                self.end()
            self.end()
            count = self.overviewInt(0x80, 0x52974491)
            self.readArray('color_bonus')
            for _ in range(count):
                self.readLong(xor=0x5B08CD8C)
            self.end()
            count = self.overviewInt(0x7C, 0x07C5C47C)
            self.readArray('score_mult')
            for _ in range(count):
                self.prepareObject()
                self.readInt('drop', 0x5F1684B1)
                self.readInt('mult', 0x9225CDF9)
                self.end()
            self.end()
            count = self.overviewInt(0x78, 0x66A383C2)
            self.readArray('_unknow3')
            for _ in range(count):
                self.readLong(xor=0xD07D040F)
            self.end()
            count = self.overviewInt(0x74, 0x54236634)
            self.readArray('accessories')
            for _ in range(count):
                self.readString(xor=self.XOR)
            self.end()
            count = self.overviewInt(0x70, 0x7AA1F6C2)
            self.readArray('hero_rewards')
            for _ in range(count*unitcount):
                self.prepareObject()
                self.insert('unit', self.getLong(0x0100) >> 3)
                self.readInt('score', 0x37CB7986)
                self.skip(0x04) # payload
                readReward(self, 'reward', 0x3B9EB0D7, -4)
                self.prepareArray('reward_ids')
                for _ in range(2):
                    self.readString(xor=self.XOR)
                self.end()
                self.end()
            self.end()
            count = self.overviewInt(0x6C, 0xDD5F9DF4)
            self.readArray('daily_rewards')
            for _ in range(count):
                self.prepareObject()
                self.skip(0x10)
                self.skip(0x04) # payload
                self.readInt('day', 0xA3F0477C)
                readReward(self, 'reward', 0x68236593, -8)
                self.prepareArray('reward_ids')
                for _ in range(2):
                    self.readString(xor=self.XOR)
                self.end()
                self.end()
            self.end()
            # self.readArray('_unknow1')
            self.skip(0x18)
            readAvail(self, 'avail')
            self.skip(0x28) # count x10
            self.skip(0x18)
            self.end()
        self.end()

FBReader = ForgingBondsReader
PortraitReader = ForgingBondsReader
