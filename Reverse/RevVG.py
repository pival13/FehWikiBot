#!/usr/bin/env python3

import json

import REutil as util

def parseTournament(data):
    return {}

def reverseVotingGauntlet():
    fpath = util.BINLZ_ASSETS_DIR_PATH + "/Common/Tournament/04_spring01.bin.lz"
    data = util.decompress(fpath)
    return parseTournament(data)


if __name__ == "__main__":
    s = reverseVotingGauntlet()
    if s:
        print(json.dumps(s, indent=2, ensure_ascii=False))