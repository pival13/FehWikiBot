#! /usr/bin/env python3

from ...Tool.Reader import IReader, Reader, InvalidReaderError

class MessageReader(IReader):
    XOR = [
        0x6F, 0xB0, 0x8F, 0xD6, 0xEF, 0x6A, 0x5A, 0xEB,
        0xC6, 0x76, 0xF6, 0xE5, 0x56, 0x9D, 0xB8, 0x08,
        0xE0, 0xBD, 0x93, 0xBA, 0x05, 0xCC, 0x26, 0x56,
        0x65, 0x1E, 0xF8, 0x2B, 0xF9, 0xA1, 0x7E, 0x41,
        0x18, 0x21, 0xA4, 0x94, 0x25, 0x08, 0xB8, 0x38,
        0x2B, 0x98, 0x53, 0x76, 0xC6, 0x2E, 0x73, 0x5D,
        0x74, 0xCB, 0x02, 0xE8, 0x98, 0xAB, 0xD0, 0x36,
        0xE5, 0x37
    ]

    @classmethod
    def fromAssets(cls, path):
        if path.find('/Message/') == -1: raise InvalidReaderError
        return super(IReader,cls).fromAssets(path)

    def parse(self):
        self.prepareArray()
        for _ in range(self.getLong()):
            self.prepareObject()
            self.readString('key', self.XOR)

            # self.readString('value', self.XOR) # readString will only retrieve at most 256 characters
            idx = self.getLong()
            s = None
            if idx != 0:
                maxi = self._buff.find(0, idx)
                s = self.decodeString(self._buff[idx:maxi], self.XOR)
            self.insert('value', s)

            self.end()
        self.end()
