#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.UW import UnitedWarfrontReader

class UnitedWarfront(ArticleContainer):
    _reader = UnitedWarfrontReader
    _linkArticleData = (r'startTime\s*=\s*([0-9TZ\-:]{20})', ['avail','start'])

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or 'United Warfront ' + str(self.number)

    @property
    def number(self) -> int:
        from ..Tool.Wiki import Wiki
        return int(Wiki.cargoQuery('UnitedWarfront', 'COUNT(DISTINCT _pageName)=Nb', where='StartTime < "'+self.data['avail']['start']+'"', limit=1))+1


    def Infobox(self):
        return super().Infobox('United Warfront', {
            'image': 'CoopTrial chara '+self.data['id_tag']+'.webp',
            'maps': ','.join([o['map_id'] for o in self.data['stages']]),
            'start': self.data['avail']['start'],
            'end': self.data['avail']['end']
        })

    def Availability(self):
        from ..Tool.misc import timeFormat
        return super().Availability('[[United Warfront]]', self.data['avail'],
                                    timeFormat(self.data['avail']['start'], 'United Warfront (%b %Y)'))

    def Rewards(self):
        from ..Utility.Reward import Reward
        s =  '==Rewards==\n'
        s += '{{#invoke:Reward/UnitedWarfront|battles\n'
        j = 0
        for i,stage in enumerate(self.data['stages']):
            s += f' |{i+1}={{\n'
            for k in stage['maps'].keys():
                s += f"  {k}={Reward(self.data['stage_rewards'][j]['reward'])};\n"
                j += 1
            s += ' }\n'
        s += f" |clear={Reward(self.data['clear_rewards'][0]['reward'])}\n"
        s += '}}'
        return s

    def Battles(self):
        import re
        from ..Stages.HB import HeroBattle
        from ..Stages.Terrain import Map
        s = '==Battles==\n'
        for i,stage in enumerate(self.data['stages']):
            o = HeroBattle.get(stage['map_id']).loadArticle(False)
            ally = re.search(r'allyPos\s*=\s*([\w\s,]*?)\n?', o.page)
            ally = ally[1] if ally else ''
            image = re.search(r'UnitData.*mapImage\s*=\s*(\{\{.+?\}\})\s*\|\s*(?:Normal|Hard|Lunatic|Infernal|Abyssal)', o.page, re.DOTALL)
            image = image[1] if image else Map.get(stage['map_id']).Image(shortest=True)
            derivedTabs = []
            units = {}
            for j,diff in enumerate(stage['maps'].keys()):
                if not self.data['_obj2'][j]['altered_data']:
                    derivedTabs.append(diff)
                else:
                    units[diff] = re.search(r'UnitData.*\|\s*'+diff+r'\s*=\s*(\[.*?\])\s*(?:\||\}\})', o.page, re.DOTALL)
                    units[diff] = units[diff][1] if units[diff] else ('[\n'+Map.Unit(Map.PLACEHOLDER_UNIT)+'\n]')
            s += f'===Battle {i+1}===\n'
            s +=  '{{#invoke:UnitData|main\n'
            s += f'|battle={i+1}|derived=united_warfront\n'
            s += f'|derivedMap={o.name}'
            s +=  '|derivedTabs={' + ';'.join([k+'='+k for k in derivedTabs]) + '}\n'
            s += f'|mapImage={image}|allyPos={ally}\n'
            for diff,units in units.items():
                s += f'|{diff}={units}\n'
            s +=  '}}\n'
        return s[:-1]

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += self.Battles() + '\n'
        self.page += '{{Main Events Navbox}}'
        return self

UW = UnitedWarfront
