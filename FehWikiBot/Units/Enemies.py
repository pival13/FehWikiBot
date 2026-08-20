#! /usr/bin/env python3

from ..Tool import ArticleContainer
from .Reader import EnemyReader
from ..Lang import Messages

class Enemies(ArticleContainer):
    _reader = EnemyReader
    _linkArticleData = (r'EnemyInternalID=(\d+)|InternalID=(\d+)', 'num_id')

    @classmethod
    def fromFace(cls, name: str): return cls.get(name, 'face_dir')

    @property
    def shortName(self): return Messages.EN(self.data['id_tag'])

    @property
    def name(self):
        APPEND = {
            'EID_ファフニール2': 'Dragon', # Fáfnir
            'EID_ヴェロニカ洗脳2': 'Dark', # Veronica
            'EID_ヴェロニカ2': 'Legendary', # Veronica
            'EID_レティシア洗脳': 'Dark', # Letizia
            'EID_ブルーノ素顔': 'Unmasked', # Bruno
            'EID_ヘイズ敵': 'Serpent', # Heiðr
            'EID_バルドル2': 'Weakened', # Baldr
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


    def Infobox(self):
        from datetime import date
        from ..Lang import Messages
        from ..Tool.globals import WEAPON_TYPE, MOVE_TYPE
        return super().Infobox('Enemy', {
            'Name': Messages.EN(self.data['id_tag']),
            'Title': Messages.EN(self.data['id_tag'].replace('ID_','ID_HONOR_')),
            'Origin': 'Fire Emblem Heroes',
            'Gender': self.data['face_dir'][ self.data['face_dir'].find('_',8)+1 : self.data['face_dir'].rfind('_') ],
            'WeaponType': WEAPON_TYPE[self.data['weapon']],
            'MoveType': MOVE_TYPE[self.data['move']],
            'actorEN': Messages.EN(self.data['id_tag'].replace('ID_','ID_VOICE_')),
            'actorJP': Messages.JA(self.data['id_tag'].replace('ID_','ID_VOICE_')),
            'artist': Messages.JA(self.data['id_tag'].replace('ID_','ID_ILLUST_')),
            'additionDate': date.today().strftime('%Y-%m-%d'),
            'Properties': '',
            'description': Messages.EN(self.data['id_tag'].replace('ID_','ID_H_')).replace('\n',' '),
            'TagID': self.data['id_tag'][4:],
            'InternalID': self.data['num_id'],
        })

    def StatsTable(self):
        s =  '{{Stats Page/Enemy\n'
        s += ''.join([f"|Lv1{k.upper()}={v+1:<3}" for k,v in self.data['base_stats'].items()]) + '\n'
        s += ''.join([f"| GR{k.upper()}={v:<3}" for k,v in self.data['growth_rates'].items()]) + '\n'
        return s + '}}'
    
    def SkillsTable(self):
        from ..Skills.Skills import Skills
        s =  '==Skills==\n'
        s += '===Weapons===\n'
        s += '{{Weapons Table'
        if self.data['skills']['weapon']:
            s += '/enemy\n|weapon4=' + Skills.get(self.data['skills']['weapon']).name + '\n'
        s += '}}\n'
        s += '===Assists===\n'
        s += '{{Assists Table'
        if self.data['skills']['assist1']:
            s += '/enemy\n|assist1=' + Skills.get(self.data['skills']['assist1']).name + '\n'
            if self.data['skills']['assist2']:
                s += '|assist2=' + Skills.get(self.data['skills']['assist2']).name + '\n'
        s += '}}\n'
        s += '===Specials===\n'
        s += '{{Specials Table'
        if self.data['skills']['special']:
            s += '/enemy\n|special1=' + Skills.get(self.data['skills']['special']).name + '\n'
        s += '}}\n'
        s += '===Passives===\n'
        s += '{{Passives Table}}'
        return s

    def OtherLanguage(self):
        return super().OtherLanguage(self.data['id_tag'], self.data['id_tag'][:4]+'HONOR'+self.data['id_tag'][3:])

    def createArticle(self):
        from .Subpages import QuotesPage, MiscPage
        if self.data is None: return self
        
        self.page =  '{{#invoke:NameAbout|main|Name=' + self.shortName + '}}{{HeroPage Tabs}}\n'
        self.page += self.Infobox() + '\n'
        self.page += self.StatsTable() + '\n'
        self.page += self.SkillsTable() + '\n'
        self.page += '{{Enemies Navbox}}'

        self.misc = MiscPage(self)
        self.quotes = QuotesPage(self)

        return self

    def export(self, summary: str, *, minor=False, create=True):
        from ..Tool.Wiki import Wiki
        from ..Tool.misc import waitSec
        if self.page == '': return
        waitSec(10)
        Wiki.exportPage(self.name, self.page, summary, minor=minor, create=create)
        if hasattr(self, 'quotes') and self.quotes != '':
            waitSec(10)
            Wiki.exportPage(self.name+'/Quotes', self.quotes, summary, minor=minor, create=create)
        if hasattr(self, 'misc') and self.misc != '':
            waitSec(10)
            Wiki.exportPage(self.name+'/Misc', self.misc, summary, minor=minor, create=create)
