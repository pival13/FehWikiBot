#! /usr/bin/env python3

from ...Tool.Reader import IReader
from ...Utility.Reader.Reward import readReward
from ...Tool.globals import ITEM_KIND

class AccessoryReader(IReader):
    _basePath = 'Common/DressAccessory/Data/'

    TYPES = {1: 'hat', 0: 'mask', 2: 'hair', 3: 'tiara', 4: 'aide'}

    def parse(self):
        nb = self.overviewLong(0x08, 0xde4c6f0ab07e0e13)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('sprite')
            self.readInt('num_id', 0xf765ad9c)
            self.readInt('sort_id', 0x0159b21d)
            self.insert('type', self.TYPES.get(self.getByte(0xf6)) or f"Unknow ({self.overviewByte(-1,0xf6)})")
            self.skip(0x02)#
            # self.assertBytes(2, 0xA526, f"[{self._stack[-1][0]['id_tag']}]._1")
            self.readBool('summoner', 0xf6)
            self.assertBytes(4, 0x981B01B7, '_filler')
            self.end()
        self.end()
    
class AccessoryAideData(IReader):
    _basePath = 'Common/DressAccessory/TamerData/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x4D456A353BA30E65)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('unit_id')
            self.readString('accessory_id')
            self.end()
        self.end()

class AccessoryPurchaseData(IReader):
    _basePath = 'Common/DressAccessory/ShopData/'

    def parse(self):
        nb = self.overviewLong(0x08, 0x948EEF2C71838C95)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('purchase_id')
            readReward(self, 'granted', 0x58B8C4C2)
            self.readInt('num_id', 0x1C5214A0)
            self.prepareObject('required')
            self.readInt('count', 0x975C6D07)
            self.insert('kind', ITEM_KIND.get(self.getInt(0x37E08AFE)) or f'Unknow ({self.overviewInt(-0x04, 0x37E08AFE)})')
            self.end()
            self.end()
        self.end()

AccessoryShopData = AccessoryPurchaseData