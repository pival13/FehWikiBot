#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer, Container
from .Reader.MS import MjolnirsStrikeReader, MechanismReader


class MjolnirsStrikeMechanism(Container):
    _reader = MechanismReader

    @property
    def name(self) -> str:
        from ..Utility.Messages import EN
        return EN('MID_MF_' + self.data['id_tag'][:-1])

MSMechanism = MjolnirsStrikeMechanism
Mechanism = MjolnirsStrikeMechanism

class MjolnirsStrike(ArticleContainer):
    _reader = MjolnirsStrikeReader
    _linkArticleData = (r'startTime\s*=\s*([0-9TZ\-:]{20})', ['shield_avail','start'])

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or 'Mjölnir\'s Strike ' + str(self.number)

    @property
    def number(self) -> int:
        from ..Tool.Wiki import Wiki
        return int(Wiki.cargoQuery('MjolnirsStrike', 'COUNT(DISTINCT _pageName)=Nb', where='StartTime < "'+self.data['avail']['start']+'"', limit=1))+1


    def Infobox(self):
        from ..Utility.Units import Heroes
        from ..Tool.misc import cleanStr
        return super().Infobox('Mjolnirs Strike', {
            'image': f"Mjolnirs Strike {cleanStr(Heroes.get(self.data['boss_id']).name)}.jpg",
            'mapImage': '{{MapLayout '+self.data['map_id']+'}}',
            'startTime': self.data['shield_avail']['start'],
            'endTime': self.data['counter_avail']['end'],
            'leader': Heroes.get(self.data['boss_id']).name,
            'bonusStructure': Mechanism.get(self.data['bonus_structure']).name,
            'askrLV':'','strikeLV':'','askrScore':'','strikeScore':'','timesStronger':'',
            'season': self.data['season']
        })

    def Availability(self):
        from ..Tool.misc import timeFormat
        avail = self.data['avail']
        avail['start'] = self.data['shield_avail']['start']
        return super().Availability('[[Mjölnir\'s Strike]]', avail, timeFormat(self.data['avail']['start'], 'Mjölnir\'s Strike Battles Begin! (%b %d, %Y)'),
                                    [('Shield Phase', self.data['shield_avail']),('Counter Phase', self.data['counter_avail'])])

    def Rewards(self):
        from ..Utility.Reward import Reward
        s =  '==Rewards==\n'
        s += '===Tier rewards===\n'
        s += '{{#invoke:Reward/MjolnirsStrike|tier\n'
        for r in self.data['rewards']:
            if r['kind'] != 2: continue
            s += f" |{r['tier_hi']+1}={Reward(r['reward'])}\n"
        s += '}}\n===Askr LV. rewards===\n'
        s += '{{#invoke:Reward/MjolnirsStrike|askrLevel\n'
        for r in self.data['rewards']:
            if r['kind'] != 1: continue
            s += f" |{r['tier_hi']+1}={Reward(r['reward'])}\n"
        return s + '}}'

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += '==Final results==\n{{MjolnirStrikeResults\n'
        for i in range(21):
            self.page += f'|askr{i+1}=|strike{i+1}=\n'
        self.page += '}}\n'
        self.page += '{{Main Events Navbox}}'
        return self

    @classmethod
    def incompleteArticles(cls):
        from ..Tool.Wiki import Wiki
        return [cls.fromWiki(s) for s in Wiki.cargoQuery('MjolnirsStrike', where='AskrScore IS NULL')]

    def update(self) -> Self:
        import re
        import json
        import requests

        if self.page.find('askrScore=\n') == -1: return self

        content = requests.get(url=f'https://support.fire-emblem-heroes.com/mjolnir/terms/m_{self.number:04}').content.decode()
        lvs = re.findall(r'レベル (\d+)', content)
        timeStronger = re.search(r'\d+時間中、(\d+)時間', content)[1]
        situations = json.loads(re.search(r'data-situations="([^"]*)"', content)[1].replace('&quot;','"'))

        self.page = re.sub(r'\|askrLV=.*?\n',f'|askrLV={lvs[0]}\n', self.page)
        self.page = re.sub(r'\|strikeLV=.*?\n',f'|strikeLV={lvs[1]}\n', self.page)
        self.page = re.sub(r'\|timesStronger=.*?\n', f'|timesStronger={timeStronger}\n', self.page)

        score = [0,0]
        for i, situation in enumerate(situations):
            score = [score[0]+situation['ally_score'], score[1]+situation['enemy_score']]
            self.page = re.sub(f'\\|askr{i+1}=.*?\\|strike{i+1}=.*?\n', f"|askr{i+1}={score[0]}|strike{i+1}={score[1]}\n", self.page)

        self.page = re.sub(r'\|askrScore=.*?\n', f'|askrScore={score[0]}\n', self.page)
        self.page = re.sub(r'\|strikeScore=.*?\n', f'|strikeScore={score[1]}\n', self.page)

        return self

HoF = MjolnirsStrike
