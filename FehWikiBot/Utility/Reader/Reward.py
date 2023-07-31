#! /usr/bin/env python3

from ...Tool.Reader import Reader, IReader

class RewardReader(IReader):
    ENCR_KEY = bytes([0x4B, 0x0D, 0xB4, 0x88, 0x61, 0x7C, 0x60, 0xA1, 0x2B, 0x09, 0x40, 0xE9, 0xED, 0x92, 0xA6, 0x8F])

    def __init__(self, buff):
        self._header = [0]*0x20
        self._buff = bytes(buff)
        self._i = 0
        self._obj = None
        self._stack = []

    def isValid(self):
        return super().isValid() and self.overviewLong(-(self._i+0x18)) == 0x160707001B9AD871

    def parse(self):
        from Crypto.Cipher import AES
        from Crypto.Util import Counter

        if not self.isValid(): return
        iv = int.from_bytes(self._buff[-0x10:], 'big')
        cipher = AES.new(self.ENCR_KEY, AES.MODE_CTR, counter=Counter.new(128, initial_value=iv))

        self._buff = cipher.decrypt(self._buff[:-0x18]) + self._buff[-0x18:]
        self.prepareArray()
        for _ in range(self.getByte()):
            self.parseOne(self.getByte())
        self.end()
    
    def parseOne(self, kind):
        from ...Tool.globals import ITEM_KIND, COLOR, MOVE_TYPE, BLESSING, TODO
        FB_RANK = [ 'C', 'B', 'A', 'S' ]
        AA_ITEM = [
            'Elixir', 'Fortifying Horm', 'Special Blade', 'Infantry Boots', 'Naga\'s Tear',
            'Dancer\'s Veil', 'Lightning Charm', 'Panic Charm', 'Fear Charm', 'Pressure Charm'
        ]
        REWARDS = {
            # (hasCount, hasStr, others)
            0x00: (True,  False, []), # Orb
            0x01: (False, True,  [lambda:self.readShort('rarity')]), #Hero
            0x02: (True,  False, []), # Feather
            0x03: (True,  False, []), # Stamina Potion
            0x04: (True,  False, []), # Dueling Crest
            0x05: (True,  False, []), # Light's Blessing
            0x06: (True,  False, [lambda:self.readBool('great'), lambda:self.insert('color', COLOR[self.getByte()])]), # Exp
            0x0C: (True,  False, [lambda:self.readBool('great'), lambda:self.insert('color', COLOR[self.getByte()+1])]), # Badge
            0x0D: (True,  False, []), # VG Stamina
            0x0E: (False, True,  []), # Seal
            0x0F: (True,  False, [lambda:self.insert('item', AA_ITEM[self.getByte()])]),
            0x10: (True,  False, []), # Sacred Coin
            0x11: (True,  False, []), # Refining Stone
            0x12: (True,  False, []), # Divine Dew
            0x13: (True,  False, []), # Arena Medal
            0x14: (True,  False, [lambda:self.insert('element', BLESSING[self.getByte()])]), # Blessing
            0x15: (True,  False, []), # GC Stamina
            0x16: (False, True,  []), # Accessory
            0x17: (False, True,  []), # FB conv
            0x19: (True,  False, []), # Arena Crown
            0x1A: (True,  False, []), # Heroic Grail
            0x1B: (True,  True,  []), # AR Item
            0x1C: (True,  False, [lambda:self.readByte('color')]), 
            0x1D: (True,  True,  []), # Ticket
            0x1E: (True,  False, [lambda:self.insert('move', MOVE_TYPE[self.getByte()])]), # Dragonflower
            0x22: (True,  False, []), # RS Stamina
            0x23: (True,  True,  []), # Music
            0x24: (True,  True,  []), # HoF Stamina
            0x25: (True,  False, []), # Midgard Gem
            0x27: (True,  True,  []), # Divine Code
            0x2B: (True,  False, []), # Forma Soul
            0x2C: (True,  False, []), # FP Stamina
            0x2D: (True,  False, []), # Trait Fruit
            0x2E: (True,  False, []), # Celestial Stone
            0x32: (True,  True,  []), # BW Stamina
        }

        self.prepareObject()

        hasCount,hasString,others = REWARDS.get(kind, (False,False,[]))
        if kind in ITEM_KIND or kind == 0x17:
            self.insert('kind', ITEM_KIND[kind])
        else:
            self.insert('kind', f'Unknow ({kind}])')
            print(TODO + f'Unknow reward: {kind}')
        if hasCount:
            self.readShort('count')
        if kind == 0x17: self.insert('rank',FB_RANK(self.getByte()))
        if hasString:
            l = self.getByte()
            self.insert('id_tag', self.decodeString(self._buff[self._i:self._i+l]))
            self.skip(l)
        for f in others: f()

        self.end()

def readReward(reader:Reader, key:str=None, xorSize=0, offSize=8):
    size = reader.overviewInt(offSize, xorSize) # 0x48 == 72, + 0x10 x K
    off = reader.getLong()
    if offSize == 8: reader.skip(4)
    if size != 0 and (size-72)%16 != 0: print('Reward size:', size)
    obj = None
    if off != 0:
        rewardReader = RewardReader(reader._buff[off:off+size])
        if rewardReader.isValid(): obj = rewardReader.object
    reader.insert(key, obj)

Reader.readReward = readReward