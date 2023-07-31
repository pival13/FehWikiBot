#! /usr/bin/env python3

from typing_extensions import Self
from .Reader import SkillReader, SealReader, RefineryReader, SealForgeReader
from ..Tool.ArticleContainer import Container, JsonContainer, ArticleContainer

class SacredSealsForge(Container):
    _reader = SealForgeReader
    
    @property
    def skill(self): return Skills.get(self.data['id_tag'])

class SacredSeals(Container):
    _reader = SealReader

    @classmethod
    def load(cls, name: str) -> bool:
        ret = super().load(name)
        if not ret: return False
        datas = cls._DATA.get(name)
        for data in (datas.values() if isinstance(datas, dict) else datas or []):
            data['creatable'] = (data['prev_id'] or SacredSealsForge.get(data['id_tag'])) is not None
        return True

    @property
    def skill(self): return Skills.get(self.data['id_tag'])

class WeaponRefinery(Container):
    _reader = RefineryReader
    _key = 'refine_id'

def _createChildClass(obj):
    from .Weapon import Weapon
    from .Assist import Assist
    from .Special import Special
    from .Passive import Passive
    if obj is None: return None
    elif obj.type == 'Weapon': o = Weapon()
    elif obj.type == 'Assist': o = Assist()
    elif obj.type == 'Special': o = Special()
    elif obj.type in ('A','B','C','Seal'): o = Passive()
    else: o = Skills()
    o.data = obj.data
    o.page = obj.page
    return o

class Skills(JsonContainer, ArticleContainer):
    _DATA = {}
    _reader = SkillReader
    _linkArticleData = (r'tagid\s*=\s*(\w+)','id_tag')

    def __init_subclass__(cls):
        d = cls._DATA
        super().__init_subclass__()
        cls._DATA = d

    @classmethod
    def load(cls, name: str) -> bool:
        ret = super().load(name)
        if not ret: return False
        datas = cls._DATA.get(name)
        for data in (datas.values() if isinstance(datas, dict) else datas or []):
            data['@SealForge'] = SacredSeals.get(data['id_tag']).data if SacredSeals.get(data['id_tag']) else None
            data['@Refinery'] = WeaponRefinery.get(data['id_tag'], 'refine_id').data if WeaponRefinery.get(data['id_tag'], 'refine_id') else None
            data['@refines'] = [o.data['refine_id'] for o in WeaponRefinery.getAll(data['id_tag'], 'base_id')]
        return True

    @classmethod
    def get(cls, key: str, at: list = None) -> Self | None:
        return _createChildClass(super().get(key, at))

    @classmethod
    def getAll(cls, key: str, at: list = None):
        os = super().getAll(key, at)
        for i in range(len(os)):
            os[i] = _createChildClass(os[i])
        return os

    @classmethod
    def getGroup(cls, group) -> list[Self]:
        base = cls.get(group)
        if base and base.type in ('Weapon','Assist','Special'):
            return [base]
        elif base and base.type in ('Duo','Refine'):
            return []
        elif base is None:
            for i in range(5,-1,-1):
                base = cls.get(group+str(i))
                if base: break
        if base is None: return []
        #TODO handle passive skills

    @classmethod
    def fromAssets(cls, file: str, type: list = None) -> list[Self]:
        tmp = super().fromAssets(file)
        os = []
        if isinstance(type, str): type = [type]
        for i in range(len(tmp)):
            if type is not None and tmp[i].type not in type: continue
            elif tmp[i].type == 'Weapon' and tmp[i].data['@Refinery'] is not None: continue
            os.append(_createChildClass(tmp[i]))
        return os

    @classmethod
    def fromWiki(cls, name: str):
        o = _createChildClass(super().fromWiki(name))
        if o is not None: o.name = name
        return o


    @staticmethod
    def description(key):
        from ..Utility.Messages import EN
        import re
        s = EN(key).replace('$a','').replace('\n\n','<br><br>')
        s = re.sub(r'(?:\n|<br>)((?:Effect:\s*)?【[^】]+】)\n', '<br>\\1<br>', s)
        return s.replace('\n',' ')


    @ArticleContainer.name.getter
    def name(self):
        from ..Utility.Messages import EN
        APPEND = {
            'SID_ファルシオン': 'Mystery', # Falchion
            'SID_ファルシオン外伝': 'Gaiden', # Falchion
            'SID_ファルシオン覚醒': 'Awakening', # Falchion
            'SID_ナーガ': 'weapon', # Naga
            'SID_レーヴァテイン': 'weapon', # Laevatein
            'SID_アトラース': 'weapon', # Atlas
            'SID_ギンヌンガガプ': 'weapon', # Ginnungagap
            'SID_セイズ': 'weapon', # Seiðr
            'SID_ヘイズ': 'weapon', # Heiðr
            'SID_クワシル': 'weapon', # Kvasir
            'SID_グルヴェイグ': 'weapon', # Gullveig
            'SID_ミステルトィン': 'sword', # Missiltainn
            'SID_魔書ミステルトィン': 'tome', # Missiltainn
        }
        s = super().name
        if s or self.data is None: return s
        s = EN(self.data['name_id'])
        if self.data['id_tag'] in APPEND:
            s += ' (' + APPEND[self.data['id_tag']] + ')'
        return s
    
    @property
    def articleName(self):
        import re
        from ..Utility.Messages import EN
        s = self.name
        if hasattr(self,'_datas'):
            s = re.sub(r'\s+\d+$','', EN(self._datas[0]['name_id']).replace('/',' '))
        return s

    @property
    def type(self):
        return self.data['type']

    @property
    def exclusive(self):
        return self.data['exclusive']

    def loadArticle(self, canCreate=True, revision=0) -> Self:
        from ..Tool.Wiki import Wiki
        s =  Wiki.getPageContent(self.articleName, revision)
        if s is not None:
            self.page = s
        elif canCreate:
            self.createArticle()
        else:
            self.page = ''
        return self

    def update(self) -> Self:
        return self

    def export(self, summary: str, *, minor=False, create=True):
        from ..Tool.Wiki import Wiki
        from ..Tool.misc import waitSec
        if self.page == '': return
        waitSec(10)
        Wiki.exportPage(self.articleName, self.page, summary, minor, create)

    def Availability(self):
        if self.type == 'Seal': return ''
        s  = '==List of owners==\n'
        s += '{{Skill Hero List}}\n'
        if not self.data['exclusive'] and not self.data['enemy_only']:
            s += '==Availability==\n'
            s += '{{PassiveFocusList}}\n'
            s += '{{PassiveDistributionList}}\n'
            s += '{{PassiveCombatManualList}}\n'
        return s[:-1]
    
    def OtherLanguage(self):
        return super().OtherLanguage(self.data['name_id'])