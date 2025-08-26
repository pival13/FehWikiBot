#! /usr/bin/env python3

__all__ = ['StoryChainChallenge','ParalogueChainChallenge']

from typing_extensions import Self
from ..Tool import ArticleContainer, globals
from .Reader.MultiMap import StoryChainChallengeReader, ParalogueChainChallengeReader

_defDiff = globals.DIFFICULTIES[0]

class BaseChainChallenge(ArticleContainer):
    _linkArticleData = None

    @classmethod
    def get(cls, key: str) -> Self | None:
        import re
        if not re.match(r'^ST_[SX][01]\d{3}[A-C]?$', key): return None
        if key[4] == '0':
            obj = super(BaseChainChallenge,cls).get(key[:8]+'A', ('stages',0,_defDiff,'id_tag')) \
               or super(BaseChainChallenge,cls).get(key[:8]+'A', ('stages',1,_defDiff,'id_tag'))
        else:
            obj = super(BaseChainChallenge,cls).get(key[:8]+'A', ('stages',2,_defDiff,'id_tag'))
        if obj is None: return None
        o = cls()
        o.data = obj.data
        o.idx = [v[_defDiff]['id_tag'] for v in o.data['stages']].index(key[:8]+'A')
        return o

    @classmethod
    def getGroup(cls, key: str, at: list=None) -> list[Self]:
        obj = super().get(key, at)
        if obj is None: return []
        os = []
        for i in range(len(obj.data['stages'])):
            o = cls()
            o.data = obj.data
            o.idx = i
            os.append(o)
        return os

    @classmethod
    def getAll(cls, key: str, at: list = None) -> list[Self]:
        objs = super().getAll(key, at)
        os = []
        for obj in objs:
            for i in range(len(obj.data['stages'])):
                o = cls()
                o.data = obj.data
                o.idx = i
                os.append(o)
        return os

    @classmethod
    def fromAssets(cls, file: str) -> list[Self]:
        objs = super().fromAssets(file)
        os = []
        for obj in objs:
            for i in range(len(obj.data['stages'])):
                o = cls()
                o.data = obj.data
                o.idx = i
                os.append(o)
        return os

    @property
    def stage(self):
        return self.data['stages'][self.idx]
    
    @property
    def id_tag(self):
        return self.stage[_defDiff]['id_tag'][:-1]

    @ArticleContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import EN
        from ..Tool.globals import ROMAN
        return super().name or (('Chain Challenge: ' + (f"Book {ROMAN[self.data['book']]}, " if self.data['book'] else '') + EN('MID_STAGE_TITLE_'+self.id_tag)) if self.data is not None else None)

    @property
    def groupName(self) -> str:
        from ..Utility.Messages import EN
        from ..Tool.globals import ROMAN
        return 'Chain Challenge: ' + (f"Book {ROMAN[self.data['book']]}, " if not self.data['is_paralogue'] else '') + EN('MID_CHAPTER_'+self.data['id_tag'])


    def settingsFromMaps(self, i) -> str:
        from ..Tool.globals import DIFFICULTIES, WARNING
        if self.id_tag[4] == '0':
            SETTINGS = {
                'cc_single_1': {
                    DIFFICULTIES[0]: {'level': 30, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 35, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                },
                'cc_single_2': {
                    DIFFICULTIES[0]: {'level': 31, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 36, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 41, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                },
                'cc_single_3': {
                    DIFFICULTIES[0]: {'level': 32, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 37, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 42, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                },
                'cc_single_4': {
                    DIFFICULTIES[0]: {'level': 33, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 38, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 43, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                },
                'cc_single_5': {
                    DIFFICULTIES[0]: {'level': 35, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                },
                'cc_single_5_c13': {
                    DIFFICULTIES[0]: {'level': 35, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 44, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                },
            }
            for tag,o in SETTINGS.items():
                ok = True
                for diff,conds in o.items():
                    if diff not in self.stage: break
                    for k,v in conds.items():
                        if self.stage[diff]['maps'][i][k] != v:
                            ok = False
                if ok:
                    return tag
        else:
            SETTINGS = {
                'cc_double_1_2': {
                    DIFFICULTIES[0]: {'level': 35, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 40, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                },
                'cc_double_3_4': {
                    DIFFICULTIES[0]: {'level': 36, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 41, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 46, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                },
                'cc_double_5': {
                    DIFFICULTIES[0]: {'level': 38, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 43, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 48, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                },
                'cc_double_6_7': {
                    DIFFICULTIES[0]: {'level': 37, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[1]: {'level': 42, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                    DIFFICULTIES[2]: {'level': 47, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 150},
                },
                'cc_double_8_9': {
                    DIFFICULTIES[0]: {'level': 38, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[1]: {'level': 43, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                    DIFFICULTIES[2]: {'level': 48, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 150},
                },
                'cc_double_10': {
                    DIFFICULTIES[0]: {'level': 40, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[1]: {'level': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                    DIFFICULTIES[2]: {'level': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 150},
                },
                'cc_double_x4': {
                    DIFFICULTIES[0]: {'level': 37, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 42, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 47, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                },
                'cc_double_x6': {
                    DIFFICULTIES[0]: {'level': 40, 'rarity': 4, 'promotion_tier': 1, 'hp_factor': 110},
                    DIFFICULTIES[1]: {'level': 45, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 120},
                    DIFFICULTIES[2]: {'level': 50, 'rarity': 5, 'promotion_tier': 1, 'hp_factor': 130},
                }
            }
            for tag,o in SETTINGS.items():
                ok = True
                for diff,conds in o.items():
                    if diff not in self.stage: break
                    for k,v in conds.items():
                        if self.stage[diff]['maps'][i][k] != v:
                            ok = False
                if ok:
                    return tag
        print(WARNING + f'Unknown derived properties for {self}, battle {i+1}')
        return ''


    def Infobox(self):
        from ..Utility.Messages import EN
        from ..Utility.Reward import Rewards
        from ..Tool.globals import ROMAN
        return super().Infobox('Battle', {
            'bannerImage': self.data['id_tag'] + '.webp',
            'stageTitle': EN('MID_STAGE_TITLE_'+self.id_tag),
            'mapName': self.name,
            'bookGroup': (f"Book {ROMAN[self.data['book']]}" if not self.data['is_paralogue'] else None),
            'mapGroup': self.groupName,
            'map': self.id_tag,
        } \
        | {'lvl'+k: o['level'] for k,o in self.stage.items()} \
        | {'rarity'+k: o['rarity'] for k,o in self.stage.items()} \
        | {'stam'+k: o['stamina'] for k,o in self.stage.items()} \
        | {
            'reward': Rewards({k: o['reward'] for k,o in self.stage.items()}),
        })
    
    def Intro(self):
        from . import StageFromMap

        s =  'A [[Chain Challenge]] based on '
        title = StageFromMap(self.stage[_defDiff]['maps'][0]['map_id']).groupName
        if self.data['is_paralogue']:
            s += f"[[Paralogue Maps#{title}|{title}]]"
        else:
            s += f"[[Story Maps#{title[title.find(', ')+2:]}|{title}]]"

        title2 = StageFromMap(self.stage[_defDiff]['maps'][-1]['map_id']).groupName
        if title2 != title:
            if self.data['is_paralogue']:
                s += f" and [[Paralogue Maps#{title2}|{title2}]]"
            else:
                s += f" and [[Story Maps#{title2[title2.find('C'):]}|{title2}]]"

        return s + '.'

    def Availability(self):
        from . import StageFromMap
        if self.data['avail']['start']:
            start = self.data['avail']['start']
        else:
            start = StageFromMap(self.data['required'][0]).data['avail']['start']
        return super().Availability('[[Chain Challenge]]', {'start':start}, isMap=True)

    def Units(self):
        from ..Tool.globals import WARNING,DIFFICULTIES
        from . import Map,StageFromMap
        s = "==Unit data=="
        for i,o in enumerate(self.stage[_defDiff]['maps']):
            stage = StageFromMap(o['map_id'])
            map = Map.get(o['map_id'])
            settings = self.settingsFromMaps(i)
            s += f"\n===Battle {i+1}===\n"
            s += '{{#invoke:UnitData|main\n'
            s += f'|battle={i+1}|derived={settings}\n'
            if stage:
                s += '|derivedMap='+stage.name
            else:
                s += '|derivedMap='
                print(WARNING + f'Unknown base map for {self}, battle {i+1}')
            s += '|derivedTabs={'+';'.join([k+'='+DIFFICULTIES[ord(v['maps'][i]['map_id'][-1])-65] for k,v in self.stage.items()])+'}\n'
            s += '|mapImage=' + map.Image(shortest=True).replace('|allyPos='+','.join(map.data['starting_pos']),'')
            s += '|allyPos=' + ','.join(map.data['starting_pos']) + '\n'
            s += '}}'
        return s

    def createArticle(self) -> Self:
        from ..Tool.globals import ROMAN
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Intro() + '\n'
        self.page += self.Availability() + '\n'
        self.page += '{{clear|right}}\n'
        self.page += self.Units() + '\n'
        self.page += '{{Chain Challenges Navbox|' + ('paralogues' if self.data['is_paralogue'] else ('book-' + ROMAN[self.data['book']].lower())) + '}}'
        return self


class StoryChainChallenge(BaseChainChallenge):
    _reader = StoryChainChallengeReader

class ParalogueChainChallenge(BaseChainChallenge):
    _reader = ParalogueChainChallengeReader

CCS = StoryChainChallenge
CCX = ParalogueChainChallenge
