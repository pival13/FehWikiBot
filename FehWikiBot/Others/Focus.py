#! /usr/bin/env python3

from typing_extensions import Self, LiteralString
from ..Tool import Article, Container
from .Reader.Summon import FocusReader

class FocusTickets(Container):
    _reader = FocusReader

    @classmethod
    def load(cls, name: str) -> bool:
        if name in cls._DATA: return False
        reader = cls._reader.fromAssets(name)
        if not reader.isValid() or reader.object is None: return False
        objs = reader.object['summons']
        cls._DATA[name] = {o[cls._key]: o for o in objs}
        return True

    @property
    def ticket(self) -> str|None:
        import re
        from ..Tool.globals import ROMAN
        if self.data is None or self.data['ticket_path'] is None:
            return None
        n = re.search(r'(\d+)\.png$', self.data['ticket_path'])
        n = (' ' + ROMAN[int(n[1])]) if n else ''
        if   self.data['ticket_path'].find('Icon_FreeSummonRed') != -1:
            return 'Red First Summon Ticket' + n
        elif self.data['ticket_path'].find('Icon_FreeSummon_Arena') != -1:
            return 'Silver First Summon Ticket ' + self.data['ticket_path'][-5]
        elif self.data['ticket_path'].find('Icon_FreeSummon_Secret') != -1:
            return 'Golden First Summon Ticket' + n
        elif re.search(r'FreeSummon\d*\.png$', self.data['ticket_path']):
            return 'First Summon Ticket' + n
        else:
            return '<!--First Summon Ticket (' + self.data['ticket_path'].replace('UI/FreeSummon/FreeSummon.plist/','') + ')-->'


class Focus(Article):
    @classmethod
    def get(cls, name:str) -> Self:
        o = super().fromWiki(name)
        if o is None:
            o = cls()
            o.name = name
            o.page = ''
        return o

    TYPES = [
        'New Heroes', 'New Heroes Revival', 'Returning',
        'Special', 'Double Special Heroes',
        'Legendary', 'Mythic', 'Legendary & Mythic', 'Legendary & Mythic Hero Remix',
        'Voting Gauntlet', 'Tempest Trials', 'Hall of Forms', 'Hall of Forms Revival'
        'Bound Hero Battle',
        'Skill', 'New Power',
        'Weekly Revival', 'Legendary Revival',
        'Hero Fest',
        'A Hero Rises',
        'Other',
        'Free Summon',
        'Select Summon',
    ]

    def update(self, *, type: LiteralString, start: str, end: str, **kwargs) -> Self:
        def _parseTime(time: str):
            from datetime import datetime
            try:
                time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                try:
                    time = datetime.strptime(time, '%Y-%m-%d')
                except ValueError:
                    try:
                        time = datetime.strptime(time, '%b %d, %Y')
                    except ValueError:
                        print(self.name + ': Invalid time: ' + time)
                        return None
            return time

        import re

        kwargs |= {'type': type, 'start': start, 'end': end}
        if 'name' not in kwargs: kwargs['name'] = re.sub(r' \(.+?\)$', '', self.name)
        kwargs['start'] = _parseTime(start)
        kwargs['end'] = _parseTime(end)

        if (self.page.find(kwargs['start'].strftime('%Y-%m-%d')) != -1 or self.page.find(kwargs['start'].strftime('%b %d, %Y')) != -1) and kwargs['type'] != 'Select Summon':
            pass

        elif self.page == '':
            if len(kwargs.get('heroes',[])) == 0 and kwargs['type'] != 'Free Summon':
                return self
            self.page =  self.Infobox(kwargs) + '\n'
            self.page += self.OtherLanguage() + '\n'
            self.page += '{{Summoning Event Navbox}}'
            if kwargs['type'] in ('New Heroes','Special','Tempest Trials'):
                self.page += '\n{{Daily Log-In Bonus/Focus}}'
                if kwargs['name'][:14] == 'Harmonized CYL':
                    self.page = self.page[:-2] + '|name=Har. CYL Heroes Bonus}}'

        else:
            if 'shsr' in kwargs and kwargs['shsr'] and kwargs['name'].find('SHSR') == -1:
                kwargs['name'] += ' (4★SHSR)'
            if kwargs['type'] == 'Hall of Forms Revival':
                kwargs['name'] += ' Revival'
            format = '%Y' if type in ('Special','ω Special Heroes') else '%b %Y'
            if 'heroes' not in kwargs or kwargs['heroes'] == []:
                heroes = re.findall(r'\|\s*hero(\d+)\s*=\s*(.+?)(?=\n|\||\})', self.page)
                heroes = {o[0] : o[1] for o in heroes}
                kwargs['heroes'] = [o[1] for o in sorted([(k,v) for k,v in heroes.items()], key=lambda o: int(o[0]))]
                rarities = re.findall(r'\|\s*rarity(\d+)\s*=\s*(.+?)(?=\n|\||\})', self.page)
                rarities = {o[0]: o[1] for o in rarities}
                if len(rarities) != 0:
                    kwargs['focus4'] = [i+1 for i in range(len(heroes)) if str(i+1) not in rarities or rarities[str(i+1)] != '5']
            if self.page.find('{{tab/end}}') == -1:
                if type in ('Special','ω Special Heroes'):
                    time = re.search(r'start=(?:.+?, )?(\d{4})', self.page)[1]
                else:
                    time = _parseTime(re.search(r'start=\s*([^\}\|\n]+)', self.page)[1]).strftime(format)
                s1,s2 = self.page.split('==In other languages==', 1)
                self.page =  '{{tab/start}}{{tab/header|' + time + '}}' + s1
                self.page += '{{tab/header|' + kwargs['start'].strftime(format) + '}}' + self.Infobox(kwargs) + '\n'
                self.page += '{{tab/end}}\n==In other languages==' + s2
            else:
                s = '{{tab/header|' + kwargs['start'].strftime(format) + '}}' + self.Infobox(kwargs) + '\n'
                self.page = re.sub(r'\{\{tab/end\}\}', s + '{{tab/end}}', self.page, 1)

        return self


    def Infobox(self, params):
        s = '{{#invoke:SummoningFocus|focusPage\n'
        s += '|name=' + params['name'] + '\n'
        s += '|bannerType=' + params['type'] + '\n'
        if 'notif' in params:
            s += '|description={{SummoningEventDescription|notif=' + params['notif'] + '}}\n'
        else:
            s += '|description=\n'
        if 'youtube' in params and len(params['youtube']) == 2:
            s += '|youtubeEN=https://www.youtube.com/watch?v=' + params['youtube'][0] + '\n'
            s += '|youtubeJP=https://www.youtube.com/watch?v=' + params['youtube'][1] + '\n'

        if 'focus4' in params and (not isinstance(params['focus4'],list) or len(params['focus4']) == 0):
            params.pop('focus4')
        rarities = [f'|rarity{r}{s}Percent={float(params[str(r)+s]):.02f}%' for r in range(5,0,-1) for s in ('Focus','SHSpecial','Special','') if (str(r)+s) in params]
        if rarities != []: pass
        # 4% / 2%
        elif (params['type'] in ('Weekly Revival','Legendary Revival','Mythic Revival')) or (params['type'] == 'Special' and params.get('shsr')):
            rarities = ['|rarity5FocusPercent=4.00%','|rarity5Percent=2.00%']
            if 'focus4' in params: rarities.append('|rarity4FocusPercent=3.00%')
            if params.get('shsr'): rarities.append('|rarity4SHSpecialPercent=6.00%')
            rarities.append('|rarity4SpecialPercent=3.00%')
            rarities.append(f"|rarity4Percent={52 if 'focus4' in params else 55}.00%")
            rarities.append(f"|rarity3Percent={30 if params.get('shsr') else 36}.00%")
        # 8 Units, no 5*
        elif params['type'] in ('Returning', 'Double Special Heroes', 'Legendary & Mythic Hero Remix', 'A Hero Rises'):
            rarities = ['|rarity5FocusPercent=6.00%']
            if 'focus4' in params: rarities.append('|rarity4FocusPercent=3.00%')
            rarities.append('|rarity4SpecialPercent=3.00%')
            rarities.append(f"|rarity4Percent={54 if len(rarities) >= 3 else 57}.00%")
            rarities.append('|rarity3Percent=34.00%')
        # 8 Units, with 5*
        elif params['type'] == 'ω Special Heroes':
            rarities = ['|rarity5FocusPercent=6.00%','|rarity5Percent=2.00%']
            if 'focus4' in params: rarities.append('|rarity4FocusPercent=3.00%')
            if params.get('shsr'): rarities.append('|rarity4SHSpecialPercent=3.00%')
            rarities.append('|rarity4SpecialPercent=3.00%')
            rarities.append(f"|rarity4Percent={50 if len(rarities) > 3 else 53}.00%")
            rarities.append(f"|rarity3Percent={33 if len(rarities) > 5 else 36}.00%")
        # 12 Units, no 5*
        elif params['type'] in ('Legendary', 'Mythic', 'Emblem', '12 Luminaries') or params['type'].find(' & ') != -1:
            rarities = ['|rarity5FocusPercent=8.00%']
            if 'focus4' in params: rarities.append('|rarity4FocusPercent=3.00%')
            rarities.append('|rarity4SpecialPercent=3.00%')
            rarities.append(f'|rarity4Percent={53 if len(rarities) > 2 else 55}.00%')
            rarities.append(f'|rarity3Percent={33 if len(rarities) > 3 else 34}.00%')
        elif params['type'] == 'Hero Fest':
            rarities = ['|rarity5FocusPercent=5.00%','|rarity5Percent=3.00%','|rarity4SpecialPercent=3.00%','|rarity4Percent=55.00%','|rarity3Percent=34.00%']
        elif params['type'] in ('Free Summon', 'Select Summon'):
            if params['name'].find('4★SHSR') != -1:
                rarities = ['|rarity4SHSpecialPercent=100.00%']
            elif params['name'].find('Arena Reward') != -1:
                rarities = ['|rarity4SpecialPercent=100.00%']
            else:
                rarities = ['|rarity5FocusPercent=100.00%']
        else:
            if 'focus4' in params:
                rarities = ['|rarity5FocusPercent=3.00%','|rarity5Percent=3.00%','|rarity4FocusPercent=3.00%','|rarity4SpecialPercent=3.00%','|rarity4Percent=52.00%','|rarity3Percent=36.00%']
            else:
                rarities = ['|rarity5FocusPercent=3.00%','|rarity5Percent=3.00%',                             '|rarity4SpecialPercent=3.00%','|rarity4Percent=55.00%','|rarity3Percent=36.00%']
        s += '\n'.join(rarities) + '\n'

        for i,h in enumerate(params.get('heroes', [])):
            s += f'|hero{i+1}={h}\n'
            if 'focus4' in params and (i+1) not in params['focus4']:
                s += f'|rarity{i+1}=5\n'

        s += '|start=' + params['start'].strftime('%Y-%m-%d') + 'T07:00:00Z\n'
        s += '|end=' + ((params['end'].strftime('%Y-%m-%d') + 'T06:59:59Z\n') if params['end'] else '\n')
        s += '}}'
        return s
    
    def OtherLanguage(self):
        import re
        name = re.sub(r' \(.+?\)$', '', self.name)
        return '==In other languages==\n'+\
            '{{OtherLanguages\n'+\
            '|english='+name+'\n'+\
            '|japanese=\n'+\
            '|german=\n'+\
            '|spanishEU=\n'+\
            '|spanishLA=\n'+\
            '|french=\n'+\
            '|italian=\n'+\
            '|chineseTW=\n'+\
            '|portuguese=\n'+\
            '}}'
