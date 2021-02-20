#!/usr/bin/env python3

from subprocess import Popen, PIPE, STDOUT
import json
import ctypes
from datetime import datetime

NONE_XORKEY = [
    0x00
]

ID_XORKEY = [
    0x81, 0x00, 0x80, 0xA4, 0x5A, 0x16, 0x6F, 0x78,
    0x57, 0x81, 0x2D, 0xF7, 0xFC, 0x66, 0x0F, 0x27,
    0x75, 0x35, 0xB4, 0x34, 0x10, 0xEE, 0xA2, 0xDB,
    0xCC, 0xE3, 0x35, 0x99, 0x43, 0x48, 0xD2, 0xBB,
    0x93, 0xC1
]

MSG_XORKEY = [
    0x6F, 0xB0, 0x8F, 0xD6, 0xEF, 0x6A, 0x5A, 0xEB,
    0xC6, 0x76, 0xF6, 0xE5, 0x56, 0x9D, 0xB8, 0x08,
    0xE0, 0xBD, 0x93, 0xBA, 0x05, 0xCC, 0x26, 0x56,
    0x65, 0x1E, 0xF8, 0x2B, 0xF9, 0xA1, 0x7E, 0x41,
    0x18, 0x21, 0xA4, 0x94, 0x25, 0x08, 0xB8, 0x38,
    0x2B, 0x98, 0x53, 0x76, 0xC6, 0x2E, 0x73, 0x5D,
    0x74, 0xCB, 0x02, 0xE8, 0x98, 0xAB, 0xD0, 0x36,
    0xE5, 0x37,
]

BGM_XORKEY = [
    0x6F, 0xC0, 0x37, 0xBC, 0xC7, 0x6F, 0x04, 0x3B,
    0x6E, 0x7B, 0x76, 0xB8, 0xC7, 0x2E, 0x0E, 0x01,
    0xE6, 0x64, 0x84, 0x2B, 0xDC, 0x57, 0x2C, 0x84,
    0xEF, 0xD0, 0x85, 0x90, 0x9D, 0x53, 0x2C, 0xC5,
    0xE5, 0xEA, 0x0D, 0x8F
]

LOGIN_XORKEY = [
    0xCD, 0x76, 0x95, 0x7D, 0x7A, 0xF5, 0xB3, 0x0B,
    0xE6, 0xC9, 0x39, 0x72, 0xFC, 0x9E, 0xE2, 0x73,
    0x3D, 0x31, 0x98, 0x23, 0xC0, 0x28, 0x2F, 0xA0,
    0xE6, 0x5E, 0xB3, 0x9C, 0x6C, 0x27, 0xA9, 0xCB,
    0xB7, 0x26, 0x68, 0x64
]

PORTRAIT_XORKEY = [
    0x2F, 0x08, 0x66, 0xED, 0x7C, 0x98, 0x34, 0x2A,
    0xE4, 0xAC, 0x41, 0xD1, 0xE5, 0x1F, 0xD2, 0x5E,
    0x28, 0x32, 0x76, 0xDE, 0x87, 0x0A, 0xA7, 0xF9,
    0x44, 0x28, 0x26, 0xC7, 0x25, 0x21, 0x06, 0x68,
    0xE3, 0x72, 0x96, 0x3A, 0x24, 0xEA, 0xA2, 0x4F,
    0xDF, 0xEB, 0x11, 0xDC, 0x50, 0x26, 0x3C, 0x78,
    0xD0, 0x89, 0x04, 0xA9, 0xF7, 0x4A, 0x26, 0x28,
    0xC9, 0x2B
]

#TUTORIAL    8A FC FE 39 5A 45 98 8D 6E FE 80 CE 08 74 14 95 EF 7B 70 06 04 C3 A0 BF 62 77 94 04 7A 34 F2 8E EE 6F 15 81
#VG          9A EC EE 29 81 9E C2 42 A1 8D F3 BD 7B 77 E3 F6 8C EC 3B 4D 4F 88 20 3F 63 E3 00 2C 52 1C DA D6 42 57 2D 4D
#GC          17 FC C9 EA 79 69 24 BD A4 54 0E 58 BD 8B 36 CD AF B4 E2 09 3C 1F 8C 9C D1 48 51 A1 FB AD 48 7E C3 38 5A 41
#SUMMON      24 38 F8 00 4C E0 2E 23 73 83 EF C4 84 8F F4 E9 D2 A5 22 3E FE 06 4A E6 28 25 75 85 E9 C2 82 89 F2 EF D4 A3	assets/Common/Summon/*.bin
#HOME        19 0E C6 29 AE 2F 5E 0C B0 D6 EE 53 A8 F3 8A 7B 98 79 9A 8D 45 AA 2D AC DD 8F 33 55 6D D0 2B 70 09 F8 1B FA	assets/Common/Home/hQ2uT_yaiphg/*.bin
#LOADING     9A EC 03 C4 01 1E 42 C2 21 51 2F 7C BA 6D F9 EC 96 F6 85 F3 1C DB 1E 01 5D DD 3E 4E 30 63 A5 72 E6 F3 89 E9	assets/Common/Loading/Data.bin
#BATTLE      71 1E 04 F5 47 7A 1C A2 3E 48 3B D8 95 89 28 52 4F 0E 17 37 04 C2 47 E1 E0 8F 95 64 D6 EB 8D 33 AF D9 AA 49 04 18 B9 C3 DE 9F 86 A6 95 53 D6 70	assets/Common/Battle/Asset/*.bin
#EFFECT_ARC  44 00 35 C1 FF 14 C8 91 F3 1E 1F 6B CC 64 59 D8 BC C0 CB 8F BA 4E 70 9B 47 1E 7C 91 90 E4 43 EB D6 57 33 4F	assets/Common/Effect/arc/*.bin
#SOUND_ARC   5A 60 70 80 A1 92 0C F5 27 82 92 58 1A 8A 56 7A 46 C7 F7 CD DD 2D 0C 3F A1 58 8A 2F 3F F5 B7 27 FB D7 EB 6A	assets/Common/Sound/arc/*.bin
#WB          7C 98 E2 55 A7 C1 ED BF 8E 61 87 51 D3 BC 53 2C 01 16 5A BE C4 73 81 E7 CB 99 A8 47 A1 77 F5 9A 75 0A 27 30	assets/Common/Wb-4glP03ab/*.bin
#HP          88 00 7A 39 9C E4 45 69 F0 EC F7 C1 3A 9D 1F E5 D9 06 0C C9 E8 1C BD 2C CB BB E3 9C 0F 5E CE 46 3C 7F DA A2 03 2F B6 AA B1 87 7C DB 59 A3 9F 40 4A 8F AE 5A FB 6A 8D FD A5 DA 49 18	assets/Common/Home/9h-bR4lQy/*.bin

ENCR_KEY = [
    0x4B, 0x0D, 0xB4, 0x88, 0x61, 0x7C, 0x60, 0xA1,
    0x2B, 0x09, 0x40, 0xE9, 0xED, 0x92, 0xA6, 0x8F
]

def getBool(data, idx, xor=None):
    return False if getByte(data, idx, xor) == 0 else True

def getByte(data, idx, xor=None):
    if (len(data[idx:]) < 0x01):
        raise IndexError
    v = 0
    for i in range(1):
        v += data[i+idx] << 8*i
        #data[i+idx] = 0x00
    if xor:
        return v ^ xor
    return v

def getSByte(data, idx, xor=None):
    v = getByte(data, idx, xor)
    if v > 0x7F:
        v = -(v ^ 0xFF) - 1
    return v

def getShort(data, idx, xor=None):
    if (len(data[idx:]) < 0x02):
        raise IndexError
    v = 0
    for i in range(2):
        v += data[i+idx] << 8*i
        #data[i+idx] = 0x00
    if xor:
        return v ^ xor
    return v

def getSShort(data, idx, xor=None):
    v = getShort(data, idx, xor)
    if v > 0x7FFF:
        v = -(v ^ 0xFFFF) - 1
    return v

def getInt(data, idx, xor=None):
    if (len(data[idx:]) < 0x04):
        raise IndexError
    v = 0
    for i in range(4):
        v += data[i+idx] << 8*i
        #data[i+idx] = 0x00
    if xor:
        return v ^ xor
    return v

def getSInt(data, idx, xor=None):
    v = getInt(data, idx, xor)
    if v > 0x7FFFFFFF:
        v = -(v ^ 0xFFFFFFFF) - 1
    return v

def getLong(data, idx, xor=None):
    if (len(data[idx:]) < 0x08):
        raise IndexError
    v = 0
    for i in range(8):
        v += data[i+idx] << 8*i
        #data[i+idx] = 0x00
    if xor:
        return v ^ xor
    return v

def getSLong(data, idx, xor=None):
    v = getLong(data, idx, xor)
    if v > 0x7FFFFFFFFFFFFFFF:
        v = -(v ^ 0xFFFFFFFFFFFFFFFF) - 1
    return v

def getStat(data, idx):
    return {
        "hp": getShort(data, idx+0x00, 0xD632),
        "atk": getShort(data, idx+0x02, 0x14A0),
        "spd": getShort(data, idx+0x04, 0xA55E),
        "def": getShort(data, idx+0x06, 0x8566),
        "res": getShort(data, idx+0x08, 0xAEE5),
        #"unknow": getShort(data, idx+0x0A),
        #"unknow": getShort(data, idx+0x0C),
        #"unknow": getShort(data, idx+0x0E),
    }

def getAvail(data, idx):
    try:
        result = {
            "start": datetime.utcfromtimestamp(getLong(data, idx, 0xDC0DA236C537F660)).isoformat() + "Z" if getLong(data, idx+0x00) ^ 0xDC0DA236C537F660 != 0xFFFFFFFFFFFFFFFF else None,
            "finish": (datetime.utcfromtimestamp(getLong(data, idx+0x08, 0xC8AD692AFABD56E9)).isoformat() + "Z") if getLong(data, idx+0x08) ^ 0xC8AD692AFABD56E9 != 0xFFFFFFFFFFFFFFFF else None,
            "avail_sec": getSLong(data, idx+0x10, 0x7311F0404108A6E0),
            "cycle_sec": getSLong(data, idx+0x18, 0x6B227EC9D51B5721),
        }
    except:
        result = {
            "start": hex(getLong(data, idx+0x00, 0xDC0DA236C537F660)),
            "finish": hex(getLong(data, idx+0x08, 0xC8AD692AFABD56E9)),
            "avail_sec": hex(getSLong(data, idx+0x10, 0x7311F0404108A6E0)),
            "cycle_sec": hex(getSLong(data, idx+0x18, 0x6B227EC9D51B5721)),
        }
    return result

def xorString(data, xor):
    s = []
    size = min(len(data), (data.index(0) if 0 in data else len(data)))
    for i in range(size):
        if data[i] != xor[i%len(xor)]:
            s += [(data[i] ^ xor[i%len(xor)])]
        else:
            s += [(data[i])]
        #data[i] = 0x00
    return bytes(s).decode('utf8', 'replace')

def getString(data, idx, xor=ID_XORKEY):
    off = getLong(data, idx)
    return xorString(data[off:], xor) if off != 0 else None

from Crypto.Cipher import AES
from Crypto.Util import Counter

rewardParser = [
    lambda data, idx: ({"kind": 0x00, "_type": "orb", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x01, "_type": "hero", "len": getByte(data, idx+1), "id_tag": xorString(data[idx+2:idx+2+getByte(data, idx+1)], [0]), "rarity": getShort(data, idx+2+getByte(data, idx+1))}, idx+4+getByte(data, idx+1)),
    lambda data, idx: ({"kind": 0x02, "_type": "hero_feather", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x03, "_type": "stamina_potion", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x04, "_type": "dueling_crest", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x05, "_type": "lights_blessing", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x06, "_type": "exp_resource", "count": getShort(data, idx+1), "great": getBool(data, idx+3), "shard_color": getByte(data, idx+4)}, idx+5),
    lambda data, idx: ({"kind": 0x07, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x08, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x09, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x0A, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x0B, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x0C, "_type": "badge", "count": getShort(data, idx+1), "great": getBool(data, idx+3), "badge_color": getByte(data, idx+4)}, idx+5),
    lambda data, idx: ({"kind": 0x0D, "_type": "battle_flag", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x0E, "_type": "sacred_seal", "len": getByte(data, idx+1), "id_tag": xorString(data[idx+2:idx+2+getByte(data, idx+1)], [0])}, idx+2+getByte(data, idx+1)),
    lambda data, idx: ({"kind": 0x0F, "_type": "arena_assault_item", "count": getShort(data, idx+1), "aa_kind": getByte(data, idx+3)}, idx+4),
    lambda data, idx: ({"kind": 0x10, "_type": "sacred_coin", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x11, "_type": "refining_stone", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x12, "_type": "divine_dew", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x13, "_type": "arena_medal", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x14, "_type": "blessing", "count": getShort(data, idx+1), "element": getByte(data, idx+3)}, idx+4),
    lambda data, idx: ({"kind": 0x15, "_type": "conquest_lance", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x16, "_type": "accessory", "len": getByte(data, idx+1), "id_tag": xorString(data[idx+2:idx+2+getByte(data, idx+1)], [0])}, idx+2+getByte(data, idx+1)),
    lambda data, idx: ({"kind": 0x17, "_type": "fb_conversation", "support_rank": getByte(data, idx+1), "len": getByte(data, idx+2), "id_tag": xorString(data[idx+3:idx+3+getByte(data, idx+2)], [0])}, idx+3+getByte(data, idx+2)),
    lambda data, idx: ({"kind": 0x18, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x19, "_type": "arena_crown", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x1A, "_type": "heroic_grail", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x1B, "_type": "aether_stone", "count": getShort(data, idx+1), "len": getByte(data, idx+3), "id_tag": xorString(data[idx+4:idx+4+getByte(data, idx+3)], [0])}, idx+4+getByte(data, idx+3)),
    lambda data, idx: ({"kind": 0x1C, "_type": "throne", "count": getShort(data, idx+1), "throne_type": getByte(data, idx+3)}, idx+4),
    lambda data, idx: ({"kind": 0x1D, "_type": "summoning_ticket", "count": getShort(data, idx+1), "len": getByte(data, idx+3), "id_tag": xorString(data[idx+4:idx+4+getByte(data, idx+3)], [0])}, idx+4+getByte(data, idx+3)),
    lambda data, idx: ({"kind": 0x1E, "_type": "dragonflower", "count": getShort(data, idx+1), "move_type": getByte(data, idx+3)}, idx+4),
    lambda data, idx: ({"kind": 0x1F, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x20, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x21, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x22, "_type": "havoc_axe", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x23, "_type": "background_music", "len": getByte(data, idx+1), "id_tag": xorString(data[idx+2:idx+2+getByte(data, idx+1)], [0])}, idx+2+getByte(data, idx+1)),
    lambda data, idx: ({"kind": 0x24, "_type": "forma_torch", "count": getShort(data, idx+1), "len": getByte(data, idx+3), "id_tag": xorString(data[idx+4:idx+4+getByte(data, idx+3)], [0])}, idx+4+getByte(data, idx+3)),
    lambda data, idx: ({"kind": 0x25, "_type": "midgard_gem", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x26, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x27, "_type": "divine_code", "count": getShort(data, idx+1), "len": getByte(data, idx+3), "id_tag": xorString(data[idx+4:idx+4+getByte(data, idx+3)], [0])}, idx+4+getByte(data, idx+3)),
    lambda data, idx: ({"kind": 0x28, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x29, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x2A, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x2B, "_type": "unknow"}, idx+1),
    lambda data, idx: ({"kind": 0x2C, "_type": "guardian_shield", "count": getShort(data, idx+1)}, idx+3),
    lambda data, idx: ({"kind": 0x2D, "_type": "trait_fruit", "count": getShort(data, idx+1)}, idx+3),
    #lambda data, idx: ({"kind": 0x25, "_type": "", "count": getShort(data, idx+1)}, idx+3),
]

def getReward(data, idx, size):
    off1 = getLong(data, idx)
    size = size - 0x08-0x10
    if getLong(data, off1+size) != 0x160707001B9AD871:
        return

    iv = [getByte(data, off1+size+0x08+0x01*i) for i in range(16)]
    iv.reverse()
    ivValue = 0
    for i in range(16):
        ivValue += iv[i] << 8*i
    cipher = AES.new(bytes(ENCR_KEY), AES.MODE_CTR, counter=Counter.new(128, initial_value=ivValue))
    data = list(cipher.decrypt(bytes(data[off1:off1+size])))
    idx = 1

    result = []
    for i in range(getByte(data, 0)):
        kind = getByte(data, idx)
        if kind >= len(rewardParser):
            r, idx = {"kind": kind, "_type": "unknow"}, idx+1
        else:
            r, idx = rewardParser[kind](data, idx)
        result += [r]
    return result