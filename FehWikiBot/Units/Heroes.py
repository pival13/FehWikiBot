#! /usr/bin/env python3

from ..Tool import Container
from ..Lang import Messages
from .Reader import HeroReader

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
        from ..Lang import Quotes
        import re
        tags = re.findall(r'\$nM(PID_.+?)\|', Quotes.get('MID_'+self.data['character_file']+'_STRONGEST'))
        tags = {tag for tag in tags if tag != self.data['id_tag']}
        if len(tags) == 2:
            tags = {tag for tag in tags if self.data['id_tag'].find(tag[4:]) == -1}
        return tags.pop() if len(tags) > 0 else ''

    @property
    def isDuo(self): return self.data['extra'] and self.data['extra']['kind'] in ('Duo','Harmonized')

    @property
    def seasonal(self) -> bool:
        if not '@seasonal' in self.data:
            from ..Tool.Wiki import Wiki
            props = Wiki.cargoQuery('Units',"IFNULL(Properties__full,'')=Props",where="TagID='"+self.data['id_tag']+"' AND IFNULL(Properties__full,'') NOT LIKE '%enemy%'",limit=1)
            self.data['@seasonal'] = props.find('special') != -1 or props.find('specDisplay') != -1
        return self.data['@seasonal']

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
            if s and s.type.lower() == type.lower(): return s
            s = getter(self.data['skills']['extra2'])
            if s and s.type.lower() == type.lower(): return s
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
