#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.Story import StageScenarioReader

class StoryContainer(ArticleContainer):
    _DATA = {}
    _reader = StageScenarioReader

    def __init_subclass__(cls):
        d = cls._DATA
        super().__init_subclass__()
        cls._DATA = d

    @classmethod
    def fromWiki(cls, name: str) -> Self | None:
        from re import search
        o = super().fromWiki(name)
        if o is None: return None
        m = search(r'baseMap=(\w{2}\d{3})', o.page)
        if m:
            o2 = super().get(m[1])
            if o2:
                o.data = o2.data
                o.name = name
        return o

    @ArticleContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import EN
        return super().name or EN('MID_STAGE_'+self.id_tag) if self.data is not None else None

    @property
    def map(self):
        return self.data['maps'][self.idx]
    
    @property
    def id_tag(self):
        return self.map['Normal']['id_tag'][:-1]

    @property
    def groupName(self) -> str:
        from ..Utility.Messages import EN
        return (EN('MID_CHAPTER_TITLE_'+self.data['id_tag']) + ': ' + EN('MID_CHAPTER_'+self.data['id_tag'])) if self.data is not None else None

    def Infobox(self):
        from ..Tool.globals import ROMAN
        from ..Utility.Messages import EN
        from ..Utility.Reward import Rewards
        from ..Utility.Sound import BGM
        from .Terrain import Map
        o =  {
            'bannerImage': self.data['id_tag'] + (' C' if self.idx == 4 else '')  + '.webp',
            'stageTitle': EN('MID_STAGE_TITLE_'+self.id_tag),
            'stageName': EN('MID_STAGE_'+self.id_tag),
            'stageEpithet': '',
            'bookGroup': ('Book ' + ROMAN[self.data['book']]) if self.data['book'] > 0 else None,
            'mapGroup': EN('MID_CHAPTER_TITLE_'+self.data['id_tag']) + ': ' + EN('MID_CHAPTER_'+self.data['id_tag']),
            'mapMode': None,
            'mapImage': Map.get(self.map['Normal']['base_id']).Image()
        }
        o |= {'lvl'+k: o['level'] for k,o in self.map.items()}
        o |= {'rarity'+k: o['rarity'] for k,o in self.map.items()}
        o |= {'stam'+k: o['stamina'] for k,o in self.map.items()}
        o |= {
            'reward': Rewards({k: o['reward'] for k,o in self.map.items()}),
            'winReq': None,
        }
        o |= {f"BGM{(i+1) if i != 0 else ''}":bgm for i,bgm in enumerate(BGM.bgms(self.map['Normal']['base_id'][:-1]))}
        
        reqs = []
        if self.map['Normal']['survive']: reqs.append('All allies must survive.')
        if self.map['Normal']['lights_blessing'] == 0: reqs.append('Cannot use {{It|Light\'s Blessing}}.')
        if self.map['Normal']['max_turn']:
            o['mapMode'] = 'Turn Limit Map'
            reqs.append(f"Turns to win: {self.map['Normal']['max_turn']}")
        if self.map['Normal']['max_turn']:
            o['mapMode'] = 'Defensive Battle Map'
            reqs.append(f"Turns to defend: {self.map['Normal']['min_turn']}")
        if self.map['Normal']['reinforcements']:
            o['mapMode'] = 'Reinforcement Map'
        o['winReq'] = '<br>'.join(reqs)

        return super().Infobox('Battle', o)

    def Units(self):
        from .Terrain import Map
        return Map.UnitData({k: Map.get(o['base_id']) for k,o in self.map.items()})

    def OtherLanguage(self):
        return super().OtherLanguage('MID_STAGE_'+self.id_tag)