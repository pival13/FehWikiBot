#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from ...Utility.Reader.Reward import readReward

class MjolnirsStrikeReader(IReader):
    _basePath = 'Common/Mjolnir/BattleData/'

    def parse(self):
        SEASONS = ['LightDark','DarkLight','HeavenLogic','LogicHeaven']
        nb = self.overviewLong(0x08, 0x00)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('bonus_structure')
            self.readString('bonus_structure_next')
            self.readString('boss_id')
            self.readString('map_id')
            count = self.overviewInt(0xB0, 0xd5a73af1)
            self.readArray('rewards')
            for _ in range(count):
                self.prepareObject()
                self.readInt('kind', 0xb78d759e)
                self.readInt('tier_hi', 0x55d7f567)
                self.readInt('tier_lo', 0xf77f40bc)
                self.skip(0x04) # Payload
                readReward(self, 'reward', 0x487e08, -4)
                self.prepareArray('reward_ids')
                for _ in range(2):
                    self.readString()
                self.end()
                self.end()
            self.end()
            count = self.overviewInt(0xAC, 0xa00d812a)
            self.readArray('tiers')
            for _ in range(count):
                self.prepareObject()
                self.readShort('score_multiplier', 0xddd9)
                self.readShort('tier', 0x3472)
                self.readByte('percent_down', 0x66, signed=True)
                self.readByte('percent_up', 0xe7, signed=True)
                self.readByte('percent_2up', 0x39, signed=True)
                self.readByte('percent_3up', 0x4e, signed=True)
                self.end()
            self.end()
            count = self.overviewInt(0xA8, 0xf6c8b3aa)
            self.readArray('_unknow1')
            for _ in range(count):
                self.prepareObject()
                self.readShort('_unknow1', 0x23bd)
                self.readShort('_unknow3', 0x457d)
                self.skip(0x04) # 0x00
                self.end()
            self.end()
            count = self.overviewInt(0xA4, 0xfc7d0e75)
            self.readArray('_unknow2')
            for _ in range(count):
                self.prepareObject()
                self.insert('_unknow1', hex(self.getShort(0x2cdd)))
                self.readByte('_unknow2', 0x76)
                self.readByte('_unknow3', 0xbe)
                self.readByte('_unknow4', 0xa3)
                self.readByte('_unknow5', 0xb7)
                self.skip(0x02) # 0x00
                self.end()
            self.end()
            readAvail(self, 'avail')
            readAvail(self, 'shield_avail')
            readAvail(self, 'counter_avail')
            self.skip(0x10)
            self.readMask('origins', 4, 0xc8f81eca)
            self.skip(0x04)
            self.skip(0x10) # reward,tiers,_unknows count
            self.skip(0x0D)
            self.insert('season', SEASONS[self.getByte(0x1c)])
            self.skip(0x0A)
            self.end()
        self.end()

MSReader = MjolnirsStrikeReader
MjolnirBattleDataReader = MjolnirsStrikeReader

class MechanismReader(IReader):
    _basePath = 'Common/Mjolnir/FacilityData/'

    def parse(self):
        nb = self.overviewInt(0x08, 0xC6AC9C0F)
        self.readArray()
        for _ in range(nb):
            self.prepareObject() # 0x80
            self.readString('id_tag')
            self.readString('sprite')
            self.readString('broken_sprite')
            self.readString('_unknow1')
            self.readString('next')
            self.readString('prev')
            self.skip(0x24)
#             '_unknow2': util.getString(data, offGr+0x30),
#             '_group_id': util.getString(data, offGr+0x38),
#             '_struct_id': util.getInt(data, offGr+0x40, 0x11aa991a),
#             '_struct_id2': util.getInt(data, offGr+0x44, 0x3251464d),
#             'terrain_id': util.getInt(data, offGr+0x48, 0xe24a11af),
#             '_unknow5': util.getInt(data, offGr+0x4C, 0x4a13cf66),
#             '_unknow5-': util.getInt(data, offGr+0x50, 0x7856dae3),
            self.readInt('level', 0xc54d1c6e)
            self.skip(0x26)
#             'cost': util.getInt(data, offGr+0x58, 0x85da15bc),
#             '_unknow7': hex(util.getInt(data, offGr+0x5c, 0x35e586df)),
#             '_unknow8': hex(util.getInt(data, offGr+0x60, 0x8de0beb1)),
#             'a0': util.getInt(data, offGr+0x64, 0x69c452d9),
#             '_unknow9': hex(util.getInt(data, offGr+0x68, 0x743af47c)),
#             'range': util.getInt(data, offGr+0x6c, 0x84ca17f),# > 10 ? xy-range : range
#             '_isGateway': util.getByte(data, offGr+0x70, 0x57),
#             'effect_type': util.getByte(data, offGr+0x71, 0x70),
#             'range_type': util.getSByte(data, offGr+0x72, 0x4e),
#             '_unknow10': util.getByte(data, offGr+0x73, 0x85),
#             'turns': util.getByte(data, offGr+0x74, 0x2d),
#             'showPanelNewUpgradAvailable': util.getBool(data, offGr+0x75, 0x62),
#             '_unknow11': util.getByte(data, offGr+0x76, 0x2a),
#             '_unknow11-': util.getByte(data, offGr+0x77, 0x7c),
#             '_isGateway2': util.getByte(data, offGr+0x78, 0x38),
#             'isBase': util.getByte(data, offGr+0x79, 0xa6),
#             'isSummoner': util.getBool(data, offGr+0x7a, 0x1c),
#             'isSummoner2': util.getByte(data, offGr+0x7b, 0x1c),
#             'isSummoner3': util.getByte(data, offGr+0x7c, 0x1c),
#             'isSummoner4': util.getByte(data, offGr+0x7d, 0x1c),
            self.assertPadding(0x02)
            self.end()
        self.end()

MSStructureReader = MechanismReader
MjolnirFacilityDataReader = MechanismReader
