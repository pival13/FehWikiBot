#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.MultiMap import SquadAssaultReader as Reader

class SquadAssault(ArticleContainer):
    _reader = Reader
    _linkArticleData = None

    @ArticleContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import EN
        return super().name or (EN('MID_STAGE_TITLE_'+self.data['id_tag']) if self.data is not None else None)

    def Infobox(self):
        from ..Utility.Reward import Rewards
        return super().Infobox('Battle', {
            'stageTitle': self.name,
            'mapGroup': 'Squad Assault',
            'map': self.data['id_tag'],
            'lvl'+self.data['stage']['diff']: self.data['stage']['level'],
            'rarity'+self.data['stage']['diff']: self.data['stage']['rarity'],
            'stam'+self.data['stage']['diff']: self.data['stage']['stamina'],
            'reward': Rewards({self.data['stage']['diff']: self.data['stage']['reward']}),
        })
    
    def Availability(self):
        from datetime import datetime
        start = datetime.now().strftime('%Y-%m-%dT07:00:00Z')
        return super().Availability('[[Squad Assault]]', {'start':start}, isMap=True)

    def Units(self):
        from ..Tool.globals import WARNING,DIFFICULTIES
        from . import Map,StageFromMap
        s = "==Unit data=="
        for i,o in enumerate(self.data['stage']['maps']):
            stage = StageFromMap(o['map_id'])
            map = Map.get(o['map_id'])
            settings = ''
            if o['rarity'] == 5 and o['level'] == 50 and o['promotion_tier'] == 1 and o['hp_factor'] == 130:
                settings = 'squad_assault'
            else:
                print(WARNING + 'Unknown settings for '+str(self))
            s += f"\n===Battle {i+1}===\n"
            s += '{{#invoke:UnitData|main\n'
            s += f'|battle={i+1}|derived={settings}\n'
            if stage:
                s += '|derivedMap='+stage.name
            else:
                s += '|derivedMap='
                print(WARNING + f'Unknown base map for {self}, battle {i+1}')
            s += '|derivedTabs={'+self.data['stage']['diff']+'='+DIFFICULTIES[ord(o['map_id'][-1])-65]+'}\n'
            s += '|mapImage=' + map.Image(shortest=True).replace('|allyPos='+','.join(map.data['starting_pos']),'')
            s += '|allyPos=' + ','.join(map.data['starting_pos']) + '\n'
            s += '}}'
        return s

    def OtherLanguage(self):
        return super().OtherLanguage('MID_STAGE_TITLE_'+self.data['id_tag'])

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += '{{clear|right}}\n'
        self.page += self.Units() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Squad Assaults Navbox}}'
        return self

SA = SquadAssault