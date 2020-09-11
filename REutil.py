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
            "finish": (datetime.utcfromtimestamp(getLong(data, idx+0x08, 0xC8AD692AFABD56E9) - 1).isoformat() + "Z") if getLong(data, idx+0x08) ^ 0xC8AD692AFABD56E9 != 0xFFFFFFFFFFFFFFFF else None,
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
    for i in range(min(len(data), (data.index(0) if 0 in data else len(data)))):
        if data[i] != xor[i%len(xor)]:
            s += [(data[i] ^ xor[i%len(xor)])]
        else:
            s += [(data[i])]
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
    lambda data, idx: ({"kind": 0x06, "_type": "exp_resource", "count": getShort(data, idx+1), "great": not getBool(data, idx+3), "shard_color": getByte(data, idx+4)}, idx+5),
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
    lambda data, idx: ({"kind": 0x24, "_type": "unknow"}, idx+1),
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