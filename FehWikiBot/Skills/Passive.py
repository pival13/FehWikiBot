#! /usr/bin/env python3

from .Skills import Skills

class Passive(Skills):
    def __repr__(self) -> str:
        if self._i == -1:
            return '<Passive "None">'
        elif len(self._datas) == 1:
            return '<Passive "' + str(self.name) + '" (' + self.data['id_tag'] + ')>'
        else:
            return '<Passive "' + str(self.name) + '" (' + self.data['id_tag'] + ') (' + ', '.join([o['id_tag'] for o in self._datas]) + ')>'

    def __init__(self):
        super().__init__()
        self._datas = []
        self._i = -1

    @property
    def data(self): return self._datas[self._i] if 0 <= self._i and self._i < len(self._datas) else None

    @data.setter
    def data(self, v):
        from ..PersonalData import BINLZ_ASSETS_DIR_PATH
        from os import listdir
        from ..Utility.Messages import EN
        import re

        def getPrev(prev):
            if prev[0] is None or prev[1] is not None: return []
            for f in self._DATA.values():
                if prev[0] in f: return getPrev(f[prev[0]]['prev_id'])+[f[prev[0]]]
            for f in listdir(BINLZ_ASSETS_DIR_PATH + self._reader._basePath)[::-1]:
                if f[-7:] != '.bin.lz' or not self.load(f[:-7]): continue
                if prev[0] in self._DATA[f[:-7]]: return getPrev(self._DATA[f[:-7]][prev[0]]['prev_id'])+[self._DATA[f[:-7]][prev[0]]]
            return []
        def getNext(id):
            os = []
            for f in self._DATA.values():
                for o in f.values():
                    if o['prev_id'][0] == id and o['prev_id'][1] is None: os.append(o)
            for f in listdir(BINLZ_ASSETS_DIR_PATH + self._reader._basePath)[::-1]:
                if f[-7:] != '.bin.lz' or not self.load(f[:-7]): continue
                for o in self._DATA[f[:-7]].values():
                    if o['prev_id'][0] == id and o['prev_id'][1] is None: os.append(o)
            return os + [o2 for o in os for o2 in getNext(o['id_tag'])]

        s = EN(v['name_id'])
        self._datas = [o for o in getPrev(v['prev_id']) if s.find(re.sub(r'\d*$','',EN(o['name_id']))) == 0]
        self._i = len(self._datas)
        self._datas.append(v)
        s = re.sub(r'\d*$','', EN(self._datas[0]['name_id']) if self._i != 0 else s)
        self._datas += [o for o in getNext(v['id_tag']) if EN(o['name_id']).find(s) == 0]
        return s


    def Infobox(self):
        import re
        from ..Tool.misc import cleanStr
        from ..Utility.Messages import EN

        obj = {
            'name': re.sub(r'\s*\d*$','', EN(self._datas[0]['name_id'])),
            'type': self.type[0] if self.type != 'Attuned' else 'X',
            'exclusive': int(self._datas[0]['exclusive']),
            'canUseWeapon': '{{WeaponList|' + self._datas[0]['wep_equip'] + '}}',
            'canUseMove': '{{MoveList|' + (self._datas[0]['mov_equip'] if self._datas[0]['mov_equip'].count(',') != 3 else 'All') + '}}',
            'properties': '',
        }

        for i,data in enumerate(self._datas):
            i+=1
            obj |= {
                f'{i}name': EN(data['name_id']),
                f'alt{i}name': cleanStr(re.sub(r'\+$',' Plus',EN(data['name_id']).replace('/',' '))),
                f'{i}tagid': data['id_tag'],
                f'{i}exclusive': int(data['exclusive']),
                f'{i}effect': Skills.description(data['desc_id']),
                f'{i}cooldown': data['cooldown_count'] if data['cooldown_count'] != 0 else None,
                f'statModifiers{i}': ','.join(map(str,data['stats'].values())) if max(data['stats'].values()) != 0 else None,
                f'{i}cost': data['sp_cost'],
                f'{i}required': ';'.join([Passive.get(s).name for s in data['prev_id'] if s]),
                f'{i}next': Passive.get(data['next_id']).name if data['next_id'] else '-',
                f'canUseWeapon{i}': '{{WeaponList|' + data['wep_equip'] + '}}',
                f'canUseMove{i}': '{{MoveList|' + (data['mov_equip'] if data['mov_equip'].count(',') != 3 else 'All') + '}}',
                f'{i}promotionTier': data['promotion_tier'] if data['next_id'] else None,
                f'{i}promotionRarity': data['promotion_rarity'] if data['next_id'] else None,
                f'properties{i}': [],
            }
            if data['enemy_only']: obj[f'properties{i}'] += ['enemy_only']
            if data['tt_inherit_base']: obj[f'properties{i}'] += ['random_inherit_base']
            if data['random_allowed'] > 0:
                if data['random_mode'] == 1: obj[f'properties{i}'] += ['random_all']
                elif data['random_mode'] == 2: obj[f'properties{i}'] += ['random_owner']
            if obj[f'alt{i}name'] == obj[f'{i}name']: obj[f'alt{i}name'] = None
            if obj[f'{i}required'] == '': obj[f'{i}required'] = '-'
            obj[f'properties{i}'] = ','.join(obj[f'properties{i}'])

        obj['properties'] = obj['properties1']
        for i,data in enumerate(self._datas):
            if obj[f'{i+1}exclusive'] == obj['exclusive']: obj[f'{i+1}exclusive'] = None
            if obj[f'canUseWeapon{i+1}'] == obj['canUseWeapon']: obj[f'canUseWeapon{i+1}'] = None
            if obj[f'canUseMove{i+1}'] == obj['canUseMove']: obj[f'canUseMove{i+1}'] = None
            if obj[f'properties{i+1}'] == obj['properties']: obj[f'properties{i+1}'] = None
            if i > 0 and obj[f'{i}name'] == obj[f'{i+1}required']: obj[f'{i+1}required'] = None
            if i > 0 and obj[f'{i}next'] == obj[f'{i+1}name']: obj[f'{i}next'] = None
        if obj[f'{len(self._datas)}next'] == '-': obj[f'{len(self._datas)}next'] = None
        if obj['properties'] == '': obj['properties'] = None

        return {k:v for k,v in obj.items() if v is not None}

    def OtherLanguage(self):
        import re
        return re.sub(r'\s*\d+$','', super().OtherLanguage(), flags=re.MULTILINE)

    def createArticle(self):
        if self.data is None: return self
        self.page =  super().Infobox('Passive', self.Infobox()).replace(' Infobox','',1) + '\n'
        self.page += self.Effects() + '\n'
        self.page += '==Notes==\n\n'
        self.page += self.Availability() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '==See also==\n{{See also skills|cond= False }}\n'
        if self.type != 'Seal': self.page += '{{Passives Navbox|'+(self.type if self.type != 'Attuned' else 'X')+'}}'
        else:                   self.page += '{{Seals Navbox}}'
        return self

    def update(self):
        import re
        from num2words import num2words
        from ..Utility.Messages import EN

        prevKey = r'\{\{\s*Passive\s*'
        reEndArg = r'(\{\{([^}]|\}(?!\}))*\}\}|[^{])*?(?=\||\}\})'
        for k, v in self.Infobox().items():
            key = r'\|\s*'+k+r'\s*=\s*(?<!\n)'
            if re.search(key, self.page):
                self.page = re.sub('('+key+')'+reEndArg, f'\\g<1>{v}\n', self.page, 1)
            else:
                self.page = re.sub('('+prevKey+reEndArg+')', f'\\g<1>|{k}={v}\n', self.page, 1)
            prevKey = r'\|\s*'+k+r'\s*'


        if self._datas[0]['@SealForge']:
            if not re.search(r'==\s*Seal acquired from\s*==', self.page):
                content = '==Seal acquired from==\n'
                if self.data['enemy_only']:
                    content += '* This is an enemy exclusive Sacred Seal.\n'
                elif re.match(r'SID_第\d+迷宮の覇者\d+', self.data['id_tag']):
                    content += '===Squad Assault reward===\n* Complete the [['+num2words(re.search(r'\d+', self.data['id_tag'])[0], to='ordinal_num')+' Assault]].\n'
                else:
                    content += '===Tempest Trials reward===\n{{Tempest Trials seal reward}}\n'
                content += '===[[Sacred Seal Forge]]===\n'
                content += '{{SealCosts\n' + \
                    f"|seals={';'.join([EN(o['name_id']) for o in self._datas if o['@SealForge']])}\n" + \
                    f"|badgeColor={self._datas[0]['@SealForge']['required']['badge_type'] if not self._datas[0]['enemy_only'] else '-'}\n" + \
                    '\n'.join([f"|costs{i+1}={o['great_badge']};{o['badge']};{o['sacred_coin']}" for i,o in enumerate([o['@SealForge']['required'] for o in self._datas if o['@SealForge']])]) + \
                    '\n}}'
                self.page = re.sub(r'\n?\n(==\s*In other languages\s*==)', '\n' + content + '\n\\1', self.page)

            for i,o in enumerate([o['@SealForge'] for o in self._datas if o['@SealForge']]):
                if o['creatable'] and re.search(f'costs{i+1}\\s*=\\s*-', self.page):
                    self.page = re.sub(f'(costs{i+1}\\s*=\\s*)[^\\n|}}]+', f"\\g<1>{o['required']['great_badge']};{o['required']['badge']};{o['required']['sacred_coin']}", self.page)
                elif not o['creatable'] and re.search(f'costs{i+1}\\s*=\\s*\\d', self.page):
                    if o['required']['sacred_coin'] == 0:
                        self.page = re.sub(f'(costs{i+1}\\s*=\\s*)[^\\n|}}]+', r'\1-', self.page)
                    else:
                        self.page = re.sub(f'(costs{i+1}\\s*=\\s*)([^\\n|}}]+)', r'\1-<!--\2-->', self.page)

            if self.page.find('{{Seals Navbox}}') == -1:
                self.page += ('\n' if self.page[-1] != '\n' else '') + '{{Seals Navbox}}'

        return self