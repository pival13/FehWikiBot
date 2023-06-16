#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail
from .Stage import StageReader

class SpecialMapReader(IReader):
    _basePath = 'Common/SRPG/StageEvent/'

    def parse(self):
        nb = self.overviewLong(0x08, 0xC84AFFA7BB739117)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('banner_id')
            self.skip(0x08) # str ('V1'/None)
            self.readString('rd_bonus')
            self.skip(0x08) # str (None)
            readAvail(self, 'avail')
            self.readInt('sort_id', 0xA2BDF0B7)
            self.readInt('num_id', 0xFE6EF6B7)
            count = self.overviewInt(0x08, 0xFDBFB266)
            self.readArray('maps')
            for _ in range(count):
                self.insert(None, StageReader(self._buff, self._i).object)
                self.skip(0x078)
            self.end()
            self.skip(0x04) # count
            self.skip(0x01) # 0x36
            self.readBool('rival_domain', 0x34)
            self.skip(0x02) # padding
            self.end()
        self.end()

HeroBattleReader = SpecialMapReader
RivalDomainsReader = SpecialMapReader
StageEventReader = SpecialMapReader