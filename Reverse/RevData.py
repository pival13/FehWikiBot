#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseMsg(data):
    numberElem = util.getLong(data, 0)
    result = []
    for i in range(numberElem):
        result += [{
            "key": util.xorString(data[util.getLong(data,i*16+8):], util.MSG_XORKEY),
            "value": util.xorString(data[util.getLong(data,i*16+16):], util.MSG_XORKEY)
        }]
    return result

def parseStageBGM(data, header):
    result = []
    nbGroup = util.getLong(data, 0x08, 0x0)
    offset = util.getLong(data, 0x00)
    stringOffsetTable = util.getInt(header, 0x04) + util.getInt(header, 0x08) * 0x08
    stringTable = data[stringOffsetTable + util.getInt(header, 0x0C) * 0x08:]
    for iGr in range(nbGroup):
        result += [{
            "id_tag": util.xorString(stringTable[util.getInt(data, stringOffsetTable+0x08*iGr+0x04):], util.NONE_XORKEY),
            "bgm_id": util.getString(data, offset, util.BGM_XORKEY),
            "bgm2_id": util.getString(data, offset+0x08, util.BGM_XORKEY),
            "unknow_id": util.getString(data, offset+0x10, util.BGM_XORKEY),
            "useGenericBossMusic": util.getBool(data, offset+0x18),
            "nbBossMusic": util.getInt(data, offset+0x19),
            "bossMusics": []
        }]
        offset += 0x20
        for i in range(result[-1]["nbBossMusic"]):
            result[-1]["bossMusics"] += [{
                "boss": util.getString(data, offset, util.BGM_XORKEY),
                "bgm": util.getString(data, offset+0x08, util.BGM_XORKEY)
            }]
            offset += 0x10
    return result

def reverseMessage(name: str, type: str, lang: str="USEN"):
    """
    Args:
        tag (str): The name of the file, without the extension.
        type (str): One of "Character", "CrossLanguage", "Data", "Menu" or "Scenario"
        lang (str) ("USEN"): The langage of the message. One of:
            USEN, JPJA, EUDE, EUEN, EUFR, EUIT, EUES, TWZH, USES, USPT
    """
    fpath = util.BINLZ_ASSETS_DIR_PATH + f"/{lang}/Message/{type}/{tag}.bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseStageBGM(data[0x20:], data[:0x20])

def reverseBGM(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/SRPG/StageBgm/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseStageBGM(data[0x20:], data[:0x20])
