#! /usr/bin/env python3

from .Decompresser import Decompresser

class ReaderError(IOError):
    "An error occured on the reader"

class InvalidReaderError(ReaderError):
    "An invalid reader was chose for the data"

class IncompleteReaderError(ReaderError):
    "The reader was not completed"

class InvalidTypeReaderError(InvalidReaderError):
    "Trying to add a new object on an incompatible reader. Be mindful of the key."

DEFAULT_XOR = [
    0x81, 0x00, 0x80, 0xA4, 0x5A, 0x16, 0x6F, 0x78,
    0x57, 0x81, 0x2D, 0xF7, 0xFC, 0x66, 0x0F, 0x27,
    0x75, 0x35, 0xB4, 0x34, 0x10, 0xEE, 0xA2, 0xDB,
    0xCC, 0xE3, 0x35, 0x99, 0x43, 0x48, 0xD2, 0xBB,
    0x93, 0xC1
]

class Reader:
    """Base class for all Reader.
    
    Can either be created using the content of an `.bin.lz` file, or by calling
    the class method `fromAssets` with the path of the file, relative to the `/assets/` folder.

    Holds an `object` property which holds the parsed content when the Reader is valid.
    Any instance can be tested to check for its validity.

    Implements several utility methods for parsing, which should *only* be used by the
    class for parsing the internal binary data:
    - `skip`: Move the head of the reader forward by @n bytes
    - `insert`: Insert a new element into the list/object
    - `prepare(Array|Object)`: Insert a new array/object into the object and set it as current
    - `read(Array|Object)`: Same as `prepare*`, but move the head to the position it points
    - - `readList`: Same as `readArray`. Used for object holding only an array and its size
    - `end`: End the current array/object and reset the head to its position before the jump
    - `overview*`: Return the element at the given relative position
    - `get*`: Return the element at the head, and move the head forward
    - `read*`: Insert the element at the head, and move the head forward
    """

    def __init__(self, buff):
        buff = bytes(Decompresser(buff).data)
        self._header = buff[0x00:0x20]

        bodySize = int.from_bytes(self._header[0x04:0x08], 'little')
        ptrTblCount = int.from_bytes(self._header[0x08:0x0C], 'little')
        strTblCount = int.from_bytes(self._header[0x0C:0x10], 'little')

        self._buff = buff[0x20:]
        self._ptrTbl = []
        self._strTbl = {}

        offStrTbl = 0x20 + bodySize + ptrTblCount*0x08 + strTblCount*0x08
        for i in range(strTblCount):
            off = 0x20 + bodySize + ptrTblCount*0x08 + i*0x08
            bodyOff = int.from_bytes(buff[off:off+0x04], 'little')
            strTblOff = int.from_bytes(buff[off+0x04:off+0x08], 'little')
            self._strTbl[bodyOff] = self.decodeString(buff[offStrTbl+strTblOff:offStrTbl+strTblOff+0x30])

        self._i = 0
        self._obj = None
        self._stack = []

    @classmethod
    def fromAssets(cls, path:str):
        from ..PersonalData import BINLZ_ASSETS_DIR_PATH as basePath
        from os.path import isfile
        if not isfile(basePath + path): return cls([])
        return cls(open(basePath + path, 'rb').read())

    def isValid(self):
        return len(self._buff) != 0
    __bool__ = isValid

    @property
    def object(self):
        if not self.isValid(): return
        if self._obj == None or len(self._stack) > 0: raise IncompleteReaderError
        return self._obj

    def skip(self, count:int):
        self._i += count

    def insert(self, key:str, obj):
        if len(self._stack) == 0:
            if self._obj is None and isinstance(obj, (dict, list)): self._obj = obj
            else: raise InvalidTypeReaderError
        elif key is None and isinstance(self._stack[-1][0], list):
            self._stack[-1][0].append(obj)
        elif key is not None and isinstance(self._stack[-1][0], dict):
            self._stack[-1][0][key] = obj
        else:
            raise InvalidTypeReaderError

    def end(self):
        if len(self._stack) == 0: raise ReaderError
        if self._stack[-1][1] != 0:
            self._i = self._stack[-1][1]
        self._stack.pop()


    def readObject(self, key:str=None):
        obj = {}
        idx = self.getLong()
        if idx == 0x00:
            self.insert(key, None)
            return False
        self.insert(key, obj)
        self._stack.append((obj, self._i))
        self._i = idx
        return True

    def prepareObject(self, key:str=None):
        obj = {}
        self.insert(key, obj)
        self._stack.append((obj, 0))


    def readArray(self, key:str=None):
        obj = []
        idx = self.getLong()
        self.insert(key, obj)
        self._stack.append((obj, self._i))
        self._i = idx

    def readList(self, key:str=None, xorSize=0, inverse=False) -> int:
        self.readArray(key)
        if self._i == 0: return 0
        idx = self.overviewLong(0x00 if not inverse else 0x08)
        size = self.overviewLong(0x08 if not inverse else 0x00, xorSize)
        self._i = idx
        return size

    def prepareArray(self, key:str=None):
        obj = []
        self.insert(key, obj)
        self._stack.append((obj, 0))


    def readString(self, key:str=None, xor=DEFAULT_XOR): self.insert(key, self.getString(xor))
    def getString(self, xor=DEFAULT_XOR): self.skip(8); return self.overviewString(-8, xor)
    def overviewString(self, off=0, xor=DEFAULT_XOR):
        idx = self.overviewLong(off)
        if idx == 0: return None
        return Reader.decodeString(self._buff[idx:idx+0x100], xor)

    def readStringHeader(self, key:str=None): self.insert(key, self.getStringHeader())
    def getStringHeader(self): return self._strTbl.get(self._i)

    @staticmethod
    def decodeString(str:str|bytes, xor=[0]):
        sizeXor = len(xor)
        s = []
        for i,c in enumerate(str):
            if c == 0: break
            char = c ^ xor[i%sizeXor]
            s.append(char if char != 0 else c)
        return bytes(s).decode('utf8', 'replace')


    def readLong(self, key:str=None, xor=0, signed=False): self.insert(key, self.getLong(xor, signed))
    def getLong(self, xor=0, signed=False): self.skip(8); return self.overviewLong(-8, xor, signed)
    def overviewLong(self, off=0, xor=0, signed=False):
        v = int.from_bytes(self._buff[self._i+off:self._i+off+8], 'little')
        v ^= xor
        if signed and v > 0x7FFFFFFFFFFFFFFF: v = -(v ^ 0xFFFFFFFFFFFFFFFF) - 1
        return v

    def readInt(self, key:str=None, xor=0, signed=False): self.insert(key, self.getInt(xor, signed))
    def getInt(self, xor=0, signed=False): self.skip(4); return self.overviewInt(-4, xor, signed)
    def overviewInt(self, off=0, xor=0, signed=False):
        v = int.from_bytes(self._buff[self._i+off:self._i+off+4], 'little')
        v ^= xor
        if signed and v > 0x7FFFFFFF: v = -(v ^ 0xFFFFFFFF) - 1
        return v

    def readShort(self, key:str=None, xor=0, signed=False): self.insert(key, self.getShort(xor, signed))
    def getShort(self, xor=0, signed=False): self.skip(2); return self.overviewShort(-2, xor, signed)
    def overviewShort(self, off=0, xor=0, signed=False):
        v = int.from_bytes(self._buff[self._i+off:self._i+off+2], 'little')
        v ^= xor
        if signed and v > 0x7FFF: v = -(v ^ 0xFFFF) - 1
        return v

    def readByte(self, key:str=None, xor=0, signed=False): self.insert(key, self.getByte(xor, signed))
    def getByte(self, xor=0, signed=False): self.skip(1); return self.overviewByte(-1, xor, signed)
    def overviewByte(self, off=0, xor=0, signed=False):
        v = int.from_bytes(self._buff[self._i+off:self._i+off+1], 'little')
        v ^= xor
        if signed and v > 0x7F: v = -(v ^ 0xFF) - 1
        return v
    
    def readBool(self, key:str=None, xor=0): self.insert(key, self.getBool(xor))
    def getBool(self, xor=0): return self.getByte(xor) != 0
    def overviewBool(self, off=0, xor=0): return self.overviewByte(off, xor) != 0

    def readMask(self, key:str=None, nbByte=1, xor=0): self.insert(key, self.getMask(nbByte, xor))
    def getMask(self, nbBytes=4, xor=0):
        mask = int.from_bytes(self._buff[self._i:self._i+nbBytes], 'little')
        mask ^= xor
        l = []
        for i in range(8*nbBytes):
            if (mask & (1 << i)) != 0:
                l.append(i)
        self.skip(nbBytes)
        return l

    def assertBytes(self, nbBytes, xor, key='_'):
        from .globals import WARNING
        mask = int.from_bytes(self._buff[self._i:self._i+nbBytes], 'little')
        if (mask ^ xor) != 0:
            print(WARNING + f'{self.__class__.__name__}: Expected 0x{xor:x}, got 0x{mask:x} (XOR 0x{xor^mask:x}) ({key})')
        self.skip(nbBytes)

    def assertPadding(self, nbBytes):
        from .globals import WARNING
        if int.from_bytes(self._buff[self._i:self._i+nbBytes], 'little') != 0:
            print(WARNING + f'{self.__class__.__name__}: Expected {nbBytes} padding not found ({",".join([hex(i) for _,i in self._stack if i != 0] + [hex(self._i)])})')
        self.skip(nbBytes)


class IReader(Reader):
    """Parent class for all Reader of FeH assets.
    
    Should *always* be used as a parent class, and using the `fromAssets` constructor.
    The name of the file, without extension, should be passed instead of the relative path.

    Holds an `object` property which holds the parsed content when the Reader is valid, or None.
    Any instance can be tested to check for its validity.
    
    Any child needs to overload `_basePath` as the relative folder to the assets and
    the `parse` method.
    """
    _basePath = ''

    @classmethod
    def fromAssets(cls, name:str):
        return super().fromAssets(cls._basePath + name + '.bin.lz')

    @property
    def object(self):
        if not self.isValid(): return
        if self._obj == None:
            self.parse()
        return super().object

    def parse(self):
        raise IncompleteReaderError


def readStat(reader: Reader, key:str=None):
    reader.prepareObject(key)
    reader.readShort('hp', 0xD632, True)
    reader.readShort('atk', 0x14A0, True)
    reader.readShort('spd', 0xA55E, True)
    reader.readShort('def', 0x8566, True)
    reader.readShort('res', 0xAEE5, True)
    #reader.readShort('')
    #reader.readShort('')
    #reader.readShort('')
    reader.skip(0x06)
    reader.end()

def readTime(reader: Reader, key:str=None, xor=0):
    from .globals import TIME_FORMAT
    from datetime import datetime
    timestamp = reader.getLong(xor)
    try:
        time = datetime.utcfromtimestamp(timestamp).strftime(TIME_FORMAT) if timestamp not in [0xFFFFFFFFFFFFFFFF,xor] else None
    except:
        time = None
    reader.insert(key, time)

def readAvail(reader: Reader, key:str=None):
    from ..Tool.misc import timeDiff
    off = reader.overviewLong()
    if off == 0:
        reader.skip(8)
        reader.insert(key, None)
    else:
        reader.prepareObject(key)
        readTime(reader, 'start', 0xDC0DA236C537F660)
        readTime(reader, 'end', 0xC8AD692AFABD56E9)
        if reader._stack[-1][0]['end']:
            reader._stack[-1][0]['end'] = timeDiff(reader._stack[-1][0]['end'], 1)
        reader.readLong('avail_sec', 0x7311F0404108A6E0, True)
        reader.readLong('cycle_sec', 0x6B227EC9D51B5721, True)
        if reader.getLong() not in (0xB5,0xB7): print('Unexpected number on `readAvail`')
        reader.end()

def readReward(reader: Reader, key: str=None, xorSize=0, offSize=8):
    from ..Utility.Reader.Reward import readReward
    return readReward(reader, key, xorSize, offSize)


def getAllStrings(reader: Reader, key=DEFAULT_XOR) -> dict[str,str]:
    t = {}
    for i in range(len(reader._buff) // 0x08):
        t[hex(i*0x08)] = Reader.decodeString(reader._buff[i*0x08:i*0x08+0x40], key)
    return t

def getAllRewards(reader: Reader, payload=0x48):
    from ..Utility.Reader.Reward import RewardReader
    r = Reader([])
    r._header = reader._header
    r._buff = reader._buff
    t = {}
    while r._i < len(r._buff):
        off = r.getLong()
        if off == 0: continue
        rewardReader = RewardReader(reader._buff[off:off+payload])
        if not rewardReader.isValid(): continue
        t[hex(r._i-0x08)] = rewardReader.object
    return t
