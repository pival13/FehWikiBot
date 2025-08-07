#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.YTS import YourTimeToShineReader as Reader

class YourTimeToShine(ArticleContainer):
    _reader = Reader
    _linkArticleData = (r'startTime\s*=\s*([0-9TZ\-:]{20})', ['avail','start'])

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or ('Your Time to Shine ' + str(self.number))

    @property
    def number(self) -> int:
        from ..Tool.Wiki import Wiki
        return int(Wiki.cargoQuery('YourTimeToShine', 'COUNT(DISTINCT _pageName)=Nb', where='StartTime < "'+self.data['avail']['start']+'"', limit=1))+1


    def Infobox(self):
        return super().Infobox('Your Time to Shine', {
            'bonusVersion': 2, # self.data[], # TODO
            'finalBattle': self.data['final_battle'][:-1],
            'start': self.data['avail']['start'],
            'end': self.data['avail']['end']
        })
    
    def Availability(self):
        return super().Availability('[[Your Time to Shine]] event', self.data['avail'])

    def Rewards(self):
        from ..Utility.Reward import Reward
        s =  '==Rewards==\n'
        s += '===Daily rewards===\n'
        s += '{{#invoke:Reward/YourTimeToShine|daily\n'
        for i,r in enumerate(self.data['daily_rewards']):
            s += f" |{i+1}={Reward(r['reward'])}\n"
        s += '}}\n===Stratum cleared===\n'
        s += '{{#invoke:Reward/YourTimeToShine|stages\n'
        for stage in self.data['stages']:
            s += f" |{stage['id_num']+1:>2}={Reward(stage['reward'])}\n"
        return s + '}}'
    
    def Battles(self):
        from ..Tool.globals import DIFFICULTIES
        from ..Stages import Map,StageFromMap
        import re

        map = Map.get(self.data['final_battle'])
        stage = StageFromMap(map.data['terrain']['map_id']).loadArticle(False)
        diff = DIFFICULTIES[self.data['stages'][-1]['difficulty']]
        units = re.search(r'UnitData.*\|\s*'+diff+r'\s*=\s*(\[.*?\])\s*(?:\||\}\})', stage.page, re.DOTALL)
        units = units[1] if units else ('[\n'+Map.Unit(Map.PLACEHOLDER_UNIT)+'\n]')

        s =  '==Final Stratum==\n'
        s += '{{#invoke:UnitData|main\n'
        s += '|derivedMap='+stage.name + '\n'
        s += '|derived=your_time_to_shine|derivedTabs={}\n'
        s += '|mapImage=' + map.Image(shortest=True).replace('|allyPos='+','.join(map.data['starting_pos']),'')
        s += '|allyPos=' + ','.join(map.data['starting_pos']) + '\n'
        s +=f'|{diff}={units}\n'
        return s + '}}'
    
    def Heroes(self):
        from datetime import datetime
        s =  '==Bonus Heroes==\n'
        version = 2# TODO
        s += f"{{{{UnitsByVersion|from={version}|to={version+1}|maxDate={datetime.now().strftime('%Y-%m-%d')}}}}}"
        return s

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += self.Battles() + '\n'
        self.page += self.Heroes() + '\n'
        self.page += '{{Main Events Navbox}}'
        return self

YTS = YourTimeToShine
