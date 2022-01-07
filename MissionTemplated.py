#! /usr/bin/env python3

import re
from datetime import date, datetime
from Reverse import Reverse

from util import TIME_FORMAT

SINGULAR_QUESTS = {
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) Training": {
        'sort': 2,
        'timeChecker': lambda start,end: datetime.strptime(start, TIME_FORMAT).day == 1 and datetime.strptime(end, TIME_FORMAT).day == 1,
        'quests': [
            {'name': 'Tower: 1st Stratum', 'description': 'Clear the first stratum of the Training Tower.<br>All four allies must survive.', 'times': 5, 'reward': r'\{kind=Hero Feather;count=100\}', 'stage': 'First Stratum'},
            {'name': 'Tower: 2nd Stratum', 'description': 'Clear the second stratum of the Training Tower.<br>All four allies must survive.', 'times': 5, 'reward': r'\{kind=Hero Feather;count=100\}', 'stage': 'Second Stratum'},
            {'name': 'Tower: 3rd Stratum', 'description': 'Clear the third stratum of the Training Tower.<br>All four allies must survive.', 'times': 5, 'reward': r'\{kind=Hero Feather;count=100\}', 'stage': 'Third Stratum'},
            {'name': 'Tower: 4th Stratum', 'description': 'Clear the fourth stratum of the Training Tower.<br>All four allies must survive.', 'times': 5, 'reward': r'\{kind=Hero Feather;count=100\}', 'stage': 'Fourth Stratum'},
            {'name': 'Tower: 5th Stratum', 'description': 'Clear the fifth stratum of the Training Tower.<br>All four allies must survive.', 'times': 10, 'reward': r'\{kind=Orb\}', 'stage': 'Fifth Stratum'},
            {'name': 'Tower: 6th Stratum', 'description': 'Clear the sixth stratum of the Training Tower.<br>All four allies must survive.', 'times': 10, 'reward': r'\{kind=Orb\}', 'stage': 'Sixth Stratum'},
            {'name': 'Tower: 7th Stratum', 'description': 'Clear the seventh stratum of the Training<br>Tower. All four allies must survive.', 'times': 10, 'reward': r'\{kind=Orb\}', 'stage': 'Seventh Stratum'},
            {'name': 'Tower: 8th Stratum', 'description': 'Clear the eighth stratum of the Training Tower.<br>All four allies must survive.', 'times': 15, 'reward': r'\{kind=Orb\}', 'stage': 'Eighth Stratum'},
            {'name': 'Tower: 9th Stratum', 'description': 'Clear the ninth stratum of the Training Tower.<br>All four allies must survive.', 'times': 15, 'reward': r'\{kind=Orb\}', 'stage': 'Ninth Stratum'},
            {'name': 'Tower: 10th Stratum', 'description': 'Clear the tenth stratum of the Training Tower.<br>All four allies must survive.', 'times': 15, 'reward': r'\{kind=Orb\}', 'stage': 'Tenth Stratum'},
            {'name': 'Tower: 10th Stratum', 'description': 'Clear the tenth stratum of the Training Tower<br>using only infantry allies. \\(Allies deployed as<br>cohorts using Pair Up do not count.\\) All four<br>allies must survive.', 'times': 15, 'reward': r'\{kind=Orb\}', 'stage': 'Tenth Stratum'},
            {'name': 'Tower: 10th Stratum', 'description': 'Clear the tenth stratum of the Training Tower<br>using only armored allies. \\(Allies deployed as<br>cohorts using Pair Up do not count.\\) All four<br>allies must survive.', 'times': 15, 'reward': r'\{kind=Orb\}', 'stage': 'Tenth Stratum'},
            {'name': 'Tower: 10th Stratum', 'description': 'Clear the tenth stratum of the Training Tower<br>using only cavalry allies. \\(Allies deployed as<br>cohorts using Pair Up do not count.\\) All four<br>allies must survive.', 'times': 15, 'reward': r'\{kind=Orb\}', 'stage': 'Tenth Stratum'},
            {'name': 'Tower: 10th Stratum', 'description': 'Clear the tenth stratum of the Training Tower<br>using only flying allies. \\(Allies deployed as<br>cohorts using Pair Up do not count.\\) All four<br>allies must survive.', 'times': 15, 'reward': r'\{kind=Orb\}', 'stage': 'Tenth Stratum'}
        ],
        'template': lambda _: '{{Monthly Training Quest}}'
    },
    'RB / AA': {
        'sort': 3,
        'avail': 604800,
        'cycle': 1209600,
        'quests': [
            {'name': 'Resonant Battles Score', 'description': 'Earn a score in Resonant Battles<br>at any difficulty.', 'reward': r'\{kind=Orb\}'}, 
            {'name': 'Arena Assault: Win 1', 'description': 'Win one battle in Arena Assault.', 'reward': r'\{kind=Hero Feather;count=400\}'}, 
            {'name': 'Arena Assault: 2 in a Row', 'description': 'Win two consecutive battles in Arena Assault.', 'reward': r'\{kind=Dueling Crest;count=7\}'}
        ],
        'template': lambda group: '{{RB AA Quest|start='+group['startTime']+'|end='+group['endTime']+'}}'
    },
    'RB / AB / AA': {
        'sort': 3,
        'avail': 604800,
        'cycle': 1209600,
        'quests': [
            {'name': 'Resonant Battles Score', 'description': 'Earn a score in Resonant Battles<br>at any difficulty.', 'reward': r'\{kind=Orb\}'}, 
            {'name': 'Win Allegiance Battles', 'description': 'Win Allegiance Battles on any difficulty.', 'reward': r'\{kind=Hero Feather;count=800\}'}, 
            {'name': 'Arena Assault: Win 1', 'description': 'Win one battle in Arena Assault.', 'reward': r'\{kind=Hero Feather;count=400\}'}
        ],
        'template': lambda group: '{{RB AB AA Quest|start='+group['startTime']+'|end='+group['endTime']+'}}'
    },
    r"\s*Feh Pass": {
        'sort': 50,
        'timeChecker': lambda start,end: (datetime.strptime(start, TIME_FORMAT).day, datetime.strptime(end, TIME_FORMAT).day) in [(10,25),(25,10)],
        'quests': [
            {'name': 'KO Foe', 'description': 'Defeat a foe.', 'times': 3, 'reward': r'\{kind=Orb;count=3\}'}, 
            {'name': 'KO Foe', 'description': 'Defeat a foe.', 'times': 30, 'reward': r'\{kind=Orb;count=2\}'}, 
            {'name': 'Win Arena Duels', 'description': 'Win Arena Duels at any difficulty.', 'reward': r'\{kind=Divine Code: Part \d+;count=120\}'}, 
            {'name': 'Win Arena Duels', 'description': 'Win Arena Duels at any difficulty.', 'times': 3, 'reward': r'\{kind=Divine Dew;count=35\}'}, 
            {'name': 'KO Armored Foe', 'description': 'Defeat an armored foe.', 'reward': r'\{kind=Heroic Grail;count=50\}'}, 
            {'name': 'KO Flying Foe', 'description': 'Defeat a flying foe.', 'reward': r'\{kind=Aether Stone;count=120\}'}
        ],
        'template': lambda group: f"{{{{Feh Pass Quest|start={group['startTime']}|end={group['endTime']}|Divine Code={group['quests'][2]['reward'][19:-11]}}}}}"
    },
    # Story Maps
    ".*": {
        'sort': 10,
        'timeChecker': lambda start,end: True,
        'quests': [
            {'name': r'Clear \d+-1 on Lunatic', 'description': r'Clear Book [IVX]+, Chapter \d+: Part 1 on Lunatic<br>difficulty with (a sword|a lance|an axe) ally on your team. \(Allies<br>deployed as cohorts using Pair Up do not<br>count.\) All four allies must survive.', 'reward': r'\{kind=Orb\}'},
            {'name': r'Clear \d+-2 on Lunatic', 'description': r'Clear Book [IVX]+, Chapter \d+: Part 2 on Lunatic<br>difficulty with (a sword|a lance|an axe) ally on your team. \(Allies<br>deployed as cohorts using Pair Up do not<br>count.\) All four allies must survive.', 'reward': r'\{kind=Orb\}'},
            {'name': r'Clear \d+-3 on Lunatic', 'description': r'Clear Book [IVX]+, Chapter \d+: Part 3 on Lunatic<br>difficulty with (a sword|a lance|an axe) ally on your team. \(Allies<br>deployed as cohorts using Pair Up do not<br>count.\) All four allies must survive.', 'reward': r'\{kind=Orb\}'},
            {'name': r'Clear \d+-4 on Lunatic', 'description': r'Clear Book [IVX]+, Chapter \d+: Part 4 on Lunatic<br>difficulty with (a sword|a lance|an axe) ally on your team. \(Allies<br>deployed as cohorts using Pair Up do not<br>count.\) All four allies must survive.', 'reward': r'\{kind=Orb\}'},
            {'name': r'Clear \d+-5 on Lunatic', 'description': r'Clear Book [IVX]+, Chapter \d+: Part 5 on Lunatic<br>difficulty with (a sword|a lance|an axe) ally on your team. \(Allies<br>deployed as cohorts using Pair Up do not<br>count.\) All four allies must survive.', 'reward': r'\{kind=Orb\}'}
        ],
        'template': lambda group: \
            '{{Story Maps Quest|story='+'-'.join(re.search(r'Clear Book ([IVX]+), Chapter (\d+)',group['quests'][0]['description']).group(1,2))+'|title='+group['title']+\
            '|usedWeapon=' + {'sword,lance,axe,sword,lance':'1','lance,axe,sword,lance,axe':'2','axe,sword,lance,axe,sword':'3'}[','.join([re.search('with an? (sword|lance|axe)', group['quests'][i]['description'])[1] for i in range(5)])]+\
            '|start='+group['startTime']+'|end='+group['endTime']+'}}'
    },
    # Paralogue Maps
    "..*": {
        'sort': 11,
        'timeChecker': lambda start,end: True,
        'quests': [
            {'name': r'Clear P\d+-1 on Lunatic', 'description': r'Clear Paralogue \d+: Part 1 on Lunatic difficulty<br>with (a sword|a lance|an axe) ally on your team\. \(Allies deployed<br>as cohorts using Pair Up do not count\.\) All four<br>allies must survive\.', 'reward': r'\{kind=Orb\}'},
            {'name': r'Clear P\d+-2 on Lunatic', 'description': r'Clear Paralogue \d+: Part 2 on Lunatic difficulty<br>with (a sword|a lance|an axe) ally on your team\. \(Allies deployed<br>as cohorts using Pair Up do not count\.\) All four<br>allies must survive\.', 'reward': r'\{kind=Orb\}'},
            {'name': r'Clear P\d+-3 on Lunatic', 'description': r'Clear Paralogue \d+: Part 3 on Lunatic difficulty<br>with (a sword|a lance|an axe) ally on your team\. \(Allies deployed<br>as cohorts using Pair Up do not count\.\) All four<br>allies must survive\.', 'reward': r'\{kind=Orb\}'}
        ],
        'template': lambda group: \
            '{{Paralogue Maps Quest|paralogue='+group['quests'][0]['name'][7:-13]+'|title='+group['title']+\
            '|usedWeapon=' + {'sword,lance,axe':'1','lance,axe,sword':'2','axe,sword,lance':'3'}[','.join([re.search('with an? (sword|lance|axe)', group['quests'][i]['description'])[1] for i in range(3)])]+\
            '|start='+group['startTime']+'|end='+group['endTime']+'}}'
    },

    'Voting Gauntlet': {
        'sort': 15,
        'avail': 172800,
        'count': 3,
        'quests': [
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet.','reward':r'\{kind=Orb;count=2\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet.','times':2,'reward':r'\{kind=Sacred Coin;count=30\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet.','times':3,'reward':r'\{kind=Refining Stone;count=10\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet.','times':4,'reward':r'\{kind=Sacred Coin;count=15\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet.','times':5,'reward':r'\{kind=Orb;count=2\}'},
            {'name':'Tower: 2nd Stratum','description':'Clear the second stratum of the Training Tower.','times':5,'reward':r'\{kind=Battle Flag;count=100\}','stage':'Second Stratum'},
            {'name':'Tower: 5th Stratum','description':'Clear the fifth stratum of the Training Tower.','times':5,'reward':r'\{kind=Battle Flag;count=100\}','stage':'Fifth Stratum'},
            {'name':'Tower: 8th Stratum','description':'Clear the eighth stratum of the Training Tower.','times':5,'reward':r'\{kind=Battle Flag;count=100\}','stage':'Eighth Stratum'},
            {'name':'Win Arena Duels','description':'Win Arena Duels at any difficulty.','reward':r'\{kind=Battle Flag;count=100\}'},
            {'name':'Win Arena Duels','description':'Win Arena Duels at any difficulty.','times':2,'reward':r'\{kind=Battle Flag;count=100\}'},
            {'name':'Win Int.\\+ Arena Duels','description':'Win Arena Duels on Intermediate or higher<br>difficulty.','times':3,'reward':r'\{kind=Battle Flag;count=100\}'},
            {'name':'Win Int.\\+ Arena Duels','description':'Win Arena Duels on Intermediate or higher<br>difficulty.','times':5,'reward':r'\{kind=Battle Flag;count=100\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a red<br>ally on your team.','reward':r'\{kind=Battle Flag;count=200\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a blue<br>ally on your team.','reward':r'\{kind=Battle Flag;count=200\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a green<br>ally on your team.','reward':r'\{kind=Battle Flag;count=200\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a<br>colorless ally on your team.','reward':r'\{kind=Battle Flag;count=200\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a red<br>ally on your team.','times':2,'reward':r'\{kind=Divine Code: Ephemera \d+;count=10}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a blue<br>ally on your team.','times':2,'reward':r'\{kind=Divine Code: Ephemera \d+;count=10}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a green<br>ally on your team.','times':2,'reward':r'\{kind=Divine Code: Ephemera \d+;count=10}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a<br>colorless ally on your team.','times':2,'reward':r'\{kind=Divine Code: Ephemera \d+;count=10}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a red<br>ally on your team.','times':3,'reward':r'\{kind=Battle Flag;count=100\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a blue<br>ally on your team.','times':3,'reward':r'\{kind=Battle Flag;count=100\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a green<br>ally on your team.','times':3,'reward':r'\{kind=Battle Flag;count=100\}'},
            {'name':'Voting Gauntlet','description':'Win a battle in the Voting Gauntlet with a<br>colorless ally on your team.','times':3,'reward':r'\{kind=Battle Flag;count=100\}'}
        ],
        'template': lambda group: f"{{{{Voting Gauntlet Quest|start={group['startTime']}|Divine Code={group['quests'][16]['reward'][19:-10]}|stage={group['quests'][0]['stage']}}}}}"
    },
    'Grand Conquests': {
        'sort': 18,
        'avail': 172800,
        'count': 3,
        'quests': [
            {'name':'GC: Earn Score','description':'Earn points in Grand Conquests.','reward':r'\{kind=Orb\}'},
            {'name':'GC: Earn Score','description':'Earn points in Grand Conquests.','times':2,'reward':r'\{kind=Universal Shard;count=1500\}'},
            {'name':'GC: Earn Score','description':'Earn points in Grand Conquests.','times':3,'reward':r'\{kind=Hero Feather;count=150\}'},
            {'name':'Tower: 2nd Stratum','description':'Clear the second stratum of the Training Tower.','times':5,'reward':r'\{kind=Conquest Lance\}','stage':'Second Stratum'},
            {'name':'Tower: 8th Stratum','description':'Clear the eighth stratum of the Training Tower.','times':5,'reward':r'\{kind=Conquest Lance\}','stage':'Eighth Stratum'},
            {'name':'Win Arena Duels','description':'Win Arena Duels on any difficulty.','times':5,'reward':r'\{kind=Conquest Lance\}'}
        ],
        'template': lambda group: f"{{{{Grand Conquests Quest|start={group['startTime']}|stage={group['quests'][0]['stage']}}}}}"
    },
    'Røkkr Sieges': {
        'sort': 20,
        'avail': 172800,
        'count': 3,
        'quests': [
            {'name':'Røkkr Sieges','description':'Clear a battle in Røkkr Sieges.','reward':r'\{kind=Orb\}'},
            {'name':'Røkkr Sieges','description':'Clear a battle in Røkkr Sieges.','times':2,'reward':r'\{kind=Universal Shard;count=1500\}'},
            {'name':'Røkkr Sieges','description':'Clear a battle in Røkkr Sieges.','times':3,'reward':r'\{kind=Hero Feather;count=150\}'},
            {'name':'Røkkr Sieges','description':'Clear a battle in Røkkr Sieges.','reward':r'\{kind=Divine Code: Ephemera \d+;count=10\}'},
            {'name':'Røkkr Sieges','description':'Clear a battle in Røkkr Sieges.','times':2,'reward':r'\{kind=Divine Code: Ephemera \d+;count=10\}'},
            {'name':'Røkkr Sieges','description':'Clear a battle in Røkkr Sieges.','times':3,'reward':r'\{kind=Divine Code: Ephemera \d+;count=10\}'},
            {'name':'Røkkr Sieges','description':'Clear a battle in Røkkr Sieges.','times':4,'reward':r'\{kind=Divine Code: Ephemera \d+;count=10\}'},
            {'name':'Tower: 2nd Stratum','description':'Clear the second stratum of the Training Tower.','times':5,'reward':r'\{kind=Havoc Axe\}','stage':'Second Stratum'},
            {'name':'Tower: 8th Stratum','description':'Clear the eighth stratum of the Training Tower.','times':5,'reward':r'\{kind=Havoc Axe\}','stage':'Eighth Stratum'},
            {'name':'Win Arena Duels','description':'Win Arena Duels at any difficulty.','times':5,'reward':r'\{kind=Havoc Axe\}'}
        ],
        'template': lambda group: f"{{{{Rokkr Siege Quest|start={group['startTime']}|Divine Code={group['quests'][3]['reward'][19:-10]}|stage={group['quests'][0]['stage']}}}}}"
    },
    "Mjölnir's Strike": {
        'sort': 23,
        'avail': 172800,
        'quests': [
            {'name': 'KO w/Summoner', 'description': "Defeat a foe with the My Summoner unit<br>in Mjölnir's Strike.", 'reward': r"\{kind=Divine Code: Part \d+;count=20\}", 'unit': 'PID_アバター'},
            {'name': 'KO w/Summoner', 'description': "Defeat a foe with the My Summoner unit<br>in Mjölnir's Strike.", 'times': 5, 'reward': r"\{kind=Divine Code: Part \d+;count=40\}", 'unit': 'PID_アバター'}
        ],
        'template': lambda group: f"{{{{Mjolnirs Strike Quest|start={group['startTime']}|Divine Code={group['quests'][0]['reward'][19:-10]}}}}}"
    },
    'Frontline Phalanx': {
        'sort': 24,
        'avail': 864000,
        'quests': [
            {'name':'Tower: 1st Stratum','description':'Clear the first stratum of the Training Tower.','reward':r'\{kind=Guardian Shield\}','stage':'First Stratum'},
            {'name':'Tower: 4th Stratum','description':'Clear the fourth stratum of the Training Tower.','reward':r'\{kind=Guardian Shield\}','stage':'Fourth Stratum'},
            {'name':'Tower: 7th Stratum','description':'Clear the seventh stratum of the<br>Training Tower.','reward':r'\{kind=Guardian Shield\}','stage':'Seventh Stratum'},
        ],
        'template': lambda group: '{{Frontline Phalanx Quest|start='+group['startTime']+'}}'
    },
    'Pawns of Loki': {
        'sort': 25,
        'avail': 172800,
        'quests': [
            {'name': 'PoL: Complete a Game', 'description': 'Finish all turns to complete a game of Pawns<br>of Loki.', 'reward': r'\{kind=Orb\}'}
        ],
        'template': lambda group: '{{Pawns of Loki Quest|start='+group['startTime']+'}}'
    },
    'Heroes Journey': {
        'sort': 26,
        'avail': 86400,
        'count': 4,
        'quests': [
            {'name': 'Clear Heroes Journey', 'description': 'Clear Heroes Journey.', 'reward': r'\{kind=Orb;count=3\}'}, 
            {'name': 'Clear Heroes Journey', 'description': 'Clear Heroes Journey.', 'reward': r'\{kind=Stamina Potion\}'}
        ],
        'template': lambda group: '{{Heroes Journey Quest|start='+group['startTime']+'}}'
    },
}
ALTERNATING_QUESTS = {
    "Daily Quest": {
        'sort': 4,
        'groups': [
            {
                'avail': 86400,
                'timeChecker': lambda start,end,i: datetime.strptime(start,TIME_FORMAT).weekday()==i,
                'quests': [
                    {'name': 'KO Foe', 'description': 'Defeat an enemy.', 'times': 10, 'reward': '\\{kind='+reward1+(';count='+rewardCount if rewardCount != '1' else '')+'\\}'},
                    {'name': 'KO Foe', 'description': 'Defeat an enemy.', 'times': 20, 'reward': '\\{kind='+reward2+(';count='+rewardCount if rewardCount != '1' else '')+'\\}'},
                    {'name': 'Win Arena Duels', 'description': 'Win Arena Duels at any difficulty.', 'times': 2, 'reward': r'\{kind=Hero Feather;count=100\}'}
                ]
            } for reward1, reward2, rewardCount in zip(
                ['Universal Shard','Scarlet Shard','Azure Shard','Verdant Shard','Transparent Shard','Dueling Crest','Stamina Potion'],
                ['Universal Crystal','Scarlet Crystal','Azure Crystal','Verdant Crystal','Transparent Crystal','Orb','Orb'],
                ['1000']*5+['1']*2)
        ],
        'template': lambda groups: '{{Daily Quest|start='+groups[0]['startTime'].split(',')[0]+'|end='+max([group['endTime'].split(',')[-1] for group in groups])+'}}'
    }
}
GROUP_QUESTS = {
    "Tempest Trials": {
        'sort': 16,
        'groups': [
            {
                'avail': 86400,
                'quests': []
            },
            {
                'avail': 86400,
                'quests': []
            }
        ],
        'template': lambda groups: ''
    }
}

[
    {'title': 'Tempest Trials', 'startTime': '2021-12-16T07:00:00Z', 'endTime': '2021-12-21T06:59:59Z', 'availTime': 86400, 'sort': 16, 'quests': [{'name': 'Clear Trial', 'description': 'Clear one of the final maps in Tempest Trials.', 'reward': r'\{kind=Refining Stone;count=2\}', 'stage': 'Ice & Flame Finale'}, {'name': 'Clear Trial', 'description': 'Clear one of the final maps in Tempest Trials.', 'reward': r'\{kind=Stamina Potion\}', 'stage': 'Ice & Flame Finale'}, {'name': 'Clear Trial', 'description': 'Clear one of the final maps in Tempest Trials.', 'times': 2, 'reward': r'\{kind=Universal Crystal;count=1500\}', 'stage': 'Ice & Flame Finale'}, {'name': 'Clear Trial', 'description': 'Clear one of the final maps in Tempest Trials.', 'times': 3, 'reward': r'\{kind=Hero Feather;count=150\}', 'stage': 'Ice & Flame Finale'}]},
    {'title': 'Tempest Trials', 'startTime': '2021-12-21T07:00:00Z', 'endTime': '2021-12-26T06:59:59Z', 'availTime': 86400, 'sort': 16, 'quests': [{'name': 'Clear Trial', 'description': 'Clear one of the final maps in Tempest Trials.', 'reward': r'\{kind=Refining Stone;count=4\}', 'stage': 'Ice & Flame Finale'}, {'name': 'Clear Trial', 'description': 'Clear one of the final maps in Tempest Trials.', 'reward': r'\{kind=Stamina Potion;count=2\}', 'stage': 'Ice & Flame Finale'}, {'name': 'Clear Trial', 'description': 'Clear one of the final maps in Tempest Trials.', 'times': 2, 'reward': r'\{kind=Universal Crystal;count=3000\}', 'stage': 'Ice & Flame Finale'}, {'name': 'Clear Trial', 'description': 'Clear one of the final maps in Tempest Trials.', 'times': 3, 'reward': r'\{kind=Hero Feather;count=300\}', 'stage': 'Ice & Flame Finale'}]},
]

def checkSingularQuest(group: dict, obj: dict, objTitle: str):
    if not re.match(objTitle, group['title']): return False
    if group['sort'] != obj['sort']: return False
    # Check availability
    if 'timeChecker' in obj:
        if not all([obj['timeChecker'](start,end) for start,end in zip(group['startTime'].split(','),group['endTime'].split(','))]): return False
    else:
        if 'cycleTime' in group and ('cycle' not in obj or obj['cycle'] != group['cycleTime']): return False
        times = list(zip([datetime.strptime(starttime, TIME_FORMAT) for starttime in group['startTime'].split(',')], [datetime.strptime(endtime, TIME_FORMAT) for endtime in group['endTime'].split(',')]))
        if 'count' in obj:
            if 'availTime' in group:
                if obj['avail'] != group['availTime'] or any([(end-start).total_seconds()+1 != obj['avail']*obj['count'] for start,end in times]): return False
            elif len(times) % obj['count'] != 0 or any([(end-start).total_seconds()+1 != obj['avail'] for start,end in times]): return False
        else:
            if 'availTime' in group:
                if obj['avail'] != group['availTime']: return False
            elif any([(end-start).total_seconds()+1 != obj['avail'] for start,end in times]): return False
    # Check quests
    if len(obj['quests']) != len(group['quests']): return False
    for ref,qu in zip(obj['quests'],group['quests']):
        for key in ref:
            if key not in qu: return False
            if isinstance(ref[key],str):
                if not re.match(ref[key],qu[key]): return False
            elif ref[key] != qu[key]: return False
    return True

def templateMissions(groups):
    for i,group in enumerate(groups):
        for title, obj in SINGULAR_QUESTS.items():
            if not checkSingularQuest(group, obj, title): continue
            groups[i] = obj['template'](group)
            break

    groupedGroup = {}
    for i,group in enumerate(groups):
        if isinstance(group, str): continue
        if group['title'] in groupedGroup:
            groupedGroup[group['title']]['groups'].append(group)
            groupedGroup[group['title']]['index'].append(i)
        else:
            groupedGroup[group['title']] = {'groups': [group], 'index': [i]}
    removeIndex = []
    for title,group in groupedGroup.items():
        group['groups'] = sorted(group['groups'], key=lambda o:o['startTime'])
        for pattern,obj in ALTERNATING_QUESTS.items():
            if not re.match(pattern,title): continue
            if not all([gr['sort']==obj['sort'] for gr in group['groups']]): continue
            # Check global availability
            cycle = sum([gr['avail'] for gr in obj['groups']])
            if not all(['cycleTime' not in gr or gr['cycleTime']==cycle for gr in group['groups']]): continue
            # Check correspondance of first group
            firstIndex = -1
            for i,gr in enumerate(obj['groups']):
                if 'availTime' in group['groups'][0]:
                    if gr['avail'] != group['groups'][0]['availTime']: continue
                elif any([(datetime.strptime(end,TIME_FORMAT)-datetime.strptime(start,TIME_FORMAT)).total_seconds()+1 != gr['avail'] for start,end in zip(group['groups'][0]['startTime'].split(','),group['groups'][0]['endTime'].split(','))]): continue
                if 'timeChecker' in gr and not all([gr['timeChecker'](start,end,i) for start,end in zip(group['groups'][0]['startTime'].split(','),group['groups'][0]['endTime'].split(','))]): continue
                if len(gr['quests']) != len(group['groups'][0]['quests']): continue
                for ref,qu in zip(gr['quests'],group['groups'][0]['quests']):
                    for key in ref:
                        if key not in qu: firstIndex = -2
                        if isinstance(ref[key],str):
                            if not re.match(ref[key],qu[key]): firstIndex = -2
                        elif ref[key] != qu[key]: firstIndex = -2
                if firstIndex == -2: firstIndex = -1; continue
                firstIndex = i
                break
            if firstIndex < 0: continue
            # Check correspondance of other groups
            for i,gr in enumerate(group['groups'][1:]):
                i = (firstIndex+i+1)%len(obj['groups'])
                if 'availTime' in gr:
                    if obj['groups'][i]['avail'] != gr['availTime']: firstIndex = -1; break
                elif any([(datetime.strptime(end,TIME_FORMAT)-datetime.strptime(start,TIME_FORMAT)).total_seconds()+1 != obj['groups'][i]['avail'] for start,end in zip(gr['startTime'].split(','),gr['endTime'].split(','))]): firstIndex = -1; break
                if 'timeChecker' in obj['groups'][i] and not all([obj['groups'][i]['timeChecker'](start,end,i) for start,end in zip(gr['startTime'].split(','),gr['endTime'].split(','))]): firstIndex = -1; break
                if len(obj['groups'][i]['quests']) != len(gr['quests']): firstIndex = -1; break
                for ref,qu in zip(obj['groups'][i]['quests'],gr['quests']):
                    for key in ref:
                        if key not in qu: firstIndex = -1
                        if isinstance(ref[key],str):
                            if not re.match(ref[key],qu[key]): firstIndex = -1
                        elif ref[key] != qu[key]: firstIndex = -1
                if firstIndex == -1: break
            # Replace the groups
            i = min(group['index'])
            group['index'].remove(i)
            removeIndex += group['index']
            groups[i] = obj['template'](group['groups'])
            break
    for i in sorted(removeIndex, reverse=True): groups.pop(i)
    return groups