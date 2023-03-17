#! /usr/bin/env python3

from .Skills import Skills

class Assist(Skills):
    def Infobox(self):
        obj = {
            'tagid': self.data['id_tag'],
            'intID': self.data['id_num'],
            'exclusive': int(self.data['exclusive']),
            'canUseWeapon': '{{WeaponList|' + self.data['wep_equip'] + '}}',
            'canUseMove': '{{MoveList|' + (self.data['mov_equip'] if self.data['mov_equip'].count(',') != 3 else 'All') + '}}',
            'cost': self.data['sp_cost'],
            'range': self.data['range'],
            'cooldown': self.data['cooldown_count'] if self.data['cooldown_count'] != 0 else None,
            'effect': Skills.description(self.data['desc_id']),
            'required': ';'.join([Assist.get(s).name for s in self.data['prev_id'] if s]) if self.data['prev_id'][0] else '-',
            'next': Assist.get(self.data['next_id']).name if self.data['next_id'] else None,
            'promotionRarity': self.data['promotion_rarity'] if self.data['next_id'] else None,
            'promotionTier': self.data['promotion_tier'] if self.data['next_id'] else None,
            'properties': []
        }

        if self.data['enemy_only']: obj['properties'] += ['enemy_only']
        if self.data['tt_inherit_base']: obj['properties'] += ['random_inherit_base']
        if self.data['random_allowed'] > 0:
            if self.data['random_mode'] == 1: obj['properties'] += ['random_all']
            elif self.data['random_mode'] == 2: obj['properties'] += ['random_owner']
        obj['properties'] = ','.join(obj['properties'])

        return super().Infobox('Assist', obj).replace(' Infobox','',1)

    def createArticle(self):
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += '==Notes==\n\n'
        self.page += self.Availability() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '==See also==\n\n'
        self.page += '{{Assists Navbox}}'
        return self