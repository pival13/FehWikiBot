#! /usr/bin/env python3

from ...Tool.Reader import IReader
from ...Utility.Reader.Reward import readReward

class StageReader(IReader):    
    def __init__(self, buff, i):
        self._header = [0]*0x20
        self._buff = bytes(buff)
        self._i = i
        self._obj = None
        self._stack = []

    def parse(self):
        from ...Tool.globals import DIFFICULTIES, WEAPON_TYPE

        self.prepareObject()
        self.readString('id_tag')
        self.readString('base_id')
        count = self.overviewInt(0x08, 0x092DFD01)
        self.readArray('required')
        for _ in range(count):
            self.readString()
        self.end()
        self.skip(0x04) # required count
        self.skip(0x04) # padding
        self.readString('honor_id')
        self.readString('name_id')
        self.readString('_unknow1')
        readReward(self, 'reward', 0x64645EE2)
        self.readMask('origins', 4, 0x67080B02)
        self.readShort('stamina', 0xBB22)
        self.skip(0x02)
        self.insert('diff', DIFFICULTIES[self.getShort(0xC074)])
        self.skip(0x08)
        self.readShort('survive', 0x4FCB, signed=True)
        self.readShort('lights_blessing', 0x3031)
        self.readShort('max_turn', 0xA743)
        self.readShort('min_turn', 0x8091)
        self.readShort('rarity', 0xCBB6)
        self.readShort('diplay_level', 0x14BA)
        self.readShort('level', 0xD953)
        self.readShort('reinforcements', 0x6399)
        self.readShort('last_enemy_phase', 0x6C4A)
        self.readShort('max_refreshers', 0x295B, signed=True)
        self.skip(0x02) # self.readShort('rd_level', 0x7C4E, signed=True)
        self.skip(0x04) # padding
        self.prepareArray('enemies')
        for _ in range(8):
            if self.getByte() != 0x68: self.insert(None, WEAPON_TYPE[self.overviewByte(-1,0x97)])
        self.end()
        self.end()

class MultiStageReader(IReader):
    def __init__(self, buff, i):
        self._header = [0]*0x20
        self._buff = bytes(buff)
        self._i = i
        self._obj = None
        self._stack = []
    
    def parse(self):
        from ...Tool.globals import DIFFICULTIES, WEAPON_TYPE
        self.prepareObject()
        self.readString('id_tag')
        if self.readPointer():
            self.readString('group_id')
            count = self.overviewInt(0x08, 0x1421ABBE)
            self.readArray('maps')
            for _ in range(count):
                self.prepareObject()
                self.readString('map_id')
                self.readByte('rarity', 0xCD)
                self.readShort('level', 0xC244)
                self.readByte('promotion_tier', 0x01)
                self.readShort('hp_factor', 0x8926)
                self.assertPadding(2)
                self.end()
            self.end()
            self.skip(0x04) # count
            self.readInt('team_count', 0x597A851B)
        self.end()
        readReward(self, 'reward', 0xE4189863)
        self.readBool('keep_team', 0xA4)
        self.assertBytes(1, 0x81)
        self.readShort('stamina', 0x5BD0)
        self.insert('diff', DIFFICULTIES[self.getShort(0x6FE0)])
        self.assertBytes(8, 0x84FD7EBB892D38B9)
        self.readShort('rarity', 0x9228)
        self.readShort('display_level', 0xF884)
        self.readShort('level', 0x1073)
        self.prepareArray('enemies')
        for _ in range(8):
            if self.getByte(0x1A,True) != -1: self.insert(None, WEAPON_TYPE[self.overviewByte(-1,0x1A)])
        self.end()
        self.end()
