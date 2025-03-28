#! /usr/bin/env python3

from ...Tool.Reader import IReader, readReward, readAvail

class CompileCombatManualReader(IReader):
    _basePath = 'Common/StockShop/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x4C642BB6)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('currency')
            readAvail(self, 'avail')
            count = self.overviewInt(0x08, 0x2D089F09)
            self.readArray('targets')
            ptrs = []
            for _ in range(count):
                self.prepareObject()
                ptrs.append(self._i)
                readReward(self, 'reward', 0x2B8A8BD4, 16)
                prevOff = self.getLong()
                self.insert('prev_idx', ptrs.index(prevOff) if prevOff in ptrs else None)
                self.skip(0x04) # payload
                self.readInt('cost', 0x1549E147)
                self.end()
            self.end()
            self.skip(0x04) # count
            self.readBool('limited',0xC0)
            self.readByte('part',0x7F)
            self.assertPadding(2)
            self.end()
        self.end()

StockShopReader = CompileCombatManualReader
