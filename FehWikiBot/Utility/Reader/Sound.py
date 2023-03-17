#! /usr/bin/env python3

from ...Tool.Reader import IReader

class SoundReader(IReader):
    _basePath = 'Common/Sound/arc/'

    XOR = [
        0x5A, 0x60, 0x70, 0x80, 0xA1, 0x92, 0x0C, 0xF5,
        0x27, 0x82, 0x92, 0x58, 0x1A, 0x8A, 0x56, 0x7A,
        0x46, 0xC7, 0xF7, 0xCD, 0xDD, 0x2D, 0x0C, 0x3F,
        0xA1, 0x58, 0x8A, 0x2F, 0x3F, 0xF5, 0xB7, 0x27,
        0xFB, 0xD7, 0xEB, 0x6A
    ]

    TYPE = {8: 'Simple', 10: 'Compound', 12: 'Random', 16: 'Alias', 24: 'Alias'}
    KIND = ['BGM', 'Sound', 'Voice']

    def parse(self):
        print(self._strTbl)
        nb = self.overviewLong(0x08, 0x00)
        self.readArray()
        for _ in range(nb):
            self.readObject()
            self.insert('off', hex(self._i+0x20))
            self.readStringHeader('id_tag')
            self.readString('name', self.XOR)
            count = self.getByte()
            type = self.TYPE[self.getByte()]
            self.insert('type', type)
            self.skip(0x02)
            self.insert('kind', self.KIND[self.getInt()])
            self.prepareArray('list')
            for _ in range(count):
                self.readObject()
                if type == 'Alias':
                    self._i = self.getLong()
                    self.readString('original', self.XOR)
                else:
                    self.insert('off', hex(self._i+0x20))
                    self.readString('file', self.XOR)
                    self.readString('archive', self.XOR)
                    # More
                self.end()
            self.end()
            self.end()
        self.end()