#! /usr/bin/env python3

from typing_extensions import Self
from .SpecialMapContainer import SpecialMapContainer
from ..PersonalData import JSON_ASSETS_DIR_PATH

class EventMap(SpecialMapContainer):
    _linkArticleData = (r'baseMap=(V\d+)', 'id_tag')
    _jsonFile = JSON_ASSETS_DIR_PATH + 'EventMaps.json'
    _JSON = None

    @classmethod
    def fromAssets(cls, file: str) -> list[Self]:
        return [o for o in super().fromAssets(file) if o.data['id_tag'][0] == 'V']

    @property
    def jsonData(self) -> dict | None:
        if EventMap._JSON is None:
            import json
            from os.path import exists
            EventMap._JSON = json.load(open(self._jsonFile, 'r', encoding='utf8')) if exists(self._jsonFile) else {}
        return self._JSON[self.data['id_tag']] if self.data and self.data['id_tag'] in self._JSON else None

    @SpecialMapContainer.name.getter
    def name(self) -> str:
        from ..Lang import EN
        return super().name or (EN('MID_STAGE_'+self.data['id_tag']) + ': ' + self.event)

    @property
    def event(self) -> str:
        from ..Lang import EN
        s = EN('MID_STAGE_HONOR_'+self.data['id_tag'])
        if s == 'Daily':
            from datetime import datetime
            from ..Tool.globals import TIME_FORMAT
            return s + f" ({datetime.strptime(self.data['avail']['start'], TIME_FORMAT).strftime('%b %Y')})"
        elif s == 'Feh\'s Summer':
            return s + f" ({self.data['avail']['start'][:4]})"
        else:
            return s

    def export(self, summary: str, *, minor=False, create=True):
        from ..Tool.Wiki import Wiki
        from ..Tool.misc import waitSec
        if self.page == '': return
        if self.jsonData.get('baseMap'):
            waitSec(10)
            Wiki.exportPage('File:Map '+self.data['id_tag']+'.png', '#REDIRECT [[File:Map ' + self.jsonData['baseMap'] + '.webp]]', summary, minor=minor, create=create)
        waitSec(10)
        Wiki.exportPage(self.name, self.page, summary, minor=minor, create=create)


    def Infobox(self):
        from ..Lang import EN
        from ..Utility.Reward import Rewards
        from ..Others.Sound import BGM
        from .Terrain import Map
        map = Map.get(self.jsonData.get('baseMap', self.data['id_tag'])+'A')
        if map is None:
            map = Map.create(self.data['id_tag']).Image()
        else:
            map = map.Image().replace(self.jsonData['baseMap'], self.data['id_tag'])
        o =  {
            'bannerImage': 'Banner ' + self.data['banner_id'] + '.webp',
            'stageTitle': EN('MID_STAGE_TITLE_'+self.data['id_tag']),
            'stageName': EN('MID_STAGE_'+self.data['id_tag']),
            'stageEpithet': EN('MID_STAGE_HONOR_'+self.data['id_tag']),
            'mapGroup': self.event,
            'mapMode': None,
            'mapImage': map
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
        if self.data['maps'][0]['min_turn']:
            o['mapMode'] = 'Defensive Battle Map'
            reqs.append(f"Turns to defend: {self.data['maps'][0]['min_turn']}")
        if self.data['maps'][0]['reinforcements']:
            o['mapMode'] = 'Reinforcement Map'
        o['winReq'] = '<br>'.join(reqs)

        return super().Infobox('Battle', o)

    def Availability(self):
        if self.event[-1] == ')':
            return super().Availability(f"map is part of the '''{self.event.replace(' (',' Celebration (')}''' event and", self.data['avail'], isMap=True)
        else:
            return super().Availability(f"map is part of the '''{self.event} Celebration''' event and", self.data['avail'], isMap=True)
    
    def UnitData(self):
        from .Terrain import Map
        from ..Units import Heroes

        s = "==Unit data==\n"
        s += "{{#invoke:UnitData|main|globalai="
        if self.data['maps'][-1]['reinforcements']:
            s += "\n|mapImage="

        for idiff,map in enumerate(self.data['maps']):
            s += '\n|' + map['diff'] + '=[\n'
            for unit in self.jsonData.get('units', []):
                o = Map.PLACEHOLDER_UNIT.copy()
                o['pos'] = unit['pos']
                o['rarity'] = map['rarity']
                o['true_lv'] = map['level']
                u = Heroes.fromName(unit['name'])
                if u:
                    o['unit'] = u.data['id_tag']
                    o['stats'] = u.Stats(map['level'], map['rarity'])
                    # Weapon
                    if   map['rarity'] == 3 and map['level'] == 5:
                        defWep = u.Skill('weapon', 1)
                    elif map['rarity'] == 3 and map['level'] == 15:
                        defWep = u.Skill('weapon', 2)
                    else:
                        defWep = u.Skill('weapon', map['rarity'])
                    if u.seasonal or (u.data.get('extra') or {}).get('kind') == 'Attuned':
                        wep = u.Skill('weapon')
                        if wep and wep.data['id_tag'][-1] == '＋':
                            wep = u.Skill('weapon', 4)
                    else:
                        wep = defWep
                    o['weapon'] = wep.data['id_tag'] if wep else ''
                    if defWep and wep:
                        o['stats']['atk'] = max(0, o['stats']['atk'] + defWep.data['might'] - wep.data['might'])
                    else:
                        o['stats']['atk'] = '<!--' + o['stats']['atk'] + '-->'
                    #Assist
                    if u.data['refresher']:
                        o['assist'] = u.Skill('assist', 4)
                    elif u.data['weapon'] == 15: # Colorless staff
                        if map['rarity'] == 3 and map['level'] == 5:
                            o['assist'] = u.Skill('assist', 1)
                        elif map['rarity'] == 3 and map['level'] == 15:
                            o['assist'] = u.Skill('assist', 2)
                s += Map.Unit(o) + '\n'
            if self.data['maps'][idiff]['reinforcements']:
                s += Map.Unit(Map.PLACEHOLDER_UNIT | {'rarity': map['rarity'], 'true_lv': map['level'], 'nb_spawn': 1})
            s += ']'
        return s.replace('=-;','=;') + '\n}}'
    
    def Story(self):
        from ..Lang import Scenario
        s = Scenario.Conversation(self.data['id_tag'], 'MID_SCENARIO_MAP_BEGIN')
        if s == '': return ''
        return '==Story==\n' + s + '\n' + Scenario.StoryNavbar(self.data['id_tag']) + '\n'

    def Trivia(self):
        from ..Tool.globals import TODO
        from ..Tool.Wiki import Wiki
        s =  '==Trivia==\n'
        if self.jsonData.get('baseMap'):
            if self.jsonData['baseMap'][:1] == 'X':
                o = Wiki.cargoQuery('Maps','_pageName=Page,StageTitle',where="Map='"+self.jsonData['baseMap']+"'", limit=1)
                s += f"* This map is based on [[{o['Page']}|{o['StageTitle']}]]."
            elif self.jsonData['baseMap'][:1] == 'S':
                o = Wiki.cargoQuery('Maps','_pageName=Page,StageTitle,BookGroup',where="Map='"+self.jsonData['baseMap']+"'", limit=1)
                s += f"* This map is based on [[{o['Page']}|{o['StageTitle'].replace(': Part ','-')}]] of [[{o['BookGroup']}]]."
            elif self.jsonData['baseMap'][:1] in ('L','T'):
                os = Wiki.cargoQuery('Maps,MapUnits,Units', 'Maps._pageName=Page,Maps.MapGroup=Group,Units._pageName=Unit', where="Map='"+self.jsonData['baseMap']+"' AND IFNULL(Units.Properties__full,'') NOT LIKE '%generic%'", join='Maps._pageName=MapUnits._pageName,MapUnits.Unit=Units.WikiName', group='Units._pageName', order='MapUnits._ID')
                s += f"* This map is based on the [[{os[0]['Page']}|{os[0]['Group']}]] against "+' and '.join(['{{Ut|'+o['Unit']+'}}' for o in os])+'.'
            else:
                print(TODO + f'Unsupported "baseMap"="{self.jsonData["baseMap"]}"')
                s += '* '
        return s
    
    def OtherLanguage(self):
        return super().OtherLanguage('MID_STAGE_'+self.data['id_tag'], 'MID_STAGE_HONOR_'+self.data['id_tag'])

    def createArticle(self) -> Self:
        if self.data is None: return self
        if self.jsonData is None:
            from ..Tool.globals import TODO
            print(TODO + f'Missing event map "{self.id_tag}"')
            return self
        try:
            self.page =  self.Infobox() + '\n'
            self.page += self.Availability() + '\n'
            self.page += self.UnitData() + '\n'
            self.page += self.Story()
            self.page += self.Trivia() + '\n'
            self.page += self.OtherLanguage() + '\n'
            self.page += '{{Special Maps Navbox}}\n[[Category:Event maps]]'
        except Exception as e:
            from ..Tool.globals import ERROR
            print(ERROR + str(e))
            self.page = ''
        return self
