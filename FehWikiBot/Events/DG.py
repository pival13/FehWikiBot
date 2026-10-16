#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.DG import DivineGamesReader as Reader

class DivineGames(ArticleContainer):
    _reader = Reader
    _linkArticleData = (r'startTime\s*=\s*([0-9TZ\-:]{20})', ['avail','start'])

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or ('Divine Games ' + str(self.number))

    @property
    def number(self) -> int:
        return int(self.data['id_tag'], base=10)


    def Infobox(self):
        from ..Lang.Messages import EN
        return super().Infobox('Divine Games', {
            'bonusVersion': self.data['bonus_version'],
            'blazeArts': ';'.join(EN('MID_GRACE_SKILL_'+o['id_tag']) for o in self.data['skills'] if o['category'] == 2),
            'start': self.data['avail']['start'],
            'end': self.data['avail']['end']
        })

    def Availability(self):
        return super().Availability('[[Divine Games]] event', self.data['avail'])

    def Rewards(self):
        from ..Utility.Reward import Reward
        s =  '==Rewards==\n'
        s += '===Cumulative score===\n'
        s += '{{#invoke:Reward/DivineGames|total\n'
        for r in self.data['score_rewards']:
            s += f" |{r['score']:>5}={Reward(r['reward'])}\n"
        s += '}}\n===High score===\n'
        s += '{{#invoke:Reward/DivineGames|best\n'
        for r in self.data['best_score_rewards']:
            s += f" |{r['score']:>4}={Reward(r['reward'])}\n"
        s += '}}\n===Rank===\n'
        s += '{{#invoke:Reward/DivineGames|rank\n'
        for i,r in enumerate(self.data['rank_rewards']):
            if i == 0: rank = f"{1:>6}~{r['rank']:>6}"
            elif r['rank'] == -1: rank = f"{self.data['rank_rewards'][i-1]['rank']+1:>6}~      "
            else: rank = f"{self.data['rank_rewards'][i-1]['rank']+1:>6}~{r['rank']:>6}"
            s += f" |{rank}={Reward(r['reward'])}\n"
        return s + '}}'

    def Heroes(self):
        version = self.data['bonus_version']
        s =  '==Bonus Heroes==\n'
        s += f"{{{{UnitsByVersion|from={version}|to={version+1}|maxDate={self.data['avail']['start'][:10]}}}}}"
        return s

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += self.Heroes() + '\n'
        self.page += '{{Main Events Navbox}}'
        return self

DG = DivineGames
