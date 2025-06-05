#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail, readReward

class YourTimeToShineReader(IReader):
    _basePath = 'Common/SRPG/YouAreHero/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x757654160E6E6F41)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('final_battle')
            readAvail(self, 'avail')
            self.assertBytes(8, 0x723C2229FE9504D3, 'data[0x38:0x40]')

            self.readObject('status_effect?')
            self.assertBytes(8, 0x907EA0A72B8AAAAB, 'status_effect?[0x00:0x08]')
            self.readArray('ignored?')
            for i in range(15):
                self.prepareObject()
                self.readByte('id_num', 0xD7)
                self.assertBytes(3,0xF72503)
                self.end()
            self.end()
            self.assertBytes(8, 0xE622780A7A1AE73A, 'status_effect?[0x10:0x18]')
            self.assertBytes(8, 0xCB17D182B8E582E4, 'status_effect?[0x18:0x20]')
            self.assertBytes(8, 0x00000000D26CEC29, 'status_effect?[0x20:0x28]')
            self.end()
            
            count = self.readList('stages', 0x29227C2D)
            for i in range(count):
                self.prepareObject()
                self.readInt('id_num',0x7D0128CC)
                self.readInt('hp_factor', 0x8B98E361)
                self.readInt('min_hero_version', 0xD41A7422)
                self.readInt('max_hero_version', 0x23ACDAAA)
                self.readBool('boss?', 0x3A)
                self.readByte('difficulty', 0x57)
                self.readByte('rarity', 0xAA)
                self.readByte('level', 0xC2)
                self.readBool('generic_foes', 0x14)
                # Always: special_heroes, random_empty_skills
                # evolve_tier_4
                # skills suggested: 3,4
                self.skip(1) # self.assertBytes(1, 0x30, f'stages[{i}][0x15]')
                self.readBool('allow_refine', 0x1E)
                self.skip(1) # self.assertBytes(1, 0x05, f'stages[{i}][0x17]')
                self.readByte('possible_effects', 0x4A)
                self.assertBytes(1, 0x2F, f'stages[{i}][0x19]')

                self.assertPadding(6)
                readReward(self, 'reward', 0x0571928F)
                self.assertPadding(4)
                self.prepareArray('reward_ids')
                for _ in range(3): self.readString()
                self.end()
                self.end()
            self.end()

            count = self.readList('daily_rewards', 0x35F7601A)
            for _ in range(count):
                self.prepareObject()
                readReward(self, 'reward',0x33287F60)
                self.assertPadding(4)
                self.prepareArray('reward_ids')
                for _ in range(3): self.readString()
                self.end()
                self.end()
            self.end()
            
            self.assertBytes(8, 0x7E0E8A4F6D9CF37C, 'data[0x58:0x60]')
            self.assertBytes(8, 0x9DA572CBD2340BE0, 'data[0x60:0x68]')
            self.assertBytes(4, 0x53777B51, 'data[0x68:0x6C]')
            self.assertPadding(4)
            self.end()
        self.end()

YTSReader = YourTimeToShineReader