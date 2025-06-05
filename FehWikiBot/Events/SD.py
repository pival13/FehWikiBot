#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import Container, ArticleContainer
from .Reader.SD import SummonerDuelsReader, SDRReader, SDSReader, SummonerDuelsSeasonReader

class SummonerDuels(Container):
    _reader = SummonerDuelsReader

class SummonerDuelsSeason(Container):
    _reader = SummonerDuelsSeasonReader

    @classmethod
    def load(cls, name: str) -> bool:
        ret = super().load(name)
        if not ret: return False
        SummonerDuels.load(name)
        SummonerDuelsR.loadAll()
        SummonerDuelsS.loadAll()

        datas = cls._DATA.get(name)
        for data in (datas.values() if isinstance(datas, dict) else datas or []):
            data['@Classic'] = SummonerDuels.get('f'+data['id_tag'][1:]).data if SummonerDuels.get('f'+data['id_tag'][1:]) else None
            v = [o for os in SummonerDuelsR._DATA.values() for o in os.values() if data['avail']['start'] <= o['avail']['start'] < data['avail']['end']]
            data['@SDR'] = v[0] if v != [] else None
            v = [o for os in SummonerDuelsS._DATA.values() for o in os.values() if data['avail']['start'] <= o['avail']['start'] < data['avail']['end']]
            data['@SDS'] = v[0] if v != [] else None
        return True

class SummonerDuelsEvent(ArticleContainer):
    _linkArticleData = (r'startTime\s*=\s*([0-9TZ\-:]{20})', ['avail','start'])

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or (self.type + ' ' + str(self.number))

    @property
    def number(self) -> int:
        from ..Tool.Wiki import Wiki
        return int(Wiki.cargoQuery('EventsSummonerDuels', 'COUNT(DISTINCT _pageName)=Nb', where='_pageName LIKE "'+self.type+'%" AND StartTime < "'+self.data['avail']['start']+'"', limit=1))+1

    @property
    def type(self) -> str:
        return 'Summoner Duels ' + self.__class__.__name__[-1]

    @property
    def season(self) -> SummonerDuelsSeason:
        SummonerDuelsSeason.loadAll()
        o = SummonerDuelsSeason()
        o.data = [data for datas in SummonerDuelsSeason._DATA.values() for data in datas.values() if data['avail']['start'] <= self.data['avail']['start'] < data['avail']['end']][0]
        return o


    def Infobox(self):
        from ..Utility.Units import Units
        from ..Skills import CaptainSkill
        return super().Infobox(self.type, {
            'mapImage': '{{MapLayout '+self.season.data['fixed_map_id']+'}}',
            'bonusHeroes': ';'.join([Units.get(h).name for h in self.season.data['bonus_units']]),
            'captainSkills': ';'.join([CaptainSkill.get(id,'num_id').name for id in self.season.data['captain_skills']]),
            'startTime': self.data['avail']['start'],
            'endTime': self.data['avail']['end'],
        })

    def Availability(self):
        from ..Tool.globals import TIME_FORMAT
        from ..Tool.misc import timeFormat
        from datetime import datetime
        start = datetime.strptime(self.data['avail']['start'], TIME_FORMAT)
        season100 = datetime.strptime("2018-12-25T07:00:00Z", TIME_FORMAT)
        s = super().Availability('[['+self.type+']]', self.data['avail'],
                                timeFormat(self.data['avail']['start'], self.type+' Has Begun! (%b %Y)'))
        s += f"\n** It happened during [[Coliseum season {int((start - season100).days / 7) + 100}]]."
        return s

    def Rewards(self):
        from ..Utility.Reward import Reward
        s =  '==Rewards==\n'
        s += '===Rank rewards===\n'
        s += '{{#invoke:Reward/EventsSummonerDuels|rank\n'
        maxsize = len(str(self.data['rank_rewards'][-1]['rank_hi']))
        for rank in self.data['rank_rewards']:
            ranks = "{{:>{}}}~{{:>{}}}".format(maxsize, maxsize).format(rank['rank_hi'], rank['rank_lo'] if rank['rank_lo'] != -1 else "")
            s += f" |{ranks}={Reward(rank['reward'])}\n"
        s += '}}\n===Tier rewards===\n'
        s += '{{#invoke:Reward/EventsSummonerDuels|tier\n'
        for tier in self.data['tier_rewards']:
            s += f" |{tier['tier']+1}={Reward(tier['reward'])}\n"
        return s + '}}'

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += '{{Main Events Navbox}}'
        return self


class SummonerDuelsR(SummonerDuelsEvent):
    _reader = SDRReader

class SummonerDuelsS(SummonerDuelsEvent):
    _reader = SDSReader

SDR = SummonerDuelsR
SDS = SummonerDuelsS
