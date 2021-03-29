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

def reverseMessage(tag: str, type: str, lang: str="USEN"):
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
