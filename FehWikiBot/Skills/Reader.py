#! /usr/bin/env python3

from ..Tool.Reader import IReader

class SkillReader(IReader):
    _basePath = 'Common/SRPG/Skill/'

    SKILL_TYPE = ['Weapon', 'Assist', 'Special', 'A', 'B', 'C', 'Seal', 'Refine', 'Duo']
    REFINE_TYPE = {0: None, 1: 'Skill1', 2: 'Skill2', 101: 'Atk', 102: 'Spd', 103: 'Def', 104: 'Res'}

    def readWeaponList(self, key, xor):
        from ..Tool.globals import WEAPON_CATEGORY, WEAPON_MASK
        n =  self.getInt(xor)
        if n == WEAPON_MASK['All'] ^ WEAPON_MASK['Colorless Staff']:
            s = ',exclude=Staff'
        elif n == WEAPON_MASK['Ranged'] ^ WEAPON_MASK['Colorless Staff']:
            s = ',Ranged|exclude=Staff'
        elif n == WEAPON_MASK['Magical'] ^ WEAPON_MASK['Colorless Staff']:
            s = ',Magical|exclude=Staff'
        else:
            s = ''
            for mask, name in WEAPON_CATEGORY.items():
                if mask != 0 and (mask & n) == mask:
                    n ^= mask
                    s += ','+name
        self.insert(key, s[1:] if s != '' else None)

    def readMoveList(self, key, xor):
        from ..Tool.globals import MOVE_TYPE
        s = ','.join([MOVE_TYPE[v] for v in self.getMask(4, xor)])
        self.insert(key, s if s != '' else None)

    def parse(self):
        from ..Tool.Reader import readStat
        nb = self.overviewLong(0x08, 0x7fecc7074adee9ad)
        self.readArray()
        for _ in range(nb):
            self.prepareObject() # 0x160
            self.readString('id_tag')
            self.readString('pre_refine')
            self.readString('name_id')
            self.readString('desc_id')
            self.readString('refine_id')
            self.readString('beast_id')
            self.prepareArray('prev_id')
            for _ in range(2):
                self.readString()
            self.end()
            self.readString('next_id')
            self.readString('sprite_wepL',xor=[0])
            self.readString('sprite_wepR',xor=[0])
            self.readString('sprite_effect1',xor=[0])
            self.readString('sprite_effect2',xor=[0])
            readStat(self, 'stats')
            readStat(self, 'class_param')
            readStat(self, 'combat_buff')
            readStat(self, 'skill_param')
            readStat(self, 'skill_param2')
            readStat(self, 'refine_stats')
            self.readInt('id_num', 0xc6a53a23)
            self.readInt('sort_id', 0x8DDBF8AC)
            self.readInt('icon_id', 0xC6DF2173)
            self.readWeaponList('wep_equip', 0x35B99828)
            self.readMoveList('mov_equip', 0xAB2818EB)
            self.readInt('sp_cost', 0xC031F669)
            self.insert('type', self.SKILL_TYPE[self.getByte(0xBC)])
            self.readByte('tome_class', 0xF1)
            self.readBool('exclusive', 0xCC)
            self.readBool('enemy_only', 0x4F)
            self.readByte('range', 0x56)
            self.readByte('might', 0xD2)
            self.readByte('cooldown_count', 0x56, signed=True)
            self.readBool('assist_cd', 0xF2)
            self.readBool('healing', 0x95)
            self.readByte('skill_range', 0x09)
            self.readShort('score', 0xA232)
            self.readByte('promotion_tier', 0xE0)
            self.readByte('promotion_rarity', 0x75)
            self.readBool('refined', 0x02)
            self.insert('refine_type', self.REFINE_TYPE[self.getByte(0xFC)])
            self.readWeaponList('wep_effective', 0x23BE3D43)
            self.readMoveList('mov_effective', 0x823FDAEB)
            self.readWeaponList('wep_shield', 0xAABAB743)
            self.readMoveList('mov_shield', 0x0EBEF25B)
            self.readWeaponList('wep_weakness', 0x005A02AF)
            self.readMoveList('mov_weakness', 0xB269B819)
            self.skip(0x10)
            self.readInt('timing_id', 0x9C776648)
            self.readInt('ability_id', 0x72B07325)
            self.prepareArray('limits')
            for _ in range(2):
                self.prepareObject()
                self.readInt('id', 0x0EBDB832)
                self.readShort('param1', 0xA590, signed=True)
                self.readShort('param2', 0xA590, signed=True)
                self.end()
            self.end()
            self.readInt('target_wep', 0x409FC9D7)
            self.readInt('target_mov', 0x6C64D122)
            self.readString('next_passive')
            self.skip(0x08)
            # readTime(self, 'timestamp', 0xED3F39F93BFE9F51)
            self.readByte('random_allowed', 0x10)
            self.readByte('min_lv', 0x90)
            self.readByte('max_lv', 0x24)
            self.readBool('tt_inherit_base', 0x19)
            self.readByte('random_mode', 0xBE)
            self.skip(0x03)
            self.readInt('limit3_id', 0x0EBDB832)
            self.readShort('limit3_params1', 0xA590, signed=True)
            self.readShort('limit3_params2', 0xA590, signed=True)
            self.readByte('range_shape', 0x5C)
            self.readBool('target_either', 0xA7)
            self.readBool('distant_counter', 0xDB)
            self.readByte('canto_range', 0x41)
            self.readByte('pathfinder_range', 0xBE)
            self.readBool('arcane_weapon', 0xAA)
            self.skip(0x02)
            self.end()
        self.end()
        return

class RefineryReader(IReader):
    _basePath = 'Common/SRPG/WeaponRefine/'

    def parse(self):
        from ..Tool.globals import ITEM_KIND
        KIND = {0: '', 1: ITEM_KIND[19], 2: ITEM_KIND[17], 3: ITEM_KIND[18]}
        nb = self.overviewLong(0x08, 0x45162C00432CFD73)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('base_id')
            self.readString('refine_id')
            self.prepareArray('required')
            for _ in range(2):
                self.prepareObject()
                self.insert('kind', KIND[self.getShort(0x439C)])
                self.readShort('count', 0x7444)
                self.end()
            self.end()
            self.prepareObject('granted')
            self.insert('kind', KIND[self.getShort(0x439C)])
            self.readShort('count', 0x7444)    
            self.end()
            self.skip(0x04) # padding
            self.end()
        self.end()
        return

WeaponRefineReader = RefineryReader

class SealReader(IReader):
    _basePath = 'Common/SRPG/SkillAccessory/'

    def parse(self):
        from ..Tool.globals import COLOR
        nb = self.overviewLong(0x08, 0x166B3E4746A9D6D6)
        self.readArray()
        for _ in range(nb):
            self.prepareObject() # 0x20
            self.readString('id_tag')
            self.readString('next_id')
            self.readString('prev_id')
            self.prepareObject('required')
            self.readShort('sacred_coin', 0xC540)
            self.insert('badge_type', COLOR[self.getShort(0xD50F)+1])
            self.readShort('badge', 0x8CEC)
            self.readShort('great_badge', 0xCCFF)
            self.end()
            self.end()
        self.end()
        return

SkillAccessoryReader = SealReader

class SealForgeReader(IReader):
    _basePath = 'Common/SRPG/SkillAccessoryCreatable/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x0605B9F01A117E27)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.end()
        self.end()

SkillAccessoryCreatableReader = SealForgeReader

class CaptainSkillReader(IReader):
    _basePath = 'Common/SRPG/RealTimePvP/CaptainSkill/'

    def parse(self):
        nb = self.overviewLong(0x08, 0xB77037ED6EBCEC56)
        self.readArray()
        for _ in range(nb):
            self.prepareObject() # 0x58
            self.readString('id_tag')
            self.skip(0x40)
            #'stats1': util.getStat(data, offGr+0x08),
            #'_int1': util.getSInt(data, offGr+0x18, 0x2A4BF41A),
            #0x08
            # Padding 0x04
            #'stats2': util.getStat(data, offGr+0x28),
            #'_int2': util.getSInt(data, offGr+0x38, 0x2A4BF41A),
            #0x08
            # Padding 0x04
            self.readInt('id_num', 0x54DC7C40)
            self.readInt('_unknow', 0xC3D1B4BF)
            self.readInt('icon_id', 0x7B344922)
            self.skip(0x04)
            self.end()
        self.end()