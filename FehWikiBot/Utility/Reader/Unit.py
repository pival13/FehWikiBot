#! /usr/bin/env python3

from ...Tool.Reader import IReader, readStat, readTime

class HeroReader(IReader):
    _basePath = 'Common/SRPG/Person/'

    def parse(self):
        from ...Tool.globals import BLESSING
        KIND = ['','LegendMythic','Duo','Harmonized','Ascended','Rearmed','Attuned']
        nb = self.overviewLong(0x08, 0xde51ab793c3ab9e1)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('character_file')
            self.readString('face_dir')
            self.readString('unit_dir')
            if  self.readObject('extra'):
                self.readString('duo_skill')
                readStat(self, 'bonus_effect')
                kind = KIND[self.getByte(0x21)]
                elem = BLESSING[self.getByte(0x05)]
                self.insert('kind', kind if kind != 'LegendMythic' else 'Mythic' if elem in BLESSING[-4:] else 'Legend')
                self.insert('element', elem)
                self.readByte('bst', 0x0F)
                self.readBool('pair_up', 0x80)
                self.readBool('extra_slot', 0x24)
                self.end()
            count = self.readList('dragonflower_costs', 0xA0013774, True)
            for _ in range(count):
                self.readInt(xor=0x715C6A7B)
            self.end()
            readTime(self, 'timestamp', 0xBDC1E742E9B6489B)
            self.readInt('num_id', 0x5F6E4E18)
            self.readInt('version_num', 0x2E193A3C)
            self.readInt('sort_id', 0x2A80349B)
            self.readMask('series', 4, 0xe664b808)
            self.readByte('weapon', 0x06)
            self.readByte('magic', 0x35)
            self.readByte('move', 0x2A)
            self.readByte('origin', 0x43)
            self.readByte('random_pool', 0xA1) # 0: None, 1: Regular, 2: Special
            self.readBool('permanent_hero', 0xC7)
            self.readByte('bvid', 0x3D)
            self.readBool('refresher', 0xFF)
            self.skip(0x08)
            readStat(self, 'base_stats')
            readStat(self, 'growth_rates')

            def getSkills(key):
                self.prepareArray(key)
                for i in range(5): self.insert(None, self.overviewString(0x08 * 15*i))
                self.end()
                self.skip(0x08)
            self.prepareObject('skills')
            getSkills('summon_weapon')
            getSkills('summon_assist')
            getSkills('summon_special')
            getSkills('summon_a')
            getSkills('summon_b')
            getSkills('summon_c')
            getSkills('summon_attuned')
            getSkills('weapon')
            getSkills('assist')
            getSkills('special')
            getSkills('a')
            getSkills('b')
            getSkills('c')
            getSkills('extra1')
            getSkills('extra2')
            self.end()
            self.skip(0x08 * 15*4) # Skip skills previously read (1 iteration is already skipped)
            self.end()
        self.end()

PersonReader = HeroReader
UnitReader = HeroReader

class EnemyReader(IReader):
    _basePath = 'Common/SRPG/Enemy/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x62ca95119cc5345c)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('character_file')
            self.readString('face_dir')
            self.readString('unit_dir')
            self.prepareObject('skills')
            self.readString('weapon')
            self.readString('assist1')
            self.readString('assist2')
            self.readString('special')
            self.end()
            readTime(self, 'timestamp', 0xBDC1E742E9B6489B)
            self.readInt('num_id', 0x422f41d4)
            self.skip(0x04)
            # self.readInt('is_kiran', 0x6D154FF7)
            self.readByte('weapon', 0xe4)
            self.readByte('magic', 0x81)
            self.readByte('move', 0x0d)
            self.skip(0x01)
            # self.readBool('random_allowed', 0xc4)
            self.readBool('generic', 0x6B)
            self.readBool('refresher', 0x2A)
            self.readBool('enemy', 0x13)
            self.skip(0x01) # padding
            readStat(self, 'base_stats')
            readStat(self, 'growth_rates')
            self.end()
        self.end()