#! /usr/bin/env python3

from ...Tool.Reader import IReader, readAvail

class ConsumableReader(IReader):
    _basePath = 'Common/SkyCastle/ConsumeItemData/'

    def parse(self):
        KIND = {0: 'basic', 1: 'evolved', 2: 'limited'}

        nb = self.overviewLong(0x08, 0x995D773A)
        self.readArray()
        for _ in range(nb):
            self.prepareObject()
            self.readString('id_tag')
            self.readString('use_convertion')
            self.readString('sprite')
            readAvail(self, 'avail')
            self.insert('kind', KIND[self.getInt(0x5F139C3F)])
            self.skip(0x04) # Padding
            self.end()
        self.end()


class StructureReader(IReader):
    _basePath = 'Common/SkyCastle/FacilityData/'

    def parse(self):
        KIND = {0: 'Structure (D)', 1: 'Traps', 2: 'Resources', 3: 'Ornaments', 4: 'Structure (O)', 5: 'R&R Structures', 6: 'Structure (Resort)', 7: 'Decoy Traps'}

        nb = self.overviewLong(0x08, 0x69670863)
        self.readArray()
        for _ in range(nb):
            self.prepareObject() # 0xA0
            self.readString('id_tag')
            self.readString('sprite')
            self.readString('sprite_broken')
            self.skip(0x08) # Always null
            self.readString('next_id')
            self.readString('prev_id')
            self.skip(0x08) # Always null
            self.skip(0x08) # For Fortress, prev_prev_id
            self.readString('group') # School group
            self.readString('required_id')
            self.readString('base_id')
            self.skip(0x20)
            self.readInt('level', 0x2F49485D)
            self.readInt('required', 0x9A43DD98)
            self.skip(0x0C)
            self.readInt('a0', 0x470C8300)
            self.readInt('range', 0xEBBB944C)
            self.readBool('is_offensive', 0x61)
            self.insert('kind', KIND[self.getByte(0x5D)])
            self.skip(0x0A)
            self.end()
        self.end()
