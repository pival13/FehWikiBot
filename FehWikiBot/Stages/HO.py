#! /usr/bin/env python3

from typing_extensions import Self
from .Reader.HO import HOReader
from ..Tool import ArticleContainer

class HeroicOrdeals(ArticleContainer):
    _reader = HOReader
    _linkArticleData = (r'baseMap=H0*(\d+)', 'id_tag')

    @classmethod
    def load(cls, name: str) -> bool:
        from ..Utility.Sound import BGM
        from ..Utility.Units import Heroes
        if not super().load(name): return False
        for o in cls._DATA[name].values():
            origin = Heroes.get(int(o['id_tag']), 'num_id').data['origin']
            o['@BGM'] = BGM.HO[origin]
        return True

    @classmethod
    def fromUnique(cls) -> Self:
        return cls.fromAssets('00_first')

    @ArticleContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import EN
        if hasattr(self, '_name'): return self._name
        if self.data is None: return None
        return 'Heroic Ordeals: ' + self.unit.name + '\'s Trial'

    @property
    def unit(self):
        from ..Utility.Units import Heroes
        if self.data is None: return None
        if not hasattr(self, '_unit'):
            self._unit = Heroes.get(int(self.data['id_tag']), 'num_id')
        return self._unit

    @property
    def map(self):
        from .Terrain import Map
        if self.data is None: return None
        if not hasattr(self, '_map'):
            self._map = Map.get(f"H{int(self.data['id_tag']):04}")
        return self._map

    def Infobox(self):
        from ..Utility.Messages import EN
        from ..Utility.Sound import Sound
        from ..Tool.globals import MOVE_TYPE
        LVL = {'Normal':30,'Hard':35,'Lunatic':40}
        RARITY = {'Normal':4,'Hard':5,'Lunatic':5}
        return super().Infobox('Battle', {
            'bannerImage': '',
            'stageTitle': EN('MID_STAGE_SELECT_HERO_TRIAL'),
            'stageName': EN(self.unit.data['id_tag']),
            'stageEpithet': '',
            'mapGroup': 'Heroic Ordeals',
            'mapImage': self.map.Image(),
            'lvl'+self.data['diff']: LVL[self.data['diff']],
            'rarity'+self.data['diff']: RARITY[self.data['diff']],
            'stam'+self.data['diff']: 0,
            'reward': f"{{\n  {self.data['diff']}={{kind=Dragonflower ({MOVE_TYPE[self.unit.data['move']][0]});count={self.data['dragonflowers']}}};\n}}",
            'winReq': "The ordeal challenger must<br>defeat at least 2 foes.<br>All allies must survive.<br>Turns to win: 20",
            'BGM': Sound.get(self.data['@BGM']['bgm_map']).file,
            'BGM2': Sound.get(self.data['@BGM']['bgm_battle']).file
        })

    def Availability(self):
        from ..Tool import Wiki
        from datetime import datetime
        start = Wiki.cargoQuery('Units', 'ReleaseDate', f"IntID={self.unit.data['num_id']}", limit=1) or datetime.now().strftime('%Y-%m-%d')
        return super().Availability('map', {'start': start+'T07:00:00Z'}, isMap=True)

    def UnitData(self):
        from .Terrain import Map
        return Map.UnitData({self.data['diff']: self.map})

    def OtherLanguage(self):
        return super().OtherLanguage('MID_STAGE_SELECT_HERO_TRIAL', self.unit.data['id_tag'], False)

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  '{{HeroPage Tabs/Heroic Ordeals}}'
        self.page += self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.UnitData() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Heroic Ordeals Navbox}}'
        return self

HO = HeroicOrdeals