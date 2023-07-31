#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.TD import TacticsDrillsReader

class TacticsDrills(ArticleContainer):
    _reader = TacticsDrillsReader
    _linkArticleData = (r'baseMap=(P[ABC]\d+)', 'id_tag')

    @ArticleContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import EN
        return super().name or EN('MID_STAGE_' + self.data['id_tag']) if self.data is not None else None

    @property
    def map(self):
        from .Terrain import Map
        if self.data is None: return None
        if not hasattr(self, '_map'):
            self._map = Map.get(self.data['id_tag'])
        return self._map

    def Infobox(self):
        from ..Utility.Messages import EN
        from ..Utility.Reward import Rewards
        return super().Infobox('Battle', {
            'bannerImage': 'Banner_Tactics_Drills_' + self.data['type'].replace(' ','_') + '.png',
            'stageTitle': EN('MID_STAGE_TITLE_'+self.data['id_tag']),
            'stageName': EN('MID_STAGE_'+self.data['id_tag']),
            'stageEpithet': '',
            'mapGroup': 'Tactics Drills: ' + self.data['type'],
            'mapMode': 'Reinforcement Map' if self.data['map']['reinforcements'] else None,
            'mapImage': self.map.Image(),
            'stam'+self.data['map']['diff']: self.data['map']['stamina'],
            'reward': Rewards({self.data['map']['diff']: self.data['map']['reward']}),
            'winReq': 'Phases to win: ' + str(self.data['map']['max_turn']*2-1 + self.data['map']['last_enemy_phase']),
            'BGM': 'bgm_map_FE14_t.ogg',
        })
    
    def Availability(self):
        from datetime import datetime
        from FehWikiBot.Tool.globals import TIME_FORMAT
        notif = 'New Tactics Drills! (' + datetime.strptime(self.data['avail']['start'], TIME_FORMAT).strftime('%b %d, %Y').replace(' 0', ' ') + ')'
        return super().Availability('[[Tactics Drills]]', self.data['avail'], notif, isMap=True)

    def Text(self):
        from ..Utility.Scenario import Scenario
        scenar = Scenario.get(self.data['id_tag']).get('MID_MAP_FIELD_TEXT')
        s =  '==Text==\n'
        if scenar:
            s += '{{TDText|' + scenar.text('USEN').replace('\\n','<br>') + '|' + scenar.text('JPJA').replace('\\n','<br>') + '}}'
        else:
            s += '{{TDText||}}'
        return s

    def UnitData(self):
        from .Terrain import Map
        return Map.UnitData({self.data['map']['diff']: self.map})

    def Solution(self):
        import re
        from ..Utility.Units import Units

        s =  '==Solution==\n'
        s += '{{#invoke:TacticsDrillsSolution|main\n'
        s += '|baseMap=' + self.map.baseMap
        if self.map.needBackground():
            s += '|backdrop=' + self.map.background
        s += '\n|wallStyle=' + self.map.wallStyle
        
        walls = re.findall(r'(\w{2})=\{\{[^}]+hp=(.)', self.map.Image(False,True))
        s += '|wall={' + ';'.join([wall[0]+'='+wall[1] for wall in walls]) + '}\n'
        
        heroes = []
        enemies = [[]]
        for unit in self.map.data['units']:
            if unit['playable']:
                heroes.append(Units.get(unit['unit']).name)
            elif unit['spawn_turns'] > 0 and len(enemies) < unit['spawn_turns']+1:
                enemies.insert(unit['spawn_turns'], [Units.get(unit['unit']).name])
            else:
                enemies[max(unit['spawn_turns'],0)].append(Units.get(unit['unit']).name)
        for i, hero in enumerate(heroes):
            if ':' in hero and all([name == hero or name.find(hero[:hero.find(':')]) == -1 for name in heroes]):
                heroes[i] = hero[:hero.index(':')]
        for i, turn in enumerate(enemies):
            for j, enemy in enumerate(turn):
                if ':' in enemy and all([name == enemy or name.find(enemy[:enemy.find(':')]) == -1 for t in enemies for name in t]):
                    enemies[i][j] = enemy[:enemy.index(':')]
        s += '|turn1=[\n<!--'
        for h in heroes: s += '{unit=' + h + ';move;attack};\n'
        for e in enemies[0]: s += '{enemy=' + e + ';move=};\n'
        for i,es in enumerate(enemies[1:]):
            s += ']\n|turn' + str(i+2) + '=[\n'
            for e in es: s += '{enemy=' + e + ';move=};\n'
        s =  s[:-1] + '-->\n]\n'
        s += '}}'
        return s

    def OtherLanguage(self):
        return super().OtherLanguage('MID_STAGE_' + self.data['id_tag'])

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Text() + '\n'
        self.page += self.UnitData() + '\n'
        self.page += self.Solution() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Tactics Drills Navbox}}'
        return self

TD = TacticsDrills