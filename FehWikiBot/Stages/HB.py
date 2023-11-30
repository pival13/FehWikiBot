#! /usr/bin/env python3

from typing_extensions import Self
from .SpecialMapContainer import SpecialMapContainer

__all__ = ['HeroBattle','HB',
           'GrandHeroBattle','GHB',
           'BoundHeroBattle','BHB',
           'LegendaryHeroBattle','DoubleLegendaryHeroBattle','LHB',
           'MythicHeroBattle','DoubleMythicHeroBattle','MHB',
           'LegendaryMythicHeroBattle','LimitedHeroBattle']

class HeroBattle(SpecialMapContainer):
    _linkArticleData = (r'baseMap=([TL]\d+)', 'id_tag')

    def _toChildClass(self):
        if self.data is None: return None
        elif self.data['id_tag'][0] not in 'ILT': return None
        match self.category:
            case 'Limited Hero Battle':
                o = LimitedHeroBattle()
            case 'Grand Hero Battle':
                o = GrandHeroBattle()
            case 'Bound Hero Battle':
                o = BoundHeroBattle()
            case 'Legendary Hero Battle':
                o = LegendaryHeroBattle()
            case 'Mythic Hero Battle':
                o = MythicHeroBattle()
            case 'Double Legendary Hero Battle':
                o = DoubleLegendaryHeroBattle()
            case 'Double Mythic Hero Battle':
                o = DoubleMythicHeroBattle()
            case 'Legendary & Mythic Hero Battle':
                o = LegendaryMythicHeroBattle()
            case _:
                return self
        o.data = self.data
        o.page = self.page
        if hasattr(self,'_name'): o._name = self._name
        return o

    @classmethod
    def get(cls, key: str, at: list = None):
        o = super().get(key, at)
        o = o._toChildClass() if o else None
        return o if cls == HeroBattle or cls == type(o) else None

    @classmethod
    def getAll(cls, key: str, at: list = None):
        os = [o._toChildClass() for o in super().getAll(key, at)]
        return [o for o in os if cls == HeroBattle or cls == type(o)]

    @classmethod
    def fromAssets(cls, file: str):
        os = [o._toChildClass() for o in super().fromAssets(file)]
        return [o for o in os if (cls == HeroBattle and o is not None and not type(o) == LimitedHeroBattle) or type(o) == cls]

    @classmethod
    def fromWiki(cls, name: str):
        o = super().fromWiki(name)
        o = o._toChildClass() if o else None
        return o if cls == HeroBattle or cls == type(o) else None

    @classmethod
    def upcomingRevivals(cls) -> list[Self]:
        from datetime import datetime
        from ..Tool.globals import TIME_FORMAT
        super().get('')
        now = datetime.now().strftime(TIME_FORMAT)
        os = []
        for tag,datas in cls._DATA.items():
            for k in datas:
                if datas[k]['avail']['start'] <= now: continue
                o = cls.get(k)
                if o: os.append(o)
        return os


    @SpecialMapContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import EN
        s = super().name
        if s is None and self.data is not None:
            s = EN('MID_STAGE_'+self.data['id_tag']) + ': ' + EN('MID_STAGE_HONOR_'+self.data['id_tag'])
            if s.find('Hero Battle') == -1:
                s += ' (map)'
            elif s[1:4] == ' & ' and s[5] == ':':
                if s[0] == self.heroes[0].shortName[0]:
                    s = self.heroes[0].shortName + ' & ' + self.heroes[1].shortName + s[5:]
                else:
                    s = self.heroes[1].shortName + ' & ' + self.heroes[0].shortName + s[5:]
        return s

    @property
    def heroes(self):
        from ..Utility.Scenario import Scenario
        from ..Utility.Units import Heroes
        import re
        tags = re.findall(r'ch\d{2}_\d{2}_\w+', Scenario(self.id_tag, 'MID_SCENARIO_MAP_BEGIN').texts['USEN'])
        heroes = []
        for t in tags:
            if t not in heroes:
                heroes.append(t)
        return [Heroes.fromFace(h) for h in heroes]

    @property
    def maps(self):
        from .Terrain import Map
        o = {o['diff']: Map.create(o['base_id'], len(o['enemies'])) for o in self.data['maps']}
        return o

    @property
    def category(self):
        if self.data['id_tag'][0] == 'I': return 'Limited Hero Battle'
        heroes = self.heroes
        if len(heroes) == 1:
            if self.data['id_tag'][0] == 'T': return 'Grand Hero Battle'
            elif (heroes[0].data['extra'] or {}).get('kind') == 'Legendary': return 'Legendary Hero Battle'
            elif (heroes[0].data['extra'] or {}).get('kind') == 'Mythic': return 'Mythic Hero Battle'
        elif len(heroes) == 2:
            if self.data['id_tag'][0] == 'T': return 'Bound Hero Battle'
            elif (heroes[0].data['extra'] or {}).get('kind') == 'Legendary' and (heroes[1].data['extra'] or {}).get('kind') == 'Legendary':
                return 'Double Legendary Hero Battle'
            elif (heroes[0].data['extra'] or {}).get('kind') == 'Mythic' and (heroes[1].data['extra'] or {}).get('kind') == 'Mythic':
                return 'Double Mythic Hero Battle'
            elif ((heroes[0].data['extra'] or {}).get('kind') == 'Legendary' and (heroes[1].data['extra'] or {}).get('kind') == 'Mythic') or \
                 ((heroes[0].data['extra'] or {}).get('kind') == 'Mythic' and (heroes[1].data['extra'] or {}).get('kind') == 'Legendary'):
                return 'Legendary & Mythic Hero Battle'
        from ..Tool.globals import TODO
        print(TODO + '')
        return 'Unknown Hero Battle'


    def Infobox(self):
        from ..Utility.Messages import EN
        from ..Utility.Reward import Rewards
        from ..Utility.Sound import BGM
        o =  {
            'bannerImage': 'Banner ' + self.data['id_tag'] + '.webp',
            'stageTitle': EN('MID_STAGE_TITLE_'+self.data['id_tag']),
            'stageName': EN('MID_STAGE_'+self.data['id_tag']),
            'stageEpithet': EN('MID_STAGE_HONOR_'+self.data['id_tag']),
            'mapGroup': self.category,
            'mapMode': None,
            'mapImage': list(self.maps.values())[0].Image()
        }
        o |= {'lvl'+o['diff']:    o['level'] for o in self.data['maps']}
        o |= {'rarity'+o['diff']: o['rarity'] for o in self.data['maps']}
        o |= {'stam'+o['diff']:   o['stamina'] for o in self.data['maps']}
        o |= {
            'reward': Rewards({o['diff']: o['reward'] for o in self.data['maps']}),
            'winReq': None,
        }
        o |= {f"BGM{(i+1) if i != 0 else ''}":bgm for i,bgm in enumerate(BGM.bgms(self.data['maps'][0]['base_id'][:-1]))}

        reqs = []
        if self.data['maps'][0]['survive']: reqs.append('All allies must survive.')
        if self.data['maps'][0]['lights_blessing'] == 0: reqs.append('Cannot use {{It|Light\'s Blessing}}.')
        if self.data['maps'][0]['max_turn']:
            o['mapMode'] = 'Turn Limit Map'
            reqs.append(f"Turns to win: {self.data['maps'][0]['max_turn']}")
        if self.data['maps'][0]['max_turn']:
            o['mapMode'] = 'Defensive Battle Map'
            reqs.append(f"Turns to defend: {self.data['maps'][0]['min_turn']}")
        if self.data['maps'][0]['reinforcements']:
            o['mapMode'] = 'Reinforcement Map'
        o['winReq'] = '<br>'.join(reqs)

        return super().Infobox('Battle', o)

    def Availability(self, notif=''):
        return super().Availability('[['+self.category+']]', self.data['avail'], notif, isMap=True)

    def Units(self) -> str:
        from .Terrain import Map
        HP_MOD = {'Normal':1.2, 'Hard':1.3, 'Lunatic':1.4, 'Infernal':1.5, 'Abyssal':1.65}
        maps = self.maps
        for data in self.data['maps']:
            for i,hero in enumerate(self.heroes):
                maps[data['diff']].data['units'][i]['unit'] = hero.data['id_tag']
                maps[data['diff']].data['units'][i]['stats'] = hero.Stats(data['level'], data['rarity'])
                if data['diff'] == 'Abyssal':
                    for k in Map.PLACEHOLDER_UNIT['stats']:
                        maps[data['diff']].data['units'][i]['stats'][k] += 4
                maps[data['diff']].data['units'][i]['stats']['hp'] = int(HP_MOD[data['diff']] * maps[data['diff']].data['units'][i]['stats']['hp'])
            if data['reinforcements']:
                maps[data['diff']].data['units'].append(Map.PLACEHOLDER_UNIT | {'nb_spawn':1})
            for unit in maps[data['diff']].data['units']:
                unit['rarity'] = data['rarity']
                unit['true_lv'] = data['level']
                if unit['unit'] == '': unit['init_cooldown'] = -1
        return Map.UnitData(maps).replace('|allyPos=|enemyPos=','').replace('=-','=')

    def Story(self) -> str:
        from ..Utility.Scenario import Scenario
        s =  '==Story==\n'
        s += Scenario.Story(self.data['id_tag']) + '\n'
        s += Scenario.StoryNavbar(self.data['id_tag'])
        return s

    def OtherLanguage(self):
        return super().OtherLanguage('MID_STAGE_'+self.data['id_tag'], 'MID_STAGE_HONOR_'+self.data['id_tag'])

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Units() + '\n'
        self.page += self.Story() + '\n'
        self.page += '==Trivia==\n*\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Special Maps Navbox}}'
        return self
    
    def update(self) -> Self:
        from ..Tool.misc import timeDiff
        from datetime import datetime
        import re

        if self.data is None or self.page == '': return self
        if self.page.find(self.data['avail']['start']) != -1:
            self.page = ''
            return self

        avail = super().Availability('', self.data['avail'], '', isMap=True)[50:]
        if self.data['avail']['end'] > timeDiff(self.data['avail']['start'], 86400*4-1): # Ignore Celebratory revival
            time = datetime(year=int(self.data['avail']['start'][:4]), month=int(self.data['avail']['start'][5:7]), day=1).strftime('%b %Y')
            if   type(self) is GrandHeroBattle:
                avail = avail.replace('notification=', f'notification=Grand Hero Battle Revival - {self.heroes[0].name} (Notification)')
                if self.page.find('=Grand Hero Battle Revival') != -1:
                    avail = avail.replace('(Notification)', f'({time}) (Notification)')
            elif type(self) is BoundHeroBattle:
                avail = avail.replace('notification=',f'notification=Bound Hero Battle Revival: {self.heroes[0].shortName} & {self.heroes[1].shortName} (Notification)')
                if self.page.find('=Bound Hero Battle Revival') != -1:
                    avail = avail.replace('(Notification)', f'({time}) (Notification)')
            else:
                month = int(self.data['avail']['start'][5:7])
                day = int(self.data['avail']['start'][8:10])
                if day > 25 or day < 3:
                    if day < 3:
                        time = datetime(year=int(self.data['avail']['start'][:4]), month=month-1, day=1).strftime('%b %Y')
                    if month % 3 != 1:
                        avail = avail.replace('notification=', f'notification=Legendary Hero Battle! ({time}) (Notification)')
                    else:
                        avail = avail.replace('notification=', f'notification=Mythic Hero Battle! ({time}) (Notification)')
                else:
                    avail = avail.replace('notification=', f'notification=Legendary & Mythic Hero Remix ({time}) (Notification)')

        self.page = re.sub(r"(\{\{MapDates[^\n]*)(\s*?\n)*(==\s*Unit [Dd]ata\s*==)", '\\1\n'+avail+'\n\\3', self.page)
        return self


class GrandHeroBattle(HeroBattle):
    def Availability(self):
        return super().Availability('Grand Hero Battle - ' + self.heroes[0].name)

class BoundHeroBattle(HeroBattle):
    def Availability(self):
        return super().Availability('Bound Hero Battle: ' + self.heroes[0].shortName + ' & ' + self.heroes[1].shortName)

class LegendaryHeroBattle(HeroBattle):
    def Availability(self):
        from datetime import datetime
        from FehWikiBot.Tool.globals import TIME_FORMAT
        return super().Availability('Legendary Hero Batle! (' + datetime.strptime(self.data['avail']['start'], TIME_FORMAT).strftime('%b %Y') + ')')

class MythicHeroBattle(HeroBattle):
    def Availability(self):
        from datetime import datetime
        from FehWikiBot.Tool.globals import TIME_FORMAT
        return super().Availability('Mythic Hero Batle! (' + datetime.strptime(self.data['avail']['start'], TIME_FORMAT).strftime('%b %Y') + ')')

class LegendaryMythicHeroBattle(BoundHeroBattle):
    def Availability(self):
        from datetime import datetime
        from FehWikiBot.Tool.globals import TIME_FORMAT
        return super().Availability('Legendary & Mythic Hero Battle! (' + datetime.strptime(self.data['avail']['start'], TIME_FORMAT).strftime('%b %Y') + ')')

class DoubleLegendaryHeroBattle(LegendaryHeroBattle): pass
class DoubleMythicHeroBattle(MythicHeroBattle): pass

HB = HeroBattle
GHB = GrandHeroBattle
BHB = BoundHeroBattle
LHB = LegendaryHeroBattle
MHB = MythicHeroBattle


class LimitedHeroBattle(HeroBattle):
    @property
    def name(self) -> str:
        return HeroBattle.get(self.data['banner_id']).name

    def createArticle(self):
        return self

    def update(self) -> Self:
        import re
        from ..Utility.Reward import Rewards
        from ..Tool.misc import timeFormat

        if self.data is None or self.page == '': return self

        if not re.search(r'==\s*Limited Hero Battle\s*==', self.page):
            self.page = re.sub(r'(==\s*Unit [dD]ata\s*==(\n.*)*?)\n==', '\\1\n==Limited Hero Battle==\n{{Limited Hero Battle/header}}\n|}\n==', self.page)
        if not re.search(r'map\s*=\s*'+self.data['id_tag'], self.page):
            s =  '{{Limited Hero Battle\n'
            s += '|map=' + self.data['id_tag']
            s += '|entry=' + ','.join(map(str,self.data['maps'][0]['origins']))
            s += '|refresher=' + str(self.data['maps'][0]['max_refreshers']) + '\n'
            s += '|reward=' + Rewards({o['diff']: o['reward'] for o in self.data['maps']}) + '\n'
            s += '|start=' + self.data['avail']['start'] + '|end=' + self.data['avail']['end'] + '\n'
            s += '|notification=Limited Hero Battles! (' + timeFormat(self.data['avail']['start']) + ') (Notification)\n'
            s += '}}'
            self.page = re.sub(r'(==\s*Limited Hero Battle\s*==(\n.*)*?)\n\|\}', '\\1\n'+s+'\n|}', self.page)

        return self

