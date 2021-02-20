#! /usr/bin/env python3

import requests
import re
import json

import util
import wikiUtil

from sys import argv

if __name__ == '__main__':
    SNintendo = requests.Session()
    for arg in argv[1:]:
        if not re.match(r'\d+', arg): continue
        nb = int(arg)

        content = SNintendo.get(url=f'https://support.fire-emblem-heroes.com/mjolnir/terms/m_{nb:04}').content.decode()
        lvs = re.findall(r'レベル (\d+)', content)
        timeStronger = re.search(r'\d+時間中、(\d+)時間', content)[1]
        situations = json.loads(re.search(r'data-situations="([^"]*)"', content)[1].replace('&quot;','"'))

        s = "{{MjolnirStrikeResults"
        allyScore = 0
        enemyScore = 0
        for i, situation in enumerate(situations):
            allyScore += situation['ally_score']
            enemyScore += situation['enemy_score']
            s += f"\n|askr{i+1}={allyScore}|strike{i+1}={enemyScore}"
        s += "\n}}"


        page = wikiUtil.getPageContent([f"Mjölnir's Strike {nb}"])[f"Mjölnir's Strike {nb}"]
        page = re.sub(r'\|askrLV=.*\n', f'|askrLV={int(lvs[0])}\n', page)
        page = re.sub(r'\|strikeLV=.*\n', f'|strikeLV={int(lvs[1])}\n', page)
        page = re.sub(r'\|askrScore=.*\n', f'|askrScore={allyScore}\n', page)
        page = re.sub(r'\|strikeScore=.*\n', f'|strikeScore={enemyScore}\n', page)
        page = re.sub(r'\|timesStronger=.*\n', f'|timesStronger={timeStronger}\n', page)
        page = re.sub(r'\{\{MjolnirStrikeResults[^}]*\}\}', s, page)

        wikiUtil.waitSec(10)
        print(wikiUtil.exportPage(f"Mjölnir's Strike {nb}", page, "Bot: Mjölnir's Strike result", True))