#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.BW import BindingWorldsReader

class BindingWorlds(ArticleContainer):
    _reader = BindingWorldsReader
    _linkArticleData = (r'startTime\s*=\s*([0-9TZ\-:]{20})', ['avail','start'])

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or ('Binding Worlds ' + str(self.number))

    @property
    def number(self) -> int:
        from ..Tool.Wiki import Wiki
        return int(Wiki.cargoQuery('BindingWorlds', 'COUNT(DISTINCT _pageName)=Nb', where='StartTime < "'+self.data['avail']['start']+'"', limit=1))+1


    def Infobox(self):
        return super().Infobox('Binding Worlds', {
            'number': self.number,
            'startTime': self.data['avail']['start'],
            'endTime': self.data['avail']['end'],
        })

    def Availability(self):
        from ..Tool.misc import timeFormat
        return super().Availability('[[Binding Worlds]]', self.data['avail'],
                                    timeFormat(self.data['avail']['start'], 'Binding Worlds (%b %Y)'))

    def Rewards(self):
        from ..Utility.Reward import Reward
        s =  '==Rewards==\n'
        s += '===Daily rewards===\n'
        s += '{{#invoke:Reward/BindingWorlds|daily\n'
        for i,r in enumerate(self.data['daily_rewards']):
            s += f" |{i+1}={Reward(r['reward'])}\n"
        s += '}}\n===Enclosure cleared===\n'
        s += '{{#invoke:Reward/BindingWorlds|stages\n'
        for stage in self.data['stages']:
            s += f" |{stage['id_tag']:>2}={Reward(stage['reward'])}\n"
        return s + '}}'


    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += '{{Main Events Navbox}}'
        return self
