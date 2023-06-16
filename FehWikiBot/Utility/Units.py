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
        'ch00_00_Eclat_X_Avatar00':     {'id': 'EID_アバター',      'name': 'Kiran: Hero Summoner',},
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
        'ch00_49_Heith_Normal':         {'id': 'PID_ヘイズ',        'name': 'Heiðr: Innocent Goddess'},
        'ch00_51_Njord_M_Normal':       {'id': '',                  'name': 'Njörðr'}, # PID_ニョルズ
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
        if self.data['id_tag'] == 'EID_ファフニール2': return 'Fáfnir: King of Desolation (Dragon)'
        if self.data['id_tag'] == 'EID_ヴェロニカ洗脳2': return 'Veronica: Princess Beset (Dark)'
        if self.data['id_tag'] == 'EID_ヴェロニカ2': return 'Veronica: Princess Beset (Legendary)'
        if self.data['id_tag'] == 'EID_レティシア洗脳': return 'Letizia: Curse Director (Dark)'
        if self.data['id_tag'] == 'EID_ブルーノ素顔': return 'Bruno: Prince Beset (Unmasked)'
        if self.data['generic']: return Messages.EN(self.data['id_tag'])
        return Messages.EN(self.data['id_tag']) + ': ' + Messages.EN(self.data['id_tag'].replace('ID_','ID_HONOR_'))

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

    @classmethod
    def fromFace(cls, name: str): return cls.get(name, 'face_dir')

    @property
    def name(self): return Messages.EN(self.data['id_tag']) + ': ' + Messages.EN(self.data['id_tag'].replace('ID_','ID_HONOR_'))

    @property
    def duoId(self):
        from .Quotes import Quotes
        import re
        tags = re.findall(r'\$nM(PID_.+?)\|', Quotes.get('MID_'+self.data['character_file']+'_STRONGEST'))
        tags = [tag for tag in tags if tag != self.data['id_tag']]
        return tags[0] if len(tags) > 0 else ''

    @property
    def isDuo(self): return self.data['extra'] and self.data['extra']['kind'] in ('Duo','Harmonized')

    def Stats(self, level=40, rarity=5, hpmodifier=1.0):
        growth = lambda g: ((level-1) * ((g * (100+7*(rarity-3))) // 100)) // 100
        statsOrder = list(sorted(self.data['base_stats'].keys(), key=lambda k:self.data['base_stats'][k], reverse=True))
        return {
            k: int((growth(v) + self.data['base_stats'][k]-1 + (rarity if k in (statsOrder[1],statsOrder[2]) else rarity-1) // 2) * (hpmodifier if k == 'hp' else 1))
        for k,v in self.data['growth_rates'].items() }
