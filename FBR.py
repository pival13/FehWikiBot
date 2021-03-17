#! /usr/bin/env python3

from sys import argv, stderr
from datetime import datetime
import re

import util
from reward import parseReward
from Reverse import reverseForgingBonds

from FB import COLORS, FBRewards
from wikiUtil import getPageContent

def ForgingBondsRevival(tagId: str) -> dict:
    datas = reverseForgingBonds(tagId)
    content = {}
    for data in datas:
        if data["id_tag"] == data["original_id_tag"]:
            print("Original", file=stderr)
        else:
            data["title"] = data["title"].replace(data['id_tag'], data['original_id_tag'])
            name = util.getName(data["title"])
            page = getPageContent([name])[name]

            start = data["event_avail"]["start"]
            end = util.timeDiff(data["event_avail"]["finish"])
            wikiname = util.cleanStr(f"{name} {datetime.strptime(data['event_avail']['start'], util.TIME_FORMAT).strftime('%Y%m%d')}")
            rewards = FBRewards(data).replace("First Summon Ticket I", "First Summon Ticket II").replace("==Rewards==\n", "")

            if page.find(start) == -1:
                page = re.sub(r"(\|startTime=.*)\n", f"\\1;{start}\n", page)
            if page.find(end) == -1:
                page = re.sub(r"(\|endTime=.*)\n", f"\\1;{end}\n", page)
            if page.count("(Notification)") == 1:
                page = re.sub(r"((?:\*\s*\{\{\s*HT\s*\|.*\n)+)", f"\\1* {{{{HT|{start}}}}} – {{{{HT|{end}}}}} ([[Forging Bonds Revival: {name} (Notification)|Notification]])\n", page)
            if not re.search(r"===\s*Original [rR]un\s*===", page):
                page = re.sub("(==\s*Rewards\s*==\n)", "\\1===Original run===\n", page)
            if not re.search(f"wikiname\\s*=\\s*{wikiname}", page):
                page = re.sub(r"\}\}\n(\n*==\s*Special [cC]onversations\s*==)", "}}\n===Rerun===\n"+rewards+"\\1", page)
            
            content[name] = page
    return content


if __name__ == '__main__':
    for arg in argv[1:]:
        if re.match(r'^\d+_\w+$', arg):
            a = ForgingBondsRevival(arg)
            for k in a:
                print(k, a[k])
        else:
            print("A tagId (\\d+_\\w+) is expected, but got '"+arg+"'")
