#!/usr/bin/env python3

import json
from os.path import isfile

import REutil as util

def parseOccupation(data):
    return {}

def reverseGrandConquests(tag: str):
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Occupation/Data/" + tag + ".bin.lz"
    if isfile(fpath):
        data = util.decompress(fpath)
        return parseOccupation(data)


from sys import argv

if __name__ == "__main__":
    for arg in argv[1:]:
        s = reverseGrandConquests(arg)
        if s:
            print(json.dumps(s, indent=2, ensure_ascii=False))