#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.PoL import PawnsOfLokiReader

class PawnsOfLoki(ArticleContainer):
    _reader = PawnsOfLokiReader
    _linkArticleData = (r'startTime\s*=\s*([0-9TZ\-:]{20})', ['avail','start'])

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or ('Pawns of Loki ' + str(self.number))

    @property
    def number(self) -> int:
        return int(self.data['id_tag'][3:])


    def Infobox(self):
        from ..Tool.globals import WEAPON_CATEGORY
        from ..Tool.misc import maskToInt
        bonus = []
        for data in self.data['rounds']:
            if not data: continue
            mask = maskToInt(data['weapons'])
            bonus += [WEAPON_CATEGORY[mask] if mask != 0 else 'All']
        if len(bonus) == 1: bonus = bonus[0]
        else: bonus = "<br><!--\n-->".join([f"'''Round {i+1}''': {bonus[i]}" for i in range(len(bonus))])
        return super().Infobox('Pawns of Loki', {
            'startTime': self.data['avail']['start'],
            'endTime': self.data['avail']['end'],
            'bonus': bonus
        })

    def Availability(self):
        from ..Tool.misc import timeFormat
        if len(self.data['round_avails']) == 1:
            return super().Availability('[[Pawns of Loki]]', self.data['avail'], timeFormat(self.data['avail']['start'], 'Pawns of Loki (%b %Y)'))
        else:
            return super().Availability('[[Pawns of Loki]]', self.data['avail'],
                                        timeFormat(self.data['avail']['start'], 'Pawns of Loki (%b %Y)'),
                                        [(f'Round {i+1}', v) for i,v in enumerate(self.data['round_avails'])])

    def Rewards(self):
        from ..Utility.Reward import Reward
        s =  '==Rewards==\n'
        s += '===Cumulative Points rewards===\n'
        s += '{{#invoke:Reward/PawnsOfLoki|points\n'
        length = len(str(self.data['score_rewards'][-1]['score']))
        for r in self.data['score_rewards']:
            score = '{{:<{}}}'.format(length).format(r['score'])
            s += f" |{score}={Reward(r['reward'])}\n"
        s += '}}\n===Tier rewards===\n'
        s += '{{#invoke:Reward/PawnsOfLoki|tier\n'
        for r in self.data['tier_rewards']:
            s += f" |{r['tier']+1}={Reward(r['reward'])}\n"
        return s + '}}'

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += '{{Main Events Navbox}}'
        return self

PoL = PawnsOfLoki
