#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail, readReward, readStat

class DivineGamesReader(IReader):
    _basePath = 'Common/SRPG/GraceFestival/'

    def parse(self):
        nb = self.overviewLong(0x08, 0xD25455785BD22F09)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            readAvail(self, 'avail')
            self.assertBytes(4, 0x7353c3c0^0x26b600, '[30:34]') # Delta 574848 = 0x08C580
            # 0x410680
            # 0x4bcc00
            self.assertBytes(4, 0xA205269C, '[34:38]')
            # max_hero
            count = self.readList('skills', 0x64C45957)
            for i in range(count):
                self.prepareObject()
                self.readString('id_tag')
                self.readString('sprite_effect1')
                self.readString('sprite_effect2')
                self.readInt('id_num', 0x9904AD46)
                self.readInt('prev_id', 0x1B263366, signed=True)
                self.readInt('sort_id', 0x8150A4D6)
                self.readInt('icon_id', 0xFF0272E5)
                self.readInt('sort_id2?', 0x51F2AA9D)
                self.assertBytes(4, 0x2F3C2CA2, f"skills[{i}][0x2C]")
                self.readInt('tier', 0x8C3738A5)
                self.readInt('category', 0x4F7D817A)
                readStat(self, 'stat1')
                readStat(self, 'stat2')
                self.end()
            self.end()

            self.readObject('_obj2')
            self.assertBytes(0x8, 0xC8082272CEB592D3, '_obj2[00:08]')
            self.assertBytes(0x8, 0xC524DA86FE6E1C0A, '_obj2[08:10]')
            self.assertBytes(0x8, 0x8A0FB569D67B6B77, '_obj2[10:18]')
            self.prepareArray('_arr1')
            for _ in range(3):
                self.readInt(None, 0xB7F5B81E)
            self.end()
            self.assertPadding(4)
            self.end()

            count = self.readList('stages', 0x5A852D66^5)
            for i in range(count):
                self.prepareObject()
                self.readInt('stage_id', 0x9C054F7B)
                self.assertBytes(4, 0x76C16454, f'stages[{i}][4:8]')
                self.assertBytes(4, 0x7DB9C3AB, f'stages[{i}][8:C]')
                self.readInt('min_version', 0x89DEB653)
                self.readInt('max_version', 0xDEB62BF4)
                self.assertPadding(4)
                self.prepareArray('difficulties')
                for j in range(3):
                    self.prepareObject()
                    self.assertBytes(4, 0x7C33D664, f'stages[{i}].difficulties[{j}][00:04]')
                    self.readInt('level', 0x92E6545D)
                    self.readInt('hp_factor', 0xA5395FC5)
                    self.assertPadding(4)
                    self.end()
                self.end()
                self.end()
            self.end()
            count = self.readList('score_rewards', 0xF3D3D8A9)
            for i in range(count):
                self.prepareObject()
                readReward(self, 'reward', 0x2446DB04)
                self.readInt('score',  0x13D305F9)
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            count = self.readList('best_score_rewards', 0xF3D3D8A9)
            for i in range(count):
                self.prepareObject()
                readReward(self, 'reward', 0x2446DB04)
                self.readInt('score', 0x13D305F9)
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            count = self.readList('rank_rewards', 0xF3D3D8A9)
            for i in range(count):
                self.prepareObject()
                readReward(self, 'reward', 0x2446DB04)
                self.readInt('rank', 0x13D305F9, signed=True)
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            self.readInt('bonus_version', 0x63357ECB)
            self.assertBytes(1, 0x8F, '[-8]')
            self.assertBytes(7, 0x9D63E6F5A9D3C2, '[-07:]')
            self.assertPadding(4)
            self.end()
        self.end()

GraceFestivalReader = DivineGamesReader
