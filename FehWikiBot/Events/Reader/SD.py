#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail, readReward

class SummonerDuelsSeasonReader(IReader):
    _basePath = 'Common/SRPG/RealTimePvP/Stage/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x47A2B2C786EA31FA)
        self.readArray()
        for _ in range(nb):
            self.prepareObject() # 0x58
            self.readString('id_tag')
            readAvail(self, 'avail')
            self.readString('fixed_map_id')
            count = self.overviewByte(0x18, 0x67)
            self.readArray('random_map_ids')
            for _ in range(count):
                self.readString()
            self.end()
            count = self.overviewByte(0x11, 0x42)
            self.readArray('captain_skills')
            for _ in range(count):
                self.readInt(None, 0x7EC25F4B)
            self.end()
            count = self.overviewByte(0x0A, 0x5F)
            self.readArray('bonus_units')
            for _ in range(count):
                self.readString()
            self.end()
            self.skip(0x03) # counts x3
            self.skip(0x05) # padding
            self.end()
        self.end()

SDSeasonReader = SummonerDuelsSeasonReader

class SummonerDuelsReader(IReader):
    _basePath = 'Common/SRPG/RealTimePvP/Fave/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x5C24DEA5CC489268)
        self.readArray()
        for _ in range(nb):
            self.prepareObject() # 0x70
            self.readString('id_tag')
            readAvail(self, 'avail')
            self.skip(0x20)
            # '_ptr1': {
            #     #hex(util.getLong(data, offGr+0x30))
            #     #0x18
            #     # 74 3E 51 E3 47 8B BC DA  5F BD BF 50 13 A5 3E 27  B7 92 8B D3 39 12 B2 C3
            # },
            # '_ptr2': {
            #     '_arr1': [util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x38)+0x00), 0x1E0D)],
            #     '_arr2': [util.getSShort(data, util.getLong(data, util.getLong(data, offGr+0x38)+0x08)+0x02*i, 0x569C) for i in range(3)],
            #     '_arr3': [util.getShort(data, util.getLong(data, util.getLong(data, offGr+0x38)+0x10)+0x02*i, 0xE82A) for i in range(5)],
            #     # 0x2C
            #     # padding 0x04
            # },
            # '_arr1': [{
            #     '_str': util.getString(data, util.getLong(data, util.getLong(data, offGr+0x40))+0x18*i),
            #     'tiers': util.getLong(data, (util.getLong(data, util.getLong(data, offGr+0x40))+0x18*i+0x08)) == util.getLong(data, offGr+0x48) and "== Same as below ==" or "TODO: New object",
            #     # 0x07
            #     # 0B C9 79 FA BA AC B5
            #     # 84 C8 79 FA BB AC B5
            # } for i in range(util.getInt(data, util.getLong(data, offGr+0x40)+0x08, 0x7B3AABF4))],
            # 'tiers': [{
            #     'tier': util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x18*i+0x00, 0x63E6B689),
            #     'based_glory': util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x18*i+0x04, 0x6C6CE0C0),
            #     '_int3': util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x18*i+0x08, 0xF036CF62),
            #     'defeat_lost': util.getSInt(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x18*i+0x0C, 0x50F84663),
            #     '_int5': util.getSInt(data, util.getLong(data, util.getLong(data, offGr+0x48))+0x18*i+0x10, 0xBAFB37A5),
            #     # padding 0x04
            # } for i in range(util.getInt(data, util.getLong(data, offGr+0x48)+0x08, 0xAB20D4AE))],
            count = self.readList('tier_rewards', 0x1EEA0687)
            for _ in range(count):
                self.prepareObject()
                readReward(self, 'reward', 0xE8DD3CF9)
                self.readInt('tier', 0xD200E204)
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            count = self.readList('rank_rewards', 0x591810F7)
            for _ in range(count):
                self.prepareObject()
                readReward(self, 'reward', 0x785F977F)
                self.readInt('rank_hi', 0x0D70C748)
                self.readInt('rank_lo', 0xDBDDF690, signed=True)
                self.assertPadding(4)
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            self.skip(0x10)
            self.end()
        self.end()

SDReader = SummonerDuelsReader

class SummonerDuelsRankedReader(SummonerDuelsReader):
    _basePath = 'Common/SRPG/RealTimePvP/Rate/'
SDRReader = SummonerDuelsRankedReader

class SummonerDuelsSurvivalReader(SummonerDuelsReader):
    _basePath = 'Common/SRPG/RealTimePvP/AdvancedRate/'
SDSReader = SummonerDuelsSurvivalReader
