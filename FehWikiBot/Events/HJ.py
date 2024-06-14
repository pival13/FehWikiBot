#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.HJ import HeroesJourneyReader

class HeroesJourney(ArticleContainer):
    _reader = HeroesJourneyReader
    _linkArticleData = (r'startTime\s*=\s*([0-9TZ\-:]{20})', ['avail','start'])

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or ('Heroes Journey ' + str(self.number))

    @property
    def number(self) -> int:
        from ..Tool.Wiki import Wiki
        return int(Wiki.cargoQuery('HeroesJourney', 'COUNT(DISTINCT _pageName)=Nb', where='StartTime < "'+self.data['avail']['start']+'"', limit=1))+1


    def Infobox(self):
        from ..Utility.Messages import EN
        return super().Infobox('Heroes Journey', {
            'memento': ';'.join([EN('MID_'+id+'_Title') for id in self.data['memento_events']]),
            'startTime': self.data['avail']['start'],
            'endTime': self.data['avail']['end'],
        })

    def Availability(self):
        from ..Tool.misc import timeFormat
        return super().Availability('[[Heroes Journey]]', self.data['avail'],
                                    timeFormat(self.data['avail']['start'], 'Heroes Journey Has Begun (%b %Y)'))

    def Rewards(self):
        from ..Utility.Reward import Reward
        from ..Utility.Messages import EN
        s =  '==Rewards==\n'
        s += '===Battle rewards===\n'
        s += '{{#invoke:Reward/HeroesJourney|battle\n'
        for stage in self.data['stages']:
            if stage['base_memento'] > 0:
                stage['reward'] = [{'kind': 'Memento Point', 'count': f"{stage['base_memento']}~"}] + (stage['reward'] or [])
            s += f" |{EN('MID_JOURNEY_STAGE_LEVEL'+str(stage['difficulty']))}={Reward(stage['reward'])}\n"
        s += '}}\n===Rapport rewards===\n'
        s += '{{#invoke:Reward/HeroesJourney|rapport\n'
        for r in self.data['rewards']:
            s += f" |{r['points']}={Reward(r['reward'])}\n"
        return s + '}}'


    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += '==Memento events==\n{{Heroes Journey Memento}}\n'
        self.page += '{{Main Events Navbox}}'
        return self

HJ = HeroesJourney
