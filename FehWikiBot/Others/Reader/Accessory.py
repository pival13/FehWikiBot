#! /usr/bin/env python3

from ...Tool.Reader import IReader
from ...Utility.Reader.Reward import readReward
from ...Tool.globals import ITEM_KIND

class AccessoryReader(IReader):
    _basePath = 'Common/DressAccessory/Data/'

    TYPES = {1: 'hat', 0: 'mask', 2: 'hair', 3: 'tiara'}

    def parse(self):
        nb = self.overviewLong(0x08, 0x0de4c6f0ab07e0e13)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('sprite')
            self.readInt('num_id', 0xf765ad9c)
            self.readInt('sort_id', 0x0159b21d)
            self.insert('type', self.TYPES.get(self.getByte(0xf6)) or f"Unknow ({self.getByte(0xf6)})")
            self.readBool('summoner', 0xf6)
            self.skip(0x06) # 0x981B01B78027
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
            self.readInt('cost', 0x975C6D07)
            self.insert('kind', ITEM_KIND.get(self.getInt(0x37E08AFE)) or f'Unknow ({self.overviewInt(-0x04, 0x37E08AFE)})')
            self.end()
            self.end()
        self.end()

AccessoryShopData = AccessoryPurchaseData