#! /usr/bin/env python3

from ..Tool.ArticleContainer import ArticleContainer
from .Reader.TT import TempestTrialsReader as Reader

class TempestTrials(ArticleContainer):
    _reader = Reader
    _linkArticleData = (r'startTime\s*=\s*([0-9TZ\-:]{20})', ['avail','start'])

    TT_DIFFICULTIES = ["Normal/LV.8/3 battles","Normal/LV.14/3 battles","Normal/LV.20/3 battles","Hard/LV.25/4 battles","Hard/LV.30/5 battles","Lunatic/LV.35/5 battles","Lunatic/LV.40/7 battles"]

    def __init__(self):
        super().__init__()
        self.story = ''

    @property
    def name(self) -> str:
        from ..Utility.Messages import Messages
        return super().name or Messages.EN('MID_SEQUENTIAL_MAP_TERM_'+self.data['id_tag'])

    def Infobox(self):
        from re import sub,search
        from ..Utility.Sound import BGM
        from ..Utility.Units import Heroes
        from ..Stages import MainStory, Paralogue, Map
        from ..Tool.misc import cleanStr
        bHeroes = self.data['unit_bonus1']['units'] + self.data['unit_bonus2']['units']
        rHeroes = set(r['id_tag'] for d in self.data['score_rewards'] for r in d['reward'] if r['kind'] == 'Hero')
        stages = set(m[:-1] for s in self.data['sets'] for b in s['battles'][:-1] for m in b['maps'])

        stages = list(sorted([MainStory.get(m) or Paralogue.get(m) for m in stages], key=lambda o: o.data['id_tag']))
        for i in range(len(stages)):
            if i >= len(stages): break
            idx = sorted([o.idx+1 for o in stages[i:] if o.data['id_tag'] == stages[i].data['id_tag']])
            n = stages[i].groupName
            if isinstance(stages[i], MainStory):
                stages[i] = '[[Story Maps#' + (n if n.find('Chapter ') == -1 else n[n.find('Chapter '):]) + '|' + n
                if len(idx) != 5:
                    stages[i] += ' (Maps ' + ' & '.join([str(v) for v in idx]).replace(' & ', ', ', len(idx)-2) + ')'
                stages[i] += ']]'
            else:
                stages[i] = '[[Paralogue Maps#' + n + '|' + n
                if len(idx) != 3:
                    stages[i] += ' (Maps ' + ' & '.join([str(v) for v in idx]).replace(' & ', ', ', len(idx)-2) + ')'
                stages[i] += ']]'
            for _ in range(len(idx)-1): stages.pop(i+1)

        map = Map.get(self.data['sets'][-1]['battles'][-1]['maps'][0])
        map.data['enemy_pos'] = [unit['pos'] for unit in map.data['units']]
        map.data['enemy_pos'][0] = ''

        return '{| style="float:right"\n|' + super().Infobox('Tempest Trials', {
            'name': self.name,
            'series': sub(' \w+$','',self.name) if search(' (\d+|Finale)$',self.name) else None,
            'promoArt': 'Tempest_Trials_' + cleanStr(self.name) + '_2.jpg',
            'bonusHeroes': ';'.join([Heroes.get(h).name for h in bHeroes]),
            'rewardHeroes': ';'.join([Heroes.get(h).name for h in rHeroes]),
            'maps': ' &<br>'.join(stages).replace(' &',',',len(stages)-2),
            'startTime': self.data['avail']['start'],
            'endTime': self.data['avail']['end']
        }) + '\n|-\n|' + super().Infobox('Battle', {
            'bannerImage': 'TT_' + self.data['banner_file'] + '.webp',
            'mapName': self.name,
            'mapGroup': 'Tempest Trials',
            'mapImage': map.Image(),
            'lvlNormal': '8{{RarityStar|2}}/14{{RarityStar|2}}/20{{RarityStar|3}}',
            'lvlHard': '25{{RarityStar|3}}/30{{RarityStar|4}}',
            'lvlLunatic': '35{{RarityStar|4}}/40{{RarityStar|5}}',
            'rarityNormal': '', 'rarityHard': '', 'rarityLunatic': '',
            'stamNormal': '10', 'stamHard': '12/15', 'stamLunatic': '15',
            'reward': '{{Score Reward|rewardNormal=25/30/35|rewardHard=35|rewardLunatic=40}}',}|
            {f"BGM{(i+1) if i != 0 else ''}": bgm for i,bgm in enumerate(BGM.bgms(self.data['sets'][-1]['battles'][-1]['maps'][0][:-1]))
        }) + '\n|}'
    
    def Availability(self):
        return super().Availability('[[Tempest Trials]]', self.data['avail'], 'Tempest Trials+: ' + self.name, isMap=True)

    def Rewards(self):
        from ..Utility.Reward import Reward
        s =  '==Rewards==\n'
        s += '{{#invoke:Reward/TempestTrials|score\n'
        for rewards in self.data['score_rewards']:
            s += f"|{rewards['score']}={Reward(rewards['reward'])}\n"
        s += '}}\n===Rank rewards===\n{{#invoke:Reward/TempestTrials|rank|time=\n'
        for rewards in self.data['rank_rewards']:
            s += f"|{rewards['rank_hi']:6}~{rewards['rank_lo']:6}={Reward(rewards['reward'])}\n"
        return s + '}}'

    def UnitData(self):
        from ..Stages.Terrain import Map
        from ..Utility.Units import Units
        from ..Tool.globals import MOVE_TYPE, WEAPON_TYPE, WEAPON_MASK
        s =  '==Unit data==\n'
        s += '{{#invoke:UnitData|main\n'
        for idiff,set in enumerate(self.data['sets']):
            map = Map.get(set['battles'][-1]['maps'][0])
            s += '|' + self.TT_DIFFICULTIES[idiff] + '=[\n'
            s += Map.Unit(map.data['units'][0], 0) + '\n'
            for i,unit in enumerate(map.data['units'][1:]):
                tmp = Map.Unit(unit, i+1)
                unit = Units.get(unit['unit']).data
                idx = tmp.find(';ai={')
                s += '{' + tmp[tmp.find(';pos=')+1 : tmp.find(';stats=')] + ';'
                s += tmp[idx+1:tmp.find('};',idx)+2]
                s += 'random={'
                s += 'moves=' + MOVE_TYPE[unit['move']] + ';'
                s += 'weapons=' + ('Ranged' if (WEAPON_MASK['Ranged'] & (1 << unit['weapon'])) else 'Close')
                if s[-6:] == 'Ranged':
                    s += ';staff=' + ('1' if WEAPON_TYPE[unit['weapon']] == 'Colorless Staff' else '0')
                s += '};};\n'
            s += ']\n'
        s += '}}\n'
        s += "===Randomized units===\nThe other enemy units are selected randomly from the below pool of Heroes:\n"
        for i,unit in enumerate(Map.get(self.data['sets'][-1]['battles'][-1]['maps'][0]).data['units'][1:]):
            unit = Units.get(unit['unit']).data
            wep = ('Ranged' if (WEAPON_MASK['Ranged'] & (1 << unit['weapon'])) else 'Close')
            s += f"====Enemy {i+2}: {wep} {MOVE_TYPE[unit['move']].lower()} unit====\n"
            s += f"{{{{RandomTTUnits|WeaponClass={wep}|MoveType={MOVE_TYPE[unit['move']]}|Date=" + self.data['avail']['start'][:10] +\
                ('|NoStaves=1' if wep == 'Ranged' and WEAPON_TYPE[unit['weapon']] != 'Colorless Staff' else '') + '}}\n'
        return s[:-1]

    def Story(self):
        import re
        from ..Utility.Scenario import Scenario
        from ..Tool.globals import TODO
        from ..Stages.Paralogues import Paralogue
        scenario = Scenario.get(self.data['scenario_file'])
        KEYS = ['MID_SCENARIO_OPENING', 'MID_SCENARIO_ADDITIONAL_TALK_0', 'MID_SCENARIO_ADDITIONAL_TALK_1', 'MID_SCENARIO_ENDING']
        if len(scenario) == 2:
            self.story = Scenario.Story(self.data['scenario_file']) + '<noinclude>[[Category:Tempest Trials scenarios]]</noinclude>'
        elif len(scenario) == 4 and sorted(scenario.keys()) == sorted(KEYS):
            self.story =  '{{#vardefine:isBase|{{#ifeq:{{BASEPAGENAME}}|'+self.name+'|1}}}}'
            self.story += '{{#vardefine:isTTSerie|{{#ifeq:{{FULLPAGENAME}}|'+re.sub(r' \d+| Finale','',self.name)+'/Story|1}}}}<!--\n'
            self.story += '-->{{#if:{{#var:isBase}}{{#var:isTTSerie}}|<!--\n-->{{#invoke:Scenario|story\n'
            self.story += '|opening=' + str(scenario[KEYS[0]]) + '\n'
            self.story += '}}}}<!--\n-->{{#if:{{#var:isTTSerie}}||<!--\n-->{{#invoke:Scenario|story\n'
            self.story += '|opening supplement=' + str(scenario[KEYS[1]]) + '\n'
            self.story += '|ending supplement=' + str(scenario[KEYS[2]]) + '\n'
            self.story += '}}}}<!--\n-->{{#if:{{#var:isBase}}{{#var:isTTSerie}}|<!--\n-->{{#invoke:Scenario|story\n'
            self.story += '|ending=' + str(scenario[KEYS[3]]) + '\n'
            self.story += '}}}}<noinclude>[[Category:Tempest Trials scenarios]]</noinclude>'
        else:
            self.story = ''
            print(TODO + 'Unexpected TT story: ' + str(scenario.keys()))

        paralogues = Paralogue.getGroup(self.data['avail']['start'], ('avail','start'))
        if len(paralogues) == 0:
            from ..Tool.misc import timeDiff
            paralogues = Paralogue.getGroup(timeDiff(self.data['avail']['start'], -86400), ('avail','start'))
        if len(paralogues) == 3:
            self.story = self.story.replace('</noinclude>', '[[Category:'+paralogues[0].category()+' scenarios]]</noinclude>')
        else:
            print(TODO + 'Unknown associated paralogue for TT: ' + self.name)

        s = '==Story==\n{{/Story}}\n'
        return s + Scenario.StoryNavbar(self.data['scenario_file'])

    def OtherLanguage(self):
        return super().OtherLanguage('MID_SEQUENTIAL_MAP_TERM_'+self.data['id_tag'])

    def createArticle(self):
        if self.data is None: return self

        self.page  = self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += self.UnitData() + '\n'
        self.page += self.Story() + '\n'
        self.page += '==Trivia==\n*\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Main Events Navbox}}'

        return self

    def export(self, summary: str, *, minor=False, create=True):
        from ..Tool.Wiki import Wiki
        Wiki.exportPages({
            self.name: self.page,
            self.name+'/Story': self.story
        }, summary, minor, create)
