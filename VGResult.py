#! /usr/bin/env python3

import requests
import re

from util import DATA
import wikiUtil
from mapUtil import InOtherLanguage

from sys import argv, stderr

if __name__ == '__main__':
    SNintendo = requests.Session()
    for arg in argv[1:]:
        try:
            if re.fullmatch(r'\d+', arg):
                content = SNintendo.get(url=f'https://support.fire-emblem-heroes.com/voting_gauntlet/tournaments/{arg}?locale=en-US').content.decode()
                pageName = re.search(r'section-part-title.*?<span>(.*?)</span>', content)[1]
                page = wikiUtil.getPageContent([pageName])[pageName]
            else:
                page = wikiUtil.getPageContent([arg])[arg]
                pageName = arg
                nb = re.search(r'\|\s*tournamentNumber\s*=\s*(\d+)', page)[1]
                content = SNintendo.get(url=f'https://support.fire-emblem-heroes.com/voting_gauntlet/tournaments/{nb}?locale=en-US').content.decode()
        except:
            print(f'Failed to read Voting Gauntlet {arg}', file=stderr)
            continue
    
        scores = re.findall(r'tournaments-art-name.*?<p>((?:\d+,?)*)</p>', content)
        scores1 = scores[-8:]
        scores2 = scores[-12:-8]
        scores3 = scores[-14:-12]

        page = re.sub(r'(\|\s*scores1\s*=).*\n', '\\g<1>'+';'.join(scores1)+'\n', page)
        page = re.sub(r'(\|\s*scores2\s*=).*\n', '\\g<1>'+';'.join(scores2)+'\n', page)
        page = re.sub(r'(\|\s*scores3\s*=).*\n', '\\g<1>'+';'.join(scores3)+'\n', page)
        
        for k in DATA:
            if DATA[k] == pageName:
                tag = k
                break
        page = re.sub(r'\{\{\s*OtherLanguages.*?\}\}', InOtherLanguage(k, pageName)[:-1].replace('==In other languages==\n', ''), page, flags=re.DOTALL)
        
        wikiUtil.waitSec(10)
        wikiUtil.exportPage(pageName, page, "Bot: Voting Gauntlet result", minor=True, create=False)