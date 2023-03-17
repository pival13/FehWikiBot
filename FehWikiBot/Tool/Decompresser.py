#! /usr/bin/env python3

class InvalidFormatError(TypeError):
    "Non LZ11 compressed data"

class Decompresser:
    __slots__ = '_buff', '_i'

    def __init__(self, buffer):
        self._buff = list(buffer)
        self._i = 0

    @property
    def data(self):
        if self._buff == []: return []
        if self._i == 0: self.decompress()
        return self._buff
    
    def readByte(self):
        self._i += 1
        return self._buff[self._i-1]

    def readInt(self):
        buff = self._buff[self._i:self._i+4]
        self._i += 4
        return int.from_bytes(bytes(buff), 'little')

    def _decrypt(self, seed):
        xorkey = list((0x8083 * int.from_bytes(seed, 'little')).to_bytes(8, 'little'))
        for i in range(4, len(self._buff)):
            xor = xorkey[i%4]
            xorkey[i%4] = self._buff[i]
            self._buff[i] ^= xor

    def _decompress(self):
        size = self.readInt() >> 0o10
        if size == 0:
            size = self.readInt()

        self._buff += [0x00]*4 # To protect the read
        # Decompress data
        mask = 1
        off = 0
        mem = [0x00] * 0x1000
        buff = [0x00] * size
        while off < size:
            if mask == 1:
                flags = self.readByte()
                mask <<= 7
            else: mask >>= 1

            # Simple append
            if (flags & mask) == 0:
                b = self.readByte()
                buff[off] = b
                mem[off%0x1000] = b
                off += 1
            # Copy previous data
            else:
                b = int.from_bytes(bytes(self._buff[self._i:self._i+4]), 'big', signed=False)
                if   (b & 0xF0000000) == 0x10000000:# 60019009
                    count = ((b & 0x0FFFF000) >> 12) + 0x0111
                    off2 =  ((b & 0x00000FFF) >>  0) + 0x001
                    self._i += 4
                elif (b & 0xF0000000) == 0x00000000:
                    count = ((b & 0x0FF00000) >> 20) + 0x11
                    off2 =  ((b & 0x000FFF00) >>  8) + 0x001
                    self._i += 3
                else:
                    count = ((b & 0xF0000000) >> 28) + 0x1
                    off2 =  ((b & 0x0FFF0000) >> 16) + 0x001
                    self._i += 2

                if off2 > off:
                    self._buff.clear()
                    raise InvalidFormatError
                for i in range(count):
                    b = mem[(off+i-off2) % 0x1000]
                    buff[off+i] = b
                    mem[(off+i)%0x1000] = b
                off += count
        self._buff = buff

    def decompress(self):
        seed = bytes(self._buff[1:4])
        if self._buff[0] == 0x04 and int.from_bytes(seed, 'little') == len(self._buff)-4:
            self._decrypt(seed)
            self._buff = self._buff[4:]
        elif self._buff[0] == 0x17 and self._buff[0x04] == 0x11:
            self._buff = self._buff[4:]
            self._decrypt(seed)
            self._decompress()
        else:
            self._buff.clear()
            raise InvalidFormatError
        open('./_decompress.bin', 'bw').write(bytes(self._buff))