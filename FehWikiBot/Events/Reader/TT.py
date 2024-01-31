#! /usr/bin/env python3

from ...Tool.Reader import IReader, readTime, readAvail
from ...Utility.Reader.Reward import readReward

class TempestTrialsReader(IReader):
    _basePath = 'Common/SRPG/SequentialMap/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x37cfee6c5195437)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('banner_file')
            self.readString('id_tag2')
            self.readString('scenario_file')
            readAvail(self, 'avail')

            self.readObject('unit_bonus1')
            cUnit = self.overviewInt(0x08, 0xf3470912)
            self.readArray('units')
            for _ in range(cUnit):
                self.readString()
            self.end()
            self.skip(0x04)
            self.readInt('bonus', 0x88f82c4b)
            self.end()

            self.readObject('unit_bonus2')
            cUnit = self.overviewInt(0x08, 0xf3470912)
            self.readArray('units')
            for _ in range(cUnit):
                self.readString()
            self.end()
            self.skip(0x04)
            self.readInt('bonus', 0x88f82c4b)
            self.end()

            for _ in range(self.readList('survival_bonus', 0xA8F24510)):
                self.prepareObject()
                self.readString('rank')
                self.readInt('team_lost', 0x88F494D0, True)
                self.readInt('mult', 0x608B1F2C)
                self.end()
            self.end()
            for _ in range(self.readList('speed_bonus', 0xA8F24510)):
                self.prepareObject()
                self.readString('rank')
                self.readInt('extra_turns', 0x88F494D0, True)
                self.readInt('mult', 0x608B1F2C)
                self.end()
            self.end()
            self.skip(0x08)
            for _ in range(self.readList('score_rewards', 0x629988e0)):
                self.prepareObject()
                readReward(self, 'reward', 0x5a029dec)
                self.skip(0x04)
                self.readString('reward_id')
                self.readInt('score', 0xf342cbbd)
                self.skip(0x04)
                self.end()
            self.end()
            for _ in range(self.readList('rank_rewards', 0xd5f99032)):
                self.prepareObject()
                readReward(self, 'reward', 0x4db73c78)
                self.skip(0x04)
                self.readString('reward_id')
                self.readInt('rank_hi', 0xc1805a3c)
                self.readInt('rank_lo', 0xd5f99032)
                self.end()
            self.end()
            for _ in range(self.readList('target_bonus', 0xEAF41B8B)):
                self.prepareObject()
                self.readInt('target', 0x4e2d3d06)
                self.readInt('bonus', 0xb48ec15a)
                self.end()
            self.end()
            self.skip(0x08)
            for _ in range(self.readList('additional_story_start', 0xF6F3DF55)):
                readTime(self, xor=0xbb8d539209925b89)
            self.end()
            cSets = self.overviewInt(0x08, 0xc33b272f)
            self.readArray('sets')
            for _ in range(cSets):
                self.readObject()
                self.readString('set_id')
                count = self.overviewInt(0x10, 0x1d2b72cb)
                self.readArray('battles')
                for _ in range(count):
                    self.prepareObject()
                    count = self.overviewInt(0x08, 0x2031150d)
                    self.readArray('maps')
                    for _ in range(count):
                        self.readString()
                    self.end()
                    self.skip(0x04) # map count
                    self.skip(0x04)
                    self.readByte('foe_count', 0x4f)
                    self.skip(0x01)
                    self.readByte('rarity', 0x56)
                    self.readByte('level', 0x28)
                    self.readShort('hp_factor', 0x4555)
                    self.skip(0x02)
                    self.readBool('use_random_assist', 0x51)
                    self.readBool('use_random_passive', 0x9e)
                    self.skip(0x06)
                    self.end()
                self.end()
                count = self.overviewInt(0x0C, 0x5ee8f0c4)
                self.readArray('enemies')
                for _ in range(count):
                    self.readString()
                self.end()
                self.skip(0x08) # battle + enemy count
                self.readInt('difficulty', 0xc28919b6)
                self.readInt('stamina', 0x7ad1f34)
                self.readInt('base_score', 0x65fb2a5e)
                self.readInt('team_count', 0xd4eaabad)
                self.readInt('turn_limit', 0x0DC968F3)
                self.end()
            self.end()
            self.skip(0x04) # Sets count
            self.skip(0x04)
            self.end()
        self.end()

TTReader = TempestTrialsReader
SequentialMapReader = TempestTrialsReader