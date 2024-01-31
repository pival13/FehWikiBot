#! /usr/bin/env python3

from ..Tool import ArticleContainer
from .Reader.SS import SeersSnareReader

class SeersSnare(ArticleContainer):
    _reader = SeersSnareReader
    _linkArticleData = (r'StartTime', ('avail','start'))

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or 'Seer\'s Snare ' + str(self.number)

    @property
    def number(self) -> int:
        self.get('')
        return sorted(o['avail']['start'] for os in self._DATA.values() for o in os.values()).index(self.data['avail']['start']) + 1

    def Infobox(self):
        from ..Utility.Units import Units
        return super().Infobox('Seers Snare', {
            'bosses': ';'.join([Units.get(o['unit']).name for o in self.data['boss_battle'][1:]] + [Units.get(self.data['boss_battle'][0]['unit']).name]),
            'startTime': self.data['avail']['start'],
            'endTime': self.data['avail']['end']
        })

    def Availability(self):
        from datetime import datetime
        from FehWikiBot.Tool.globals import TIME_FORMAT
        notif = 'Seer\'s Snare (' + datetime.strptime(self.data['avail']['start'], TIME_FORMAT).strftime('%b %Y') + ')'
        return super().Availability('[[Seer\'s Snare]]', self.data['avail'], notif)

    def Rewards(self):
        from ..Utility.Reward import Reward
        s =  '==Rewards==\n'
        s += '===Daily rewards===\n{{#invoke:Reward/SeersSnare|daily\n'
        for i,r in enumerate(self.data['daily_rewards']):
            s += f" |{i+1}={Reward(r['reward'])}\n"
        s += '}}\n===Rift cleared===\n{{#invoke:Reward/SeersSnare|stages\n'
        for i,r in enumerate(self.data['stages']['stages']):
            s += f" |{i+1:>2} ={Reward(r['reward'])}\n"
            if r['advanced_reward']:
                s += f" |{i+1:>2}+={Reward(r['advanced_reward'])}\n"
        s += '}}'
        return s
    
    def UnitData(self):
        from ..Stages.Terrain import Map
        from ..Utility.Units import Units
        def weaponToSeal(unit: Units):
            from ..Tool.globals import WEAPON_MASK
            if (1 << unit.data['weapon']) & WEAPON_MASK['Red']: return 'SID_時を彷徨う者・赤'
            if (1 << unit.data['weapon']) & WEAPON_MASK['Blue']: return 'SID_時を彷徨う者・青'
            if (1 << unit.data['weapon']) & WEAPON_MASK['Green']: return 'SID_時を彷徨う者・緑'
            return 'SID_時を彷徨う者・無'

        s =  '==Timeless Rift==\n'
        prev = 0
        for o in sorted(self.data['boss_battle'],key=lambda o:o['stage'])[:-1]:
            data = self.data['stages']['stages'][o['stage']]
            map1 = Map.create(o['intermediate'][:-1])
            map2 = Map.create(o['advanced'][:-1])
            for map,idx,count in ((map1,1,3), (map2,2,4)):
                unit = Units.get(o['unit'])
                map.data['units']  = [Map.PLACEHOLDER_UNIT | unit.Skills(latest=True) | {
                    'unit': o['unit'],
                    'init_cooldown': -1,
                    'rarity': 5,
                    'true_lv': data['boss_level'][idx],
                    'stats': unit.Stats(data['boss_level'][idx], 5),#, data['hp_factor'][idx] / 100)
                    'seal': weaponToSeal(unit)
                }] + [Map.PLACEHOLDER_UNIT | {
                    'init_cooldown': -1,
                    'rarity': 5,
                    'true_lv': data['level'][idx],
                } for _ in range(count)]

            s += f"===Rifts {prev+1}-{o['stage']+1}===\n"
            s += '{{#invoke:SeersSnare|layout\n |col0=\n'
            for i in range(o['stage']-prev+1):
                s += f' |col{i+1}=\n'
            prev = o['stage']+1
            s += '}}\n'
            rift = 'Timeless Rift ' + str(o['stage']+1)
            s += '{| class="wikitable default mw-collapsed mw-collapsible\n'
            s += '! ' + rift + '\n|-\n'
            map2.data.pop('enemy_pos')
            s += '|' + map2.Image(shortest=True).replace('#invoke:MapImage|initTabber','MapImage')[:-2] + f'|init={self.name}|initTab={rift} - Advanced' + '}}\n|}\n'
            s += Map.UnitData({rift + ' - Intermediate': map1, rift + ' - Advanced': map2}).replace('==Unit data==\n','').replace('=-;','=;') + '\n'

        data = self.data['stages']['stages'][-1]
        o = self.data['boss_battle'][0]
        map1 = Map.create(o['intermediate'][:-1])
        map2 = Map.create(o['advanced'][:-1])
        for map,idx,count in ((map1,1,4), (map2,2,5)):
            print(self.data['final_boss'])
            map.data['units'] = [Map.PLACEHOLDER_UNIT | self.data['final_boss'] | {
                'init_cooldown': -1,
                'rarity': 5,
                'true_lv': data['boss_level'][idx],
                'stats': Units.get(o['unit']).Stats(data['boss_level'][idx], 5)#, data['hp_factor'][idx] / 100)
            }] + [Map.PLACEHOLDER_UNIT | Units.get(self.data['final_boss']['enemies'][i]).Skills(latest=True) | {
                'unit': self.data['final_boss']['enemies'][i],
                'init_cooldown': -1,
                'rarity': 5,
                'true_lv': data['level'][idx],
                'stats': Units.get(self.data['final_boss']['enemies'][i]).Stats(data['level'][idx]),
                'seal': weaponToSeal(unit)
            } for i in range(count)]

        s += f"===Rifts {prev+1}-{o['stage']+1}===\n"
        s += '{{#invoke:SeersSnare|layout\n |col0=\n'
        for i in range(o['stage']-prev+1):
            s += f' |col{i+1}=\n'
        s += '}}\n'
        rift = 'Timeless Rift ' + str(o['stage']+1)
        s += '{| class="wikitable default mw-collapsed mw-collapsible\n'
        s += '! ' + rift + '\n|-\n'
        map2.data.pop('enemy_pos')
        s += '|' + map2.Image(shortest=True).replace('#invoke:MapImage|initTabber','MapImage')[:-2] + f'|init={self.name}|initTab={rift} - Advanced' + '}}\n|}\n'
        s += Map.UnitData({rift + ' - Intermediate': map1, rift + ' - Advanced': map2}).replace('==Unit data==\n','') + '\n'

        return s[:-1]

    def createArticle(self):
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += self.UnitData() + '\n'
        self.page += '{{Main Events Navbox}}'
        return self

SS = SeersSnare