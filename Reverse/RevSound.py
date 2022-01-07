#!/usr/bin/env python3

from os.path import isfile

import REutil as util

getStringSound = lambda data, off: util.getString(data, off, util.SOUND_XORKEY)
getStringBgm = lambda data, off: util.getString(data, off, util.BGM_XORKEY)
from sys import stderr

def parseSound(data):
    result = []
    nbGroup = util.getLong(data, 0x08)
    for iGr in range(nbGroup):
        offGr = util.getLong(data, util.getLong(data, 0x00)+0x08*iGr)
        obj = {
            "id_tag": util.getString(data, offGr+0x00, util.SOUND_XORKEY),
            "count": util.getByte(data, offGr+0x08),
            "kind": util.getByte(data, offGr+0x09),#8 -> Simple music, 10 -> addition musics, 12 -> random music, 16 & 24 -> link to another music
            "_unknow3": hex(util.getShort(data, offGr+0x0A)),
            "audio_kind": util.getInt(data, offGr+0x0C),#0 -> BGM, 1 -> Sound, 2 -> Voice
            "list": [{
                "file": util.getString(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x00, util.SOUND_XORKEY),
                "archive": util.getString(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x08, util.SOUND_XORKEY),
                #"_ptr1": {
                #    "_unknow1": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x10)),
                #    "_unknow2": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x10)+0x04),
                #    "_unknow3": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x10)+0x08),
                #    "_unknow4": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x10)+0x0C),
                #    "_unknow5": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x10)+0x10),
                #    "_unknow6": util.getInt(data, util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x10)+0x14),
                #},
                #"_ptr2": hex(util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x18)),
                #"_ptr3": hex(util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x20)),
                #"_unknow1": hex(util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x28)),
                #"_unknow2": hex(util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x30)),
                #"_unknow3": hex(util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x38)),
                #"_unknow4": hex(util.getLong(data, util.getLong(data, offGr+0x10+0x08*iMsc)+0x40)),
            } for iMsc in range(util.getByte(data, offGr+0x08))],
        }
        if obj["kind"] == 16 or obj["kind"] == 24:
            for i in range(obj["count"]):
                obj["list"][i]["_ref"] = getStringSound(data, util.getLong(data, util.getLong(data, offGr+0x10+0x08*i)+0x00))
        result += [obj]
    return result

def parseStageBGM(data, header):
    result = []
    nbGroup = util.getLong(data, 0x08, 0x0)
    stringOffsetTable = util.getInt(header, 0x04) + util.getInt(header, 0x08) * 0x08
    stringTable = data[stringOffsetTable + util.getInt(header, 0x0C) * 0x08:]
    for iGr in range(nbGroup):
        offset = util.getInt(data, stringOffsetTable+0x08*iGr)
        result += [{
            "id_tag": util.xorString(stringTable[util.getInt(data, stringOffsetTable+0x08*iGr+0x04):], util.NONE_XORKEY),
            "bgm_id": getStringBgm(data, offset),
            "bgm2_id": getStringBgm(data, offset+0x08),
            "unknow_id": getStringBgm(data, offset+0x10),
            "useGenericBossMusic": util.getBool(data, offset+0x18),
            "nbBossMusic": util.getInt(data, offset+0x19),
            "bossMusics": [{
                "boss": getStringBgm(data, offset+0x20+0x10*i),
                "bgm": getStringBgm(data, offset+0x28+0x10*i)
            } for i in range(util.getInt(data, offset+0x19))],
        }]
    return result

def reverseSound(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Sound/arc/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseSound(data[0x20:])

def reverseBGM(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/SRPG/StageBgm/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseStageBGM(data[0x20:], data[:0x20])


import json
from sys import argv, stderr, exc_info
import traceback

if __name__ == "__main__":
    for arg in argv[1:]:
        try:
            s = reverseSound(arg)
            s2 = reverseBGM(arg)
            if s or s2:
                print(json.dumps(s, indent=2, ensure_ascii=False))
                print(json.dumps(s2, indent=2, ensure_ascii=False))
        except:
            t, v, tb = exc_info()
            print(f"Error: {arg}:", file=stderr)
            traceback.print_tb(tb)
            print(f"{t.__name__}: {v}", file=stderr)
            