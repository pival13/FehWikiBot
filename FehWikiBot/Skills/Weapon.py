#! /usr/bin/env python3

from .Skills import Skills

class Weapon(Skills):
    @property
    def might(self): return self.data['might']

    @property
    def refine(self): return self.data['refine_type']

    def Infobox(self):
        obj = {
            'tagid': self.data['id_tag'],
            'intID': self.data['num_id'],
            'noImg': None, 'image': None, 'userVersion1': None, 'userVersion2': None, 'userVersion3': None, 'userVersion4': None,
            'exclusive': int(self.exclusive),
            'weaponType': self.data['wep_equip'],
            'canUseMove': self.data['mov_equip'] if self.data['mov_equip'].count(',') != 3 else None,
            'cost': self.data['sp_cost'],
            'might': self.data['might'],
            'range': self.data['range'],
            'cooldown': self.data['cooldown_count'] if self.data['cooldown_count'] != 0 else None,
            'effectiveness': ','.join([v for v in [self.data['wep_effective'], self.data['mov_effective']] if v]),
            'effect': Skills.description(self.data['desc_id']),
            'statModifiers': ','.join(map(lambda v1,v2: str(v1+v2), self.data['stats'].values(), [0,self.data['might'],0,0,0])) if list(self.data['stats'].values()) != [0]*5 else None,
            'required': ';'.join([Weapon.get(s).name for s in self.data['prev_id'] if s]),
            'next': Weapon.get(self.data['next_id']).name if self.data['next_id'] else None,
            'promotionRarity': self.data['promotion_rarity'] if self.data['next_id'] else None,
            'promotionTier': self.data['promotion_tier'] if self.data['next_id'] else None,
            'properties': []
        }

        # Sprites
        if obj['weaponType'] == 'Beast' or (self.data['sprite_wepL'] is None and self.data['sprite_wepR'] is None):
            obj['noImg'] = 1
        elif (self.data['sprite_wepR'] or self.data['sprite_wepL'])[:2] == 'mg':
            from os.path import exists
            from ..PersonalData import WEBP_ASSETS_DIR_PATH
            from PIL import Image
            f = self.data['sprite_wepR'] or self.data['sprite_wepL']
            if exists(WEBP_ASSETS_DIR_PATH+'Common/Wep/'+f+'.ssbp') or Image.open(WEBP_ASSETS_DIR_PATH+'Common/Wep/'+f+'.png').getbbox() is None:
                obj['image'] = f
            else:
                obj['userVersion1'] = 'Closed'
                obj['userVersion2'] = 'Open'
                if exists(WEBP_ASSETS_DIR_PATH+'Common/Wep/'+f+'_up.png'):
                    obj['userVersion3'] = 'Gleam Closed'
                    obj['userVersion4'] = 'Gleam Open'
        elif self.data['sprite_wepL'] is None or self.data['sprite_wepR'] is None:
            obj['image'] = self.data['sprite_wepL'] or self.data['sprite_wepR']
        elif self.data['sprite_wepL'][:6] == 'wep_bw':
            obj['userVersion1'] = 'Bow'
            obj['userVersion2'] = 'Arrow'
        else:
            obj['userVersion1'] = 'Main'
            obj['userVersion2'] = 'Sub'

        # Properties
        if obj['effectiveness'] == '': obj['effectiveness'] = None
        if obj['required'] == '': obj['required'] = '-'
        if self.data['arcane_weapon']: obj['properties'] += ['arcane']
        if self.data['enemy_only']: obj['properties'] += ['enemy_only']
        if self.data['tt_inherit_base']: obj['properties'] += ['random_inherit_base']
        if self.data['random_allowed'] > 0:
            if self.data['random_mode'] == 1: obj['properties'] += ['random_all']
            elif self.data['random_mode'] == 2: obj['properties'] += ['random_owner']
        obj['properties'] = ','.join(obj['properties'])

        return super().Infobox('Weapon', obj)

    def InfoboxRefine(self):
        from ..Tool.globals import WEAPON_CATEGORY, ITEM_KIND, YELLOW_BG, RESET_TEXT
        refines = [self.get(r).data for r in self.data['@refines']]
        listAdd = lambda a,b:list(map(lambda c,d:c+d,a,b))
        listSub = lambda a,b:list(map(lambda c,d:c-d,a,b))

        ret = {}
        if  (    self.exclusive and self.data['wep_equip'] == WEAPON_CATEGORY[0x8000] and sorted([r['refine_type'] for r in refines]) == sorted(['Skill1'])) or \
            (    self.exclusive and self.data['wep_equip'] != WEAPON_CATEGORY[0x8000] and sorted([r['refine_type'] for r in refines]) == sorted(['Skill1','Atk','Spd','Def','Res'])) or \
            (not self.exclusive and self.data['wep_equip'] == WEAPON_CATEGORY[0x8000] and sorted([r['refine_type'] for r in refines]) == sorted(['Skill1', 'Skill2'])) or \
            (not self.exclusive and self.data['wep_equip'] != WEAPON_CATEGORY[0x8000] and sorted([r['refine_type'] for r in refines]) == sorted(['Atk','Spd','Def','Res'])):
                ret['refinePaths'] = 'default'
        else:
            ret['refinePaths'] = ','.join([r['refine_type'] for r in refines])

        ret['refineSP'] = refines[0]['sp_cost']
        costs = {o['kind']:o['count'] for o in refines[0]['@Refinery']['required']}
        if ITEM_KIND[19] in costs: ret['refineMedals'] = costs[ITEM_KIND[19]]
        if ITEM_KIND[17] in costs: ret['refineStones'] = costs[ITEM_KIND[17]]
        if ITEM_KIND[18] in costs: ret['refineDews'] = costs[ITEM_KIND[18]]

        # Changs common to all refines
        ref = Weapon(); ref.data = refines[-1] # Skill1 for exclusive, Res for inheritable
        stats = listAdd(listSub(ref.data['stats'].values(), ref.data['refine_stats'].values()), [0,ref.might,0,0,0])
        if ref.data['desc_id'] != self.data['desc_id']:
            ret['upgradedEffect'] = Skills.description(ref.data['desc_id'])
        if ref.might != self.might:
            ret['upgradedMight'] = ref.might
        if stats != listAdd(self.data['stats'].values(), [0,self.might,0,0,0]):
            ret['upgradedStatModifiers'] = ','.join(map(str,stats))
        if ref.data['cooldown_count'] != self.data['cooldown_count']:
            ret['upgradedCooldown'] = ref.data['cooldown_count']
        if ref.data['wep_effective'] != self.data['wep_effective'] or ref.data['mov_effective'] != self.data['mov_effective']:
            ret['upgradedEffectiveness'] = ','.join([s for s in [ref.data['wep_effective']]+[ref.data['mov_effective']] if s])

        # Change of a single refine
        for r in refines:
            TAGS = {'Atk':'ATK', 'Spd':'AGI', 'Def':'DEF', 'Res':'RES', 'Skill1':'神', 'Skill2':'幻'}
            STATS = {
                'Atk':   ([5,2,0,0,0], [2,1,0,0,0]),
                'Spd':   ([5,0,3,0,0], [2,0,2,0,0]),
                'Def':   ([5,0,0,4,0], [2,0,0,3,0]),
                'Res':   ([5,0,0,0,4], [2,0,0,0,3]),
                'Skill': ([3,0,0,0,0], [0,0,0,0,0])
            }
            # TODO: icon for staffs
            if r['id_tag'][r['id_tag'].rindex('_')+1:] != TAGS[r['refine_type']] and not (self.exclusive and r['refine_type'] == 'Skill1' and r['id_tag'][:-2] != '_一'):
                print(f'{YELLOW_BG}Unusual refine{RESET_TEXT}: ' + self.name)
                ret['tagidExtra'+r['refine_type']] = r['id_tag'][r['id_tag'].rindex('_')+1:]
            deltaMight = ref.might - self.data['might']
            if listSub(r['refine_stats'].values(), [0,deltaMight,0,0,0]) != STATS[r['refine_type'][:5]][r['range']-1]:
                ret['refineStats'+r['refine_type']] = ','.join(map(str,listSub(r['refine_stats'].values(), [0,deltaMight,0,0,0])))

        # Changs of Skill1
        if self.exclusive:
            refSkill = Skills.get(ref.data['refine_id'])
            ret['effectSkill1'] = Skills.description(refSkill.data['desc_id'])
            if list(refSkill.data['stats'].values()) != [0]*5:
                # != listAdd(self.data['stats'].values(), [0,self.might,0,0,0]):
                ret['statModifiersSkill1'] = ','.join(map(str,listAdd(listAdd(ref.data['stats'].values(), refSkill.data['stats'].values()), [0,ref.might,0,0,0])))
            if ref.data['cooldown_count'] != (ret['upgradedCooldown'] if 'upgradedCooldown' in ret else self.data['cooldown_count']):
                ret['cooldownSkill1'] = ref['cooldown_count']
            # TODO Effectiveness
            # if ref.data['wep_effective'] != self.data['wep_effective'] or ref.data['mov_effective'] != self.data['mov_effective']:
            #     ret['effectivenessSkill1'] = ','.join([s for s in ref.data['wep_effective']+ref.data['mov_effective'] if s != ''])

        return ret

    def createArticle(self):
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += '==Notes==\n\n'
        self.page += self.Availability() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '==See also==\n{{See also skills|cond= False }}\n'
        self.page += '{{Weapons Navbox}}'
        return self

    def update(self):
        import re
        if self.data is None or self.data['@refines'] == [] or self.page == '': return self

        pattern = r'(Weapon Infobox(\{\{.*?\}\}|.)*?)(?=\|\s*properties|\}\})'
        for key, value in self.InfoboxRefine().items():
            if re.search(f'\\|\\s*{key}\\s*=', self.page): continue
            self.page = re.sub(pattern, f"\\1|{key}={value}\n", self.page, flags=re.DOTALL)
            pattern = f'(\\|\\s*{key}\\s*=[^|}}]*)'

        if not re.search(r'Weapon Upgrade List', self.page):
            s =  '==Upgrades==\n'
            s += '{{Weapon Upgrade List}}\n'
            if self.exclusive:
                s += '===Notes===\n\n'
            self.page = re.sub(r'(==\s*Notes\s*==.*?\n)(?===[^=])', '\\1'+s, self.page, flags=re.DOTALL)

        return self
