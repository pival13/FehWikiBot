#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail, readTime
from ...Utility.Reader.Reward import readReward

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
            readTime(self, 'start2', 0x843E97F6BDC9CCB3)

            if self.readObject('stages'):
                self.readArray('stages')
                for _ in range(30):
                    self.prepareObject()
                    # 3 x 0x08 bytes, as follow
                    self.insert('_flag', [self.overviewByte(0x08*i+0x00, 0xA9) for i in range(3)])
                    self.insert('level', [self.overviewByte(0x08*i+0x01, 0x2C) for i in range(3)])
                    self.insert('boss_level', [self.overviewByte(0x08*i+0x02, 0xAD) for i in range(3)])
                    # padding
                    self.insert('factor1', [self.overviewShort(0x08*i+0x04, 0xDCDC) for i in range(3)])
                    self.insert('factor2', [self.overviewShort(0x08*i+0x06, 0xAD36) for i in range(3)])
                    # print(self._stack[-1][0]['factor1'], self._stack[-1][0]['factor2'])
                    self.skip(0x18) # previously read
                    self.readArray('_unknow2') # ['0xf7e43524', '0xf4f33524', '0xf7e4351c', '0xf7e43524', '0xf7e4351c', '0xf7e4351c']
                    for _ in range(6):
                        self.insert(None, hex(self.getInt()))
                    self.end()
                    # 3 x 0x04 bytes, as follow
                    self.insert('min_rift_vessels', [self.overviewShort(0x04*i+0x00, 0x35EC) for i in range(3)])
                    self.insert('max_rift_vessels', [self.overviewShort(0x04*i+0x02, 0xF403) for i in range(3)])
                    self.skip(0x0C) # previously read
                    self.insert('_unknow3', [hex(self.getShort(0x40BA)) for _ in range(3)])
                    self.assertPadding(6)
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
                    self.assertPadding(7)
                    readReward(self, 'reward', 0xACF0DE36)
                    self.assertPadding(4)
                    self.prepareArray('reward_ids')
                    for _ in range(3):
                        self.readString()
                    self.end()
                    readReward(self, 'advanced_reward', 0X875BB721)
                    self.assertPadding(4)
                    self.prepareArray('reward_ids2')
                    for _ in range(3):
                        self.readString()
                    self.end()
                    self.end()
                self.end()
                self.readArray('_unknow1')
                for _ in range(7):
                    self.prepareArray()
                    for _ in range(3):
                        self.readShort(None, 0x8488) # [[50, 50, 0], [50, 50, 0], [40, 40, 20], [30, 40, 30], [30, 40, 30], [20, 40, 40], [20, 40, 40]]
                        # 0x8748 => [[1010, 1010, 960], [1010, 1010, 960], [1000, 1000, 980], [990, 1000, 990], [990, 1000, 990], [980, 1000, 1000], [980, 1000, 1000]]
                    self.end()
                    self.assertPadding(0x02)
                self.end()
                self.readArray("_skillCost")
                for _ in range(6):
                    self.readInt(None, 0xF7E435EC)
                self.end()
                self.assertBytes(0x18, 0x00000088FE0773510000000000007FB67ADDF78400D80C8C, '_stages')
            self.end()
            
            for _ in range(self.readList('daily_rewards', 0x35F7601A)):
                self.prepareObject()
                readReward(self, 'reward', 0x33287F60)
                self.assertPadding(0x04)
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
            self.assertBytes(8, 0x2E410F8A7D443EB7, '_12')
            self.assertBytes(8, 0x6625D9ED5DAA0403, '_34')
            self.assertBytes(12, 0xAFEB1B0B11BA38763CA19888, '_567')
            self.assertBytes(4, 0xF0219FF7, '_8')
            self.assertBytes(4, 0xAFCE324D, '_9')
            self.assertBytes(4, 0x6CDBCD5D, '_A')
            self.end()
        self.end()

SSReader = SeersSnareReader
ExplorerReader = SeersSnareReader
