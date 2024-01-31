#! /usr/bin/env python3

__all__ = ['Units', 'Heroes', 'Enemies']

from typing_extensions import Self

from .Reader.Unit import HeroReader, EnemyReader
from ..Tool import Container, ArticleContainer
from .Messages import Messages

class _UnitMeta(type):
    def __repr__(cls):
        return f"<class {cls.__name__} ({len(Enemies._DATA)+len(Heroes._DATA)} files, {len([o for os in Heroes._DATA.values() for o in os])+len([o for os in Enemies._DATA.values() for o in os])} objects)>"

class Units(metaclass=_UnitMeta):
    @staticmethod
    def get(key: str):
        if not isinstance(key, str) or len(key) == 0:
            return None
        elif key[0] == 'E':
            return Enemies.get(key)
        else:
            return Heroes.get(key)

    @staticmethod
    def fromAssets(file: str):
        return Heroes.fromAssets(file) + Enemies.fromAssets(file)
    
    @staticmethod
    def fromFace(name: str):
        return Heroes.fromFace(name) or Enemies.fromFace(name) or NPC.fromFace(name)

    @staticmethod
    def load(name: str) -> bool:
        ret1 = Heroes.load(name)
        ret2 = Enemies.load(name)
        return ret1 or ret2

class NPC:
    UNITS = {
        # 'ch00_00_Eclat_X_Normal':       {'name': 'Kiran'}, # Mini unit only
        'ch00_00_Eclat_X_Avatar00':     {'id': 'EID_アバター',      'name': 'Kiran: Hero Summoner'},
        'ch00_01_Alfons_M_Stain':       {'id': 'PID_アルフォンス',  'name': 'Alfonse: Prince of Askr (Injured)'},
        'ch00_04_Veronica_F_Stain':     {'id': 'EID_ヴェロニカ',    'name': 'Veronica: Emblian Princess (Injured)'},
        'ch00_04_Veronica2_F_Enemy':    {'id': 'EID_ヴェロニカ2',   'name': 'Veronica: Princess Beset (Legendary Dark)'},
        'ch00_05_Bruno_M_Plain':        {'id': 'PID_ブルーノ皇子',  'name': 'Bruno (Unmasked)'},
        'ch00_05_Bruno_M_PlainStain':   {'id': 'PID_ブルーノ皇子',  'name': 'Bruno (Unmasked Injured)'},
        'ch00_13_Gustaf_M_Normal':      {'id': '',                  'name': 'Gustav'},# PID_グスタフ
        'ch00_14_Henriette_F_Normal':   {'id': '',                  'name': 'Henriette'},# PID_ヘンリエッテ
        'ch00_16_Freeze_M_Normal':      {'id': 'PID_フリーズ',      'name': 'Hríd: Icy Blade (Injured)'},
        'ch00_31_Otr_M_Stain':          {'id': 'EID_オッテル',      'name': 'Ótr: Kingsbrother (Injured)'},
        'ch00_32_Fafnir2_M_Stain':      {'id': 'EID_ファフニール',  'name': 'Fáfnir: King of Desolation (Injured)'},
        'ch00_36_MysteryHood_X_Normal': {'id': '',                  'name': 'Mystery Hood'},
        'ch00_40_Elm_M_Stain':          {'id': 'EID_エルム',        'name': 'Elm: Retainer to Embla (Injured)'},
        'ch00_42_Ask_M_Disappear':      {'id': 'PID_アスク',        'name': 'Askr: God of Openness (Disappear)'},
        'ch00_43_Embla_F_Disappear':    {'id': 'EID_エンブラ',      'name': 'Embla: God of Closure (Disappear)'},
        'ch00_45_Ganglot_F_Shadow':     {'id': 'PID_ガングレト',    'name': 'Ganglöt: Death Anew (Shadow)'},
        'ch00_47_Gullveig_F_Disappear': {'id': 'EID_グルヴェイグ',   'name': 'Gullveig: Golden Seer (Disappear)'},
        'ch00_49_Heith_Normal':         {'id': 'PID_ヘイズ',        'name': 'Heiðr: Innocent Goddess'},
        'ch00_51_Njord_M_Normal':       {'id': '',                  'name': 'Njörðr'}, # PID_ニョルズ
        'ch00_56_Nidhogg_F_Normal':     {'id': '',                  'name': 'Níðhöggr'},
         # This is the tag used for non-face unit on scenarios
        'ch90_02_FighterAX_M_Normal':   {'id': '', 'name': ''}
    }

    @classmethod
    def fromFace(cls, name):
        if name not in cls.UNITS: return None
        o = cls()
        o.data = {
            'id_tag': cls.UNITS[name]['id'],
            'name': cls.UNITS[name]['name']
        }
        return o

    @property
    def name(self):
        return self.data['name'] if hasattr(self, 'data') else ''

    @property
    def isDuo(self): return False

class Enemies(ArticleContainer):
    _reader = EnemyReader
    _linkArticleData = (r'EnemyInternalID=(\d+)|InternalID=(\d+)', 'num_id')

    @classmethod
    def fromFace(cls, name: str): return cls.get(name, 'face_dir')

    @property
    def name(self):
        APPEND = {
            'EID_ファフニール2': 'Dragon', # Fáfnir
            'EID_ヴェロニカ洗脳2': 'Dark', # Veronica
            'EID_ヴェロニカ2': 'Legendary', # Veronica
            'EID_レティシア洗脳': 'Dark', # Letizia
            'EID_ブルーノ素顔': 'Unmasked', # Bruno
            'EID_ヘイズ敵': 'Serpent', # Heiðr
        }
        s = super().name
        if s or self.data is None: return s
        if self.data['generic']:
            s = Messages.EN(self.data['id_tag'])
        else:
            s = Messages.EN(self.data['id_tag']) + ': ' + Messages.EN(self.data['id_tag'].replace('ID_','ID_HONOR_'))
        if self.data['id_tag'] in APPEND:
            s += ' (' + APPEND[self.data['id_tag']] + ')'
        return s

    @property
    def isDuo(self): return False

    def Stats(self, level=40, rarity=5, hpmodifier=1.0):
        growth = lambda g: ((level-1) * ((g * (100+7*(rarity-3))) // 100)) // 100
        statsOrder = list(sorted(self.data['base_stats'].keys(), key=lambda k:self.data['base_stats'][k], reverse=True))
        return {
            k: int((growth(self.data['growth_rates'][k]) + self.data['base_stats'][k]-1 + (rarity if k in (statsOrder[1],statsOrder[2]) else rarity-1) // 2) * (hpmodifier if k == 'hp' else 1))
        for k in self.data['base_stats'].items() }

class Heroes(Container):
    _reader = HeroReader

    def __repr__(self) -> str:
        return '<' + type(self).__name__ + ' "' + str(self.name) + '"' + (f" ({self.data['id_tag']})" if self.data else '') + '>'

    @classmethod
    def fromFace(cls, name: str): return cls.get(name, 'face_dir')

    @property
    def shortName(self): return Messages.EN(self.data['id_tag'])

    @property
    def name(self): return Messages.EN(self.data['id_tag']) + ': ' + Messages.EN(self.data['id_tag'].replace('ID_','ID_HONOR_'))

    @property
    def duoId(self):
        from .Quotes import Quotes
        import re
        tags = re.findall(r'\$nM(PID_.+?)\|', Quotes.get('MID_'+self.data['character_file']+'_STRONGEST'))
        tags = {tag for tag in tags if tag != self.data['id_tag']}
        if len(tags) == 2:
            tags = {tag for tag in tags if self.data['id_tag'].find(tag[4:]) == -1}
        return tags.pop() if len(tags) > 0 else ''

    @property
    def isDuo(self): return self.data['extra'] and self.data['extra']['kind'] in ('Duo','Harmonized')

    def Stats(self, level=40, rarity=5, hpmodifier=1.0):
        growth = lambda g: ((level-1) * ((g * (100+7*(rarity-3))) // 100)) // 100
        statsOrder = list(sorted(self.data['base_stats'].keys(), key=lambda k:self.data['base_stats'][k], reverse=True))
        return {
            k: int((growth(v) + self.data['base_stats'][k]-1 + (rarity if k in (statsOrder[1],statsOrder[2]) else rarity-1) // 2) * (hpmodifier if k == 'hp' else 1))
        for k,v in self.data['growth_rates'].items() }

    def Skills(self, rarity=5, latest=False):
        o = {
            'weapon': self.Skill('weapon', rarity, latest),
            'assist': self.Skill('assist', rarity, latest),
            'special': self.Skill('special', rarity, latest),
            'a': self.Skill('a', rarity, latest),
            'b': self.Skill('b', rarity, latest),
            'c': self.Skill('c', rarity, latest),
            'attuned': self.Skill('attuned', rarity, latest),
        }
        return {k: v.data['id_tag'] if v else None for k,v in o.items()}

    def Skill(self, type: str, rarity=5, latest=False):
        from ..Skills import Skills
        def getter(a, b=None):
            s1 = [v for v in a[:rarity] if v is not None]
            if b:
                s2 = [v for v in b[:rarity] if v is not None]
                if len(s2) > 0 and s2[-1] not in s1:
                    return Skills.get(s2[-1])
            return Skills.get(s1[-1] if len(s1) > 0 else None)

        if latest:
            s = getter(self.data['skills']['extra1'])
            if s and s.type.lower() == type: return s
            s = getter(self.data['skills']['extra2'])
            if s and s.type.lower() == type: return s
        match type.lower():
            case 'weapon':
                s = getter(self.data['skills']['summon_weapon'], self.data['skills']['weapon'])
                if not latest or not s or len(s.data['@refines']) == 0: return s
                if len(s.data['@refines']) in (1,5):
                    return Skills.get(s.data['@refines'][-1])
                else:
                    return Skills.get(s.data['@refines'][0])
            case 'assist':
                return getter(self.data['skills']['summon_assist'], self.data['skills']['assist'])
            case 'special':
                return getter(self.data['skills']['summon_special'], self.data['skills']['special'])
            case 'a':
                return getter(self.data['skills']['summon_a'], self.data['skills']['a'])
            case 'b':
                return getter(self.data['skills']['summon_b'], self.data['skills']['b'])
            case 'c':
                return getter(self.data['skills']['summon_c'], self.data['skills']['c'])
            case 'attuned':
                return getter(self.data['skills']['summon_attuned'])
            case 'seal': return None
