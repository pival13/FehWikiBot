#! /usr/bin/env python3

from ...Tool.Reader import IReader, readTime

class FocusReader(IReader):
    _basePath = 'Common/Summon/'

    XOR = [
        0x24, 0x38, 0xF8, 0x00, 0x4C, 0xE0, 0x2E, 0x23,
        0x73, 0x83, 0xEF, 0xC4, 0x84, 0x8F, 0xF4, 0xE9,
        0xD2, 0xA5, 0x22, 0x3E, 0xFE, 0x06, 0x4A, 0xE6,
        0x28, 0x25, 0x75, 0x85, 0xE9, 0xC2, 0x82, 0x89,
        0xF2, 0xEF, 0xD4, 0xA3
    ]

    def parse(self):
        self.prepareObject()

        nb = self.overviewLong(0x08)
        self.readArray('summons')
        self._i = self._stack[-1][1] + 0x38
        for _ in range(nb):
            self.readObject()
            self.insert('id_tag', self._strTbl[self._i])
            self.readString('banner_path', self.XOR)
            self.skip(0x08) # self.readString('units_path', self.XOR) # Unreachable path
            self.readString('ticket_path', self.XOR)
            self.skip(0x08) # self.readString('ticketL_path', self.XOR)
            if False:
                count = self.overviewShort(0x94, 0x7E7E)
                self.readArray('red_classes')
                for _ in range(count):
                    self.readString(xor=self.XOR)
                self.end()
                count = self.overviewShort(0x8E, 0xCD24)
                self.readArray('blue_classes')
                for _ in range(count):
                    self.readString(xor=self.XOR)
                self.end()
                count = self.overviewShort(0x88, 0xF66C)
                self.readArray('green_classes')
                for _ in range(count):
                    self.readString(xor=self.XOR)
                self.end()
                count = self.overviewShort(0x82, 0xA257)
                self.readArray('colorless_classes')
                for _ in range(count):
                    self.readString(xor=self.XOR)
                self.end()
            else:
                self.skip(0x20)
                self.insert('5_non_focus', self.overviewShort(0x74, 0x7E7E) == self.overviewShort(0x76, 0xCD24) == self.overviewShort(0x78, 0xF66C) == self.overviewShort(0x7A, 0xA257) == 6)
            self.skip(0x50)
            self.skip(0x08) # tips
            self.skip(0x08) # units
            self.skip(0x10)
            self.readShort('sort_id', 0x5F1A)
            self.readShort('is_top', 0x495A, signed=True)
            self.skip(0x08) # classes count x4
            self.skip(0x02)
            self.readByte('tips_count', 0xFB)
            self.readByte('focus_count', 0x70)
            readTime(self, 'start', 0xD8D11EC213CC3ED1)
            readTime(self, 'end', 0x4477DFA58F8520A7)
            self.end()
        self.end()
        self.skip(0x08) # count

        nb = self.overviewLong(0x08)
        self.readArray('list2')
        for _ in range(nb):
            self.prepareObject()
            self.end()
        self.end()
        self.skip(0x08) # count

        nb = self.overviewLong(0x08)
        self.readArray('list3')
        for _ in range(nb):
            self.prepareObject()
            self.end()
        self.end()
        self.skip(0x08) # count

        nb = self.overviewLong(0x08)
        self.readArray('tips')
        for _ in range(nb):
            self.prepareObject()
            self.readString('unit', self.XOR)
            self.readString('tip', self.XOR)
            self.end()
        self.end()
        self.skip(0x08) # count

        self.end()

SummonReader = FocusReader