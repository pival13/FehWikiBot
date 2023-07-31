#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from ...Utility.Reader.Reward import readReward
# from ...Tool.globals import WEAPON_TYPE

class SeersSnareReader(IReader):
    _basePath = 'Common/SRPG/Explorer/'

    def parse(self):
        nb = self.overviewLong(0x08, 0xECECA9F1A69E0B27)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')

            self.prepareObject('final_boss')
            self.readString('unit')
            self.readString('weapon')
            self.readString('assist')
            self.readString('special')
            self.readString('a')
            self.readString('b')
            self.readString('c')
            self.readString('seal')
            self.readArray('enemies')
            for _ in range(5):
                self.readString()
            self.end()
            self.end()

            readAvail(self, 'avail')
            self.skip(0x08)

            if self.readObject('stages'):
                self.readArray('stages')
                for _ in range(30):
                    self.prepareObject()
                    # 3 x 0x08 bytes, as follow
                    self.insert('_flag', [self.overviewByte(0x08*i+0x00, 0xA9) for i in range(3)])
                    self.insert('level', [self.overviewByte(0x08*i+0x01, 0x2C) for i in range(3)])
                    self.insert('boss_level', [self.overviewByte(0x08*i+0x02, 0xAD) for i in range(3)])
                    # padding
                    self.insert('_unknow', [self.overviewShort(0x08*i+0x04, 0xDC86) for i in range(3)])
                    self.insert('hp_factor', [self.overviewShort(0x08*i+0x06, 0xAD36) for i in range(3)])
                    self.skip(0x18) # previously read
                    self.readArray('_unknow2')
                    for _ in range(6):
                        self.insert(None, hex(self.getInt()))
                    self.end()
                    # 3 x 0x04 bytes, as follow
                    self.insert('min_rift_vessels', [self.overviewShort(0x04*i+0x00, 0x34C0) for i in range(3)])
                    self.insert('max_rift_vessels', [self.overviewShort(0x04*i+0x02, 0xF787) for i in range(3)])
                    self.skip(0x0C) # previously read
                    self.insert('_unknow3', [hex(self.getShort(0x00)) for _ in range(3)])
                    self.skip(0x06) # padding
                    self.skip(0x08)
                    # self.readShort('_5', 13806)
                    # self.readShort('_6', 0xF403)
                    # self.readShort('_7', 13804)
                    # self.readShort('_8', 62760)
                    self.readByte('id', 0x51)
                    self.skip(0x08)
                    # self.insert('_9', hex(self.getInt()))
                    # self.readByte('_1', 0xE7, signed=True)
                    # self.readByte('_2', 0xE3, signed=True)
                    # self.readByte('_3', 0x7E, signed=True)
                    # self.readByte('_4', 0xC2)
                    self.skip(0x07) # padding
                    readReward(self, 'reward', 0XACF0DE36)
                    self.skip(0x04) # padding
                    self.prepareArray('reward_ids')
                    for _ in range(3):
                        self.readString()
                    self.end()
                    readReward(self, 'advanced_reward', 0X875BB721)
                    self.skip(0x04) # padding
                    self.prepareArray('reward_ids2')
                    for _ in range(3):
                        self.readString()
                    self.end()
                    self.end()
                self.end()
                self.skip(0x08)
                # self.readArray('_unknow1')
                # for _ in range(7):
                #     self.readArray()
                #     for _ in range(3):
                #         self.readShort(None, 0x84BA)
                #     self.end()
                #     self.skip(0x02)
                # self.end()
                self.skip(0x08)
                # self.readArray("_unknow2")
                # for _ in range(6):
                #     self.readInt(None, 0xF7E43524)
                # self.end()
                self.skip(0x03)
                self.skip(0x01) # padding
                self.skip(0x06)
                self.skip(0x06) # padding
                self.skip(0x05)
                self.skip(0x03) # padding
            self.end()
            
            for _ in range(self.readList('daily_rewards', 0x35F7601A)):
                self.prepareObject()
                readReward(self, 'reward', 0x33287F60)
                self.skip(0x04) # Padding
                self.prepareArray('reward_ids')
                for _ in range(3):
                    self.readString()
                self.end()
                self.end()
            self.end()
            self.readArray('boss_battle')
            for _ in range(6):
                self.prepareObject()
                self.readString('unit')
                self.readString('beginner')
                self.readString('intermediate')
                self.readString('advanced')
                self.skip(0x04)
                # self.insert('_',[self.getByte(0x0) for _ in range(4)])
                self.readByte('stage', 0x8E)
                self.skip(0x03)
                self.end()
            self.end()
            self.skip(0x28)
            self.end()
        self.end()

SSReader = SeersSnareReader
ExplorerReader = SeersSnareReader
