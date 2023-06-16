#! /usr/bin/env python3

from ...Tool.Reader import IReader, readStat

class MapReader(IReader):
    _basePath = 'Common/SRPGMap/'

    TERRAIN_TYPE = {-1: None, 0: 'Normal', 1: 'Inside', 2: 'Desert', 3: 'Sunset', 4: 'Snow'}
    CELL_TYPE = []

    def parse(self):
        self.prepareObject()
        self.skip(0x04)
        self.readInt('highest_score', 0xA9E250B1)
        if  self.readObject('terrain'):
            self.readString('map_id')
            w = self.getInt(0x6B7CD75F)
            h = self.getInt(0x2BAA12D5)
            self.insert('width', w)
            self.insert('height', h)
            self.insert('type', self.TERRAIN_TYPE[self.getByte(0x41,signed=True)])
            self.skip(0x07) # padding
            self.prepareArray('ground')
            for _ in range(h):
                self.prepareArray()
                for _ in range(w):
                    self.readByte(None, 0xA1)
                    # {0: 'Plain', 3: 'Forest', 4: 'Mountain', 5: 'Water', 8: 'Wall'}
                self.end()
            self.end() 
            self.end()
        count = self.overviewInt(0x10, 0x9D63C79A)
        self.readArray('starting_pos')
        for _ in range(count):
            self.insert(None, chr(self.getShort(0xB332)+97)+str(self.getShort(0x28B2)+1))
            self.skip(0x04) # TODO
        self.end()
        count = self.overviewInt(0x0C, 0xAC6710EE)
        self.readArray('units')
        for _ in range(count):
            self.prepareObject()
            self.readString('unit')
            self.readString('weapon')
            self.readString('assist')
            self.readString('special')
            self.readString('a')
            self.readString('b')
            self.readString('c')
            self.readString('seal')
            self.readString('accessory')
            self.insert('pos', chr(self.getShort(0xB332)+97)+str(self.getShort(0x28B2)+1))
            self.readByte('rarity', 0x61)
            self.readByte('lv', 0x2A)
            self.readByte('init_cooldown', 0x1E, signed=True)
            self.readByte('max_cooldown', 0x9B, signed=True)
            readStat(self, 'stats')
            self.readByte('start_turn', 0xCF, signed=True)
            self.readByte('start_group', 0xF4, signed=True)
            self.readByte('start_delay', 0x95, signed=True)
            self.readBool('break_wall', 0x71)
            self.readBool('return_base', 0xB8)
            self.readByte('true_lv', 0x85)
            self.readBool('playable', 0xD1)
            self.skip(0x01) # padding
            self.readString('spawn_target')
            self.readByte('nb_spawn', 0x0A, signed=True)
            self.readByte('spawn_turns', 0x0A, signed=True)
            self.readByte('spawn_target_remain', 0x2D, signed=True)
            self.readByte('spawn_target_kills', 0x5B, signed=True)
            self.skip(0x04) # padding
            self.end()
        self.end()
        self.skip(0x08) # pos + units count
        self.readByte('max_turns', 0xFD)
        self.readBool('end_at_ally_phase', 0xC6)
        self.readByte('min_turns', 0xEC)
        self.end()

SRPGMapReader = MapReader

class EnvironmentReader(IReader):
    _basePath = 'Common/SRPG/Field/'

    def parse(self):
        def readObject(key):
            self.readObject(key)
            if self.overviewLong(0x08) == 0x00:
                self.end()
                self._stack[-1][0][key] = None
            else:
                self.readString('id')
                self.readString('file', [0])
                self.end()

        nb = self.overviewLong(0x08, 0x1D90083CCADFBC58)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            readObject('walls')
            readObject('underlay')
            readObject('overlay')
            readObject('overlay2')
            self.readString('cell_env_id', [0])
            self.end()
        self.end()

FieldReader = EnvironmentReader

class CellEnvironmentReader(IReader):
    _basePath = 'Common/SRPG/BattleBg/'

    def parse(self):
        def readObject(key):
            self.readObject(key)
            self.readString('background', [0])
            self.readString('walking_sound', [0])
            self.end()

        nb = self.overviewLong(0x08, 0x3926EEACBF6214E0)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag', [0])
            
            i = self.getLong()
            i, self._i = self._i, i
            
            readObject('Normal')
            readObject('Inside')
            readObject('Desert')
            readObject('Forest')
            readObject('Sea')
            readObject('Lava')
            readObject('Bridge')
            readObject('NormalWall')
            readObject('ForestWall')
            readObject('InsideWall')
            readObject('Fortress')
            readObject('River')

            self._i = i

            self.end()
        self.end()

BattleBgReader = CellEnvironmentReader
