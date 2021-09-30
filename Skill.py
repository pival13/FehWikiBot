#! /usr/bin/env python3

import re
from num2words import num2words
from os.path import exists

import util
import wikiUtil
from mapUtil import InOtherLanguage
from globals import SKILLS, SEALS, CREATABLE_SEALS, REFINES, COLOR, MOVE_TYPE, WEAPON_CATEGORY, WEAPON_MASK, REFINE_TYPE

def wepMaskToList(ref):
    l = []
    for mask, name in WEAPON_CATEGORY.items():
        if mask != 0 and (mask & ref) == mask:
            ref ^= mask
            l += [name.replace('stone','')]
    return l

def refinePath(baseSkill, refSkill, refData):
    STATS_PATH = {
        '': ([3,0,0,0,0], [0,0,0,0,0]),
        'Atk': ([5,2,0,0,0], [2,1,0,0,0]),
        'Spd': ([5,0,3,0,0], [2,0,2,0,0]),
        'Def': ([5,0,0,4,0], [2,0,0,3,0]),
        'Res': ([5,0,0,0,4], [2,0,0,0,3])
    }
    ICONS = {'神': 'Wrathful Staff W.png', '幻': 'Dazzling Staff W.png'}
    path = REFINE_TYPE[refSkill['refine_sort_id']] if refSkill['refine_sort_id'] in REFINE_TYPE else 'Unknow'
    refine = SKILLS[refSkill['refine_id']] if refSkill['refine_id'] else None

    theoricRefStats = [a for a in STATS_PATH[path if path in STATS_PATH else ''][refSkill['range']-1]]
    if 'upgradedMight' in refData: theoricRefStats[1] += refData['upgradedMight'] - baseSkill['might']

    return {
        'tagidExtra'+path: refSkill['id_tag'][refSkill['id_tag'].rindex('_')+1:] if refine else None,
        'effect'+path: util.getName(refine['desc_id']) if refine else None,
        'icon'+path: ICONS[refSkill['id_tag'][refSkill['id_tag'].rindex('_')+1:]] if refine and refSkill['id_tag'][refSkill['id_tag'].rindex('_')+1:] in ICONS else (util.cleanStr(util.getName(baseSkill['id_tag'])) + ' W.png' if refine else None),
        'refineStats'+path: list(refSkill['refine_stats'].values()) if list(refSkill['refine_stats'].values()) != theoricRefStats else None,
        'statModifiers'+path: list(map(lambda k, v: refSkill['stats'][k] + refine['stats'][k] + v, ['hp','atk','spd','def','res'], [0,refSkill['might'],0,0,0])) if refine and list(refine['stats'].values()) != [0,0,0,0,0] else None,
        'cooldown'+path: refine['cooldown_count'] if refine and refine['cooldown_count'] != (refData['upgradedCooldown'] if 'upgradedCooldown' in refData else baseSkill['cooldown_count']) else None,
        #'effectiveness'+path: , #TODO Refine effectiveness
    }

def refinePaths(baseSkill, refSkills, refCosts):
    ret = {}
    paths = [REFINE_TYPE[ref['refine_sort_id']] if ref['refine_sort_id'] in REFINE_TYPE else 'Unknow' for ref in refSkills]
    if any([path == 'Unknow' for path in paths]): print(util.TODO + util.getName(baseSkill['id_tag']) + ": Unknow refine path")
    if  (baseSkill['exclusive'] and baseSkill['wep_equip'] == WEAPON_MASK['Colorless Staff'] and paths == ['Skill1']) or \
        (baseSkill['exclusive'] and baseSkill['wep_equip'] != WEAPON_MASK['Colorless Staff'] and paths == ['Atk','Spd','Def','Res','Skill1']) or \
        (not baseSkill['exclusive'] and baseSkill['wep_equip'] == WEAPON_MASK['Colorless Staff'] and paths == ['Skill1', 'Skill2']) or \
        (not baseSkill['exclusive'] and baseSkill['wep_equip'] != WEAPON_MASK['Colorless Staff'] and paths == ['Atk','Spd','Def','Res']):
            ret['refinePaths'] = 'default'
    else:
        ret['refinePaths'] = ','.join(paths)

    costs = {
        'refineSP': refSkills[0]['sp_cost'],
        'refineMedals': max([cost['count'] for cost in refCosts[0]['use'] if cost['res_type'] == 1] + [0]),
        'refineStones': max([cost['count'] for cost in refCosts[0]['use'] if cost['res_type'] == 2] + [0]),
        'refineDews': max([cost['count'] for cost in refCosts[0]['use'] if cost['res_type'] == 3] + [0])
    }
    for key, val in costs.items():
        if val != 0: ret[key] = val

    effectiveness = refSkills[0]['wep_effective']
    effective = []
    for key, val in WEAPON_CATEGORY.items():
        if (effectiveness & key) == key:
            effective += [val] if (baseSkill['wep_effective'] & key) != key else []
            effectiveness ^= key
    effectiveness = refSkills[0]['mov_effective']
    for key, val in enumerate(MOVE_TYPE):
        if (effectiveness & (1<<key)) == (1<<key):
            effective += [val] if (baseSkill['mov_effective'] & (1<<key)) != (1<<key) else []
    stats = list(map(lambda k, v: refSkills[0]['stats'][k] - refSkills[0]['refine_stats'][k] + v, ['hp','atk','spd','def','res'], [0,refSkills[0]['might'],0,0,0]))
    upgraded = {
        'upgradedEffect': util.getName(refSkills[0]['desc_id']) if refSkills[0]['desc_id'] != baseSkill['desc_id'] else None,
        'upgradedMight': refSkills[-1]['might'] if refSkills[-1]['might'] != baseSkill['might'] else None,
        'upgradedStatModifiers': stats if stats != list(map(lambda a,b: a+b, baseSkill['stats'].values(), [0,baseSkill['might'],0,0,0])) else None,
        'upgradedCooldown': refSkills[0]['cooldown_count'] if refSkills[0]['cooldown_count'] != baseSkill['cooldown_count'] else None,
        'upgradedEffectiveness': ','.join(effective) if effective != [] else None
    }
    for key, val in upgraded.items():
        if val != None: ret[key] = val
    
    for refSkill in refSkills:
        for k,v in refinePath(baseSkill, refSkill, ret).items():
            if v: ret[k] = v

    return ret

def Refine(skill_id):
    if skill_id in REFINES:
        refines = REFINES[skill_id]
        baseSkill = SKILLS[skill_id]
    elif skill_id + '＋' in REFINES:
        refines = REFINES[skill_id+'＋']
        baseSkill = SKILLS[skill_id+'＋']
    else:
        return {}

    name = util.getName(baseSkill['id_tag']).replace('/', ' ')
    page = wikiUtil.getPageContent(name)[name]
    refData = refinePaths(baseSkill, [SKILLS[ref['refined']] for ref in refines], refines)

    for i, (key, value) in enumerate(refData.items()):
        if re.search(f'\\|\\s*{key}\\s*=', page):
            continue
        pattern = r'(Weapon Infobox(\{\{.*?\}\}|.)*?)(?=\|\s*properties|\}\})' if i == 0 else f'(\\|\\s*{list(refData.keys())[i-1]}\\s*=[^|}}]*)'
        value = ','.join(map(str, value)) if isinstance(value, list) else str(value).replace('\n\n', '<br /><br />').replace('】\n', '】<br />').replace('\n',' ').replace('$a', '')
        page = re.sub(pattern, f"\\1|{key}={value}\n", page, flags=re.DOTALL)

    if not re.search(r'\{\{\s*Weapon Upgrade List\s*\}\}', page):
        page = re.sub(r'(==\s*Notes\s*==.*?)(?=\n==[^=])', '\\1\n==Upgrades==\n{{Weapon Upgrade List}}\n===Notes===\n', page, flags=re.DOTALL)

    return {name: page}

def RefinesFrom(tag_id: str):
    datas = util.readFehData('Common/SRPG/WeaponRefine/' + tag_id + '.json')
    done = []
    res = {}
    for data in datas:
        if not data['orig'] in done:
            try:
                res.update(Refine(data['orig']))
                done += [data['orig']]
            except:
                print(util.TODO + 'Error with Refine ' + util.getName(data['orig']))
    return res

def SacredSeal(skill_id):
    if skill_id in SEALS:
        seals = [SEALS[skill_id]]
    elif skill_id + '1' in SEALS:
        seals = [SEALS[skill_id+'1']]
    else:
        return {}
    while seals[0]['prev_seal']:
        seals = [SEALS[seals[0]['prev_seal']]] + seals
    while seals[-1]['next_seal']:
        seals += [SEALS[seals[-1]['next_seal']]]

    pageName = re.sub(r'\s*\d*$', '', util.getName(seals[0]['id_tag']).replace('/', ' '))
    try: page = wikiUtil.getPageContent(pageName)[pageName]
    except: print(util.TODO + 'New Sacred Seal: ' + pageName); return {}

    if not re.search(r'==\s*Seal acquired from\s*==', page):
        content = '==Seal acquired from==\n'
        if re.search(r'第\d+迷宮の覇者\d*', seals[0]['id_tag']):
            page = re.sub(r'(?s)==\s*Notes\s*==.*(==\s*In other languages\s*==)', '\\1', page)
            content += '===Squad Assault reward===\n* Complete the [['+num2words(re.search(r'\d+', seals[0]['id_tag'])[0], to='ordinal_num')+' Assault]].\n'
        else:
            content += '===Tempest Trials reward===\n{{Tempest Trials seal reward}}\n'
        content += '===[[Sacred Seal Forge]]===\n'
        content += '{{SealCosts\n' + \
            f"|seals={','.join([util.getName(seal['id_tag']) for seal in seals])}\n" + \
            f"|badgeColor={COLOR[seals[0]['ss_badge_type']+1]}\n" + \
            '\n'.join([f"|costs{i+1}={seal['ss_great_badge']};{seal['ss_badge']};{seal['ss_coin']}" for i, seal in enumerate(seals)]) + \
            "\n}}"
        page = re.sub(r'\n*(==\s*In other languages\s*==)', '\n' + content + r'\n\1', page)

    if seals[0]['id_tag'] in CREATABLE_SEALS:
        if page.find('costs1=-<!--') != -1:
            page = re.sub(r'costs1=-<!--([^\n|]+)-->', r'costs1=\1', page)
    else:
        page = re.sub(r'costs1=([\d;]+)', r'costs1=-<!--\1-->', page)

    if page.find('{{Seals Navbox}}') == -1:
        if page.find('{{Passives Navbox') != -1:
            page = page.replace('{{Passives Navbox', '{{Seals Navbox}}\n{{Passives Navbox')
        else:
            page += '{{Seals Navbox}}'

    return {pageName: page}

def SealsFrom(tag_id: str):
    datas = util.readFehData('Common/SRPG/SkillAccessory/' + tag_id + '.json')
    datas += util.readFehData('Common/SRPG/SkillAccessoryCreatable/' + tag_id + '.json')
    res = {}
    for data in datas:
        try:
            res.update(SacredSeal(data['id_tag']))
        except:
            print(util.TODO + 'Error with Sacred Seal ' + util.getName(data['id_tag']))
    return res


def buildInfobox(name, obj):
    s = '{{' + name + '\n'
    forces = []
    if '__force' in obj:
        forces = obj['__force']
        obj['__force'] = None
    for k, v in obj.items():
        s += f"|{k}={','.join(v) if isinstance(v,list) else v}\n" if v or k in forces else ''
    s += '}}'
    return s

def Notes():
    return "*"

def Weapon(skill):
    obj = {
        'tagid': skill['id_tag'], 'intID': skill['id_num'],
        'noImg': None, 'image': None, 'userVersion1': None, 'userVersion2': None,
        'exclusive': 1 if skill['exclusive'] else 0,
        'weaponType': WEAPON_CATEGORY[skill['wep_equip']],
        'canUseMove': [move for i, move in enumerate(MOVE_TYPE) if skill['mov_equip'] & (1 << i)] if skill['mov_equip'] != 0b1111 else None,
        'cost': skill['sp_cost'],
        'might': skill['might'], 'range':skill['range'],
        'cooldown': skill['cooldown_count'] if skill['cooldown_count'] != 0 else None,
        'effectiveness': [],
        'effect': (util.DATA[skill['desc_id']] or "").replace('\n\n', '<br /><br />').replace('】\n', '】<br />').replace('\n',' ').replace('$a',''),
        'statModifiers': list(map(lambda k, v: str(skill['stats'][k] + v), ['hp','atk','spd','def','res'], [0,skill['might'],0,0,0])),
        'required': [util.getName(s) for s in skill['prerequisites'] if s] or ['-'],
        'next': util.getName(skill['next_skill']),
        'promotionRarity': skill['promotion_rarity'], 'promotionTier': skill['promotion_tier'],
        'properties': [],
        '__force': ['exclusive', 'effect', 'properties']
    }

    sprites = [s for s in skill['sprites'][:2] if s]
    if len(sprites) == 0:
        obj['noImg'] = 1
    elif len(sprites) == 1 and (sprites[0][4:6] != 'mg' or exists(util.WEBP_ASSETS_DIR_PATH + 'Common/Wep/' + sprites[0] + '.ssbp')):
        obj['image'] = sprites[0]
    else:
        obj['userVersion1'] = 'Closed' if len(sprites) == 1 else 'Bow' if sprites[0][4:6] == 'bw' else 'Main'
        obj['userVersion2'] = 'Open' if len(sprites) == 1 else 'Arrow' if sprites[0][4:6] == 'bw' else 'Sub'

    obj['effectiveness'] += wepMaskToList(skill['wep_effective'])
    for i, name in enumerate(MOVE_TYPE):
        if skill['mov_effective'] & (1 << i) != 0:
            obj['effectiveness'] += [name]

    if skill['enemy_only']: obj['properties'] += ['enemy_only']
    if skill['tt_inherit_base']: obj['properties'] += ['random_inherit_base']
    if skill['random_allowed'] > 0:
        if skill['random_mode'] == 1: obj['properties'] += ['random_all']
        elif skill['random_mode'] == 2: obj['properties'] += ['random_owner']
    obj['properties'] = ','.join(obj['properties'])

    return obj

def Special(skill):
    obj = {
        'tagid': skill['id_tag'], 'intID': skill['id_num'],
        'exclusive': 1 if skill['exclusive'] else 0,
        'canUseWeapon': f"{{{{WeaponList|{'exclude=Staff' if skill['wep_equip'] == WEAPON_MASK['All']^WEAPON_MASK['Colorless Staff'] else ','.join(wepMaskToList(skill['wep_equip']))}}}}}",
        'canUseMove': f"{{{{MoveList|{','.join([move for i, move in enumerate(MOVE_TYPE) if skill['mov_equip'] & (1 << i)]) if skill['mov_equip'] != 0b1111 else 'All'}}}}}",
        'cost': skill['sp_cost'],
        'cooldown': skill['cooldown_count'] if skill['cooldown_count'] != 0 else None,
        'effect': (util.DATA[skill['desc_id']] or "").replace('\n\n', '<br /><br />').replace('】\n', '】<br />').replace('\n',' ').replace('$a',''),
        'required': [util.getName(s) for s in skill['prerequisites'] if s] or ['-'],
        'next': util.getName(skill['next_skill']),
        'promotionRarity': skill['promotion_rarity'], 'promotionTier': skill['promotion_tier'],
        'properties': [],
        '__force': ['exclusive', 'effect', 'properties']
    }

    if skill['enemy_only']: obj['properties'] += ['enemy_only']
    if skill['tt_inherit_base']: obj['properties'] += ['random_inherit_base']
    if skill['random_allowed'] > 0:
        if skill['random_mode'] == 1: obj['properties'] += ['random_all']
        elif skill['random_mode'] == 2: obj['properties'] += ['random_owner']
    obj['properties'] = ','.join(obj['properties'])

    return obj

def Assist(skill_id):
    """{{Assist
    |tagid=
    |name=
    |range=
    |effect=
    |cost=
    |exclusive=
    |canUseMove=
    |canUseWeapon=
    |next=
    |required=
    |properties=
    }}"""

def Passive(skill):
    obj = {
        'type': ['A','B','C','S'][skill['category']-3],
        '%dname': util.getName(skill['name_id']),
        'alt%dname': util.cleanStr(util.getName(skill['name_id']).replace('/',' ')),
        '%dtagid': skill['id_tag'],
        '%dexclusive': 1 if skill['exclusive'] else 0,
        'canUseWeapon%d': f"{{{{WeaponList|{'exclude=Staff' if skill['wep_equip'] == WEAPON_MASK['All']^WEAPON_MASK['Colorless Staff'] else ','.join(wepMaskToList(skill['wep_equip']))}}}}}",
        'canUseMove%d': f"{{{{MoveList|{'All' if skill['mov_equip'] == 0b1111 else ','.join([move for i, move in enumerate(MOVE_TYPE) if skill['mov_equip'] & (1 << i)])}}}}}",
        '%dcost': skill['sp_cost'],
        '%dcooldown': skill['cooldown_count'],
        '%deffect': util.DATA[skill['desc_id']].replace('\n\n', '<br /><br />').replace('】\n', '】<br />').replace('\n',' ').replace('$a',''),
        'statModifiers%d': list(map(lambda k, v: str(skill['stats'][k] + v), ['hp','atk','spd','def','res'], [0,skill['might'],0,0,0])) if max(skill['stats'].values()) != 0 else None,
        '%drequired': [util.getName(s) for s in skill['prerequisites'] if s] or ['-'],
        '%dnext': util.getName(skill['next_skill']) or '-',
        '%dpromotionRarity': skill['promotion_rarity'],
        '%dpromotionTier': skill['promotion_tier'],
        'properties%d': [],
    }
    if skill['enemy_only']: obj['properties%d'] += ['enemy_only']
    if skill['tt_inherit_base']: obj['properties%d'] += ['random_inherit_base']
    if skill['random_allowed'] > 0:
        if skill['random_mode'] == 1: obj['properties%d'] += ['random_all']
        elif skill['random_mode'] == 2: obj['properties%d'] += ['random_owner']
    if obj['alt%dname'] == obj['%dname']: obj['alt%dname'] = None
    return obj

def createPassivePage(skills):
    obj = {
        'type': skills[0]['type'],
        'name': re.sub(r'\s*\d+$','',skills[0]['%dname']),
        '__force': ['exclusive']
    }
    for k in ['%dexclusive', 'canUseWeapon%d', 'canUseMove%d', 'properties%d']:
        if len([1 for skill in skills if skill[k] != skills[0][k]]) == 0:
            obj[k.replace('%d','')] = skills[0][k]
            for skill in skills: skill[k] = None
    for i, skill in enumerate(skills):
        for k in skill:
            obj[k.replace('%d',str(i+1))] = skill[k]
    for i in range(1, len(skills)+1):
        if f"{i-1}name" in obj and len(obj[f'{i}required']) == 1 and obj[f'{i-1}name'] == obj[f'{i}required'][0]:
            obj[f'{i}required'] = []
        if (f"{i+1}name" in obj and obj[f'{i+1}name'] == obj[f'{i}next']) or (not f"{i+1}name" in obj and obj[f'{i}next'] == '-'):
            obj[f'{i}next'] = None

    s = "{{SkillPage Tabs}}"
    s += buildInfobox('Passive', obj) + '\n'
    s += "==Notes==\n" + Notes() + "\n"
    s += "==List of owners==\n{{Skill Hero List}}\n"
    s += "==Trivia==\n* \n"
    s += re.sub(r'\s*\d+$','', InOtherLanguage('M'+skills[0]['%dtagid'], skills[0]['alt%dname']), flags=re.MULTILINE)
    s += "==See also==\n* \n"
    s += ("{{Passives Navbox|" + skills[0]['type'] + '}}') if skills[0]['type'] != 'S' else '{{Seals Navbox}}'
    return s

def updatePassivePage(page, skills):
    obj = {
        'type': skills[0]['type'],
        'name': re.sub(r'\s*\d+$','',skills[0]['%dname'])
    }
    for k in ['%dexclusive', 'canUseWeapon%d', 'canUseMove%d', 'properties%d']:
        if len([1 for skill in skills if skill[k] != skills[0][k]]) == 0:
            obj[k.replace('%d','')] = skills[0][k]
            for skill in skills: skill[k] = None
    for i, skill in enumerate(skills):
        for k in skill:
            obj[k.replace('%d',str(i+1))] = skill[k]
    for i in range(1, len(skills)+1):
        if f"{i-1}name" in obj and len(obj[f'{i}required']) == 1 and obj[f'{i-1}name'] == obj[f'{i}required'][0]:
            obj[f'{i}required'] = []
        if (f"{i+1}name" in obj and obj[f'{i+1}name'] == obj[f'{i}next']) or (not f"{i+1}name" in obj and obj[f'{i}next'] == '-'):
            obj[f'{i}next'] = None

    prevKey = r'\{\{\s*Passive\s*'
    reEndArg = r'(\{\{([^}]|\}(?!\}))*\}\}|[^{])*?(?=\|\s*\w+\s*=|\}\})'
    for k, v in obj.items():
        if k == '__force': continue
        key = '\\|\\s*'+k+'\\s*=\\s*'
        if re.search(key, page):
            if k[1:] == 'effect':
                pass
            elif v:
                page = re.sub('('+key+r')'+reEndArg, f"\\g<1>{v if not isinstance(v, list) else ','.join(v)}\n", page)
            else:
                page = re.sub(key+reEndArg, '', page)
        elif v or ('__force' in obj and k in obj['__force']):
            page = re.sub('('+prevKey+reEndArg+')', f"\\g<1>|{k}={v if not isinstance(v, list) else ','.join(v)}\n", page)
        else:
            continue
        prevKey = key
    return page

def PassivePage(skills):
    passives = list(map(Passive, skills))
    pageName = re.sub(r' (\d+|I|II|III|IV)$', '', passives[0]['%dname']).replace('/', ' ')
    page = wikiUtil.getPageContent(pageName)[pageName]
    if page:
        page = updatePassivePage(page, passives)
    else:
        page = createPassivePage(passives)
    return {pageName: page}

def ActivePage(skill):
    NAVBOX = {0:'{{Weapons Navbox}}',1:'{{Assists Navbox}}',2:'{{Specials Navbox}}'}

    s = ""
    s += "{{SkillPage Tabs}}"
    if skill['category'] == 0:
        s += buildInfobox('Weapon Infobox', Weapon(skill)) + '\n'
    elif skill['category'] == 2:
        s += buildInfobox('Special', Special(skill)) + '\n'
    s += "==Notes==\n" + Notes() + "\n"
    s += "==List of owners==\n{{Skill Hero List}}\n"
    s += "==Trivia==\n* \n"
    s += InOtherLanguage(skill['name_id'])
    s += "==See also==\n* \n"
    s += NAVBOX[skill['category']]
    return s

def Skill(tag_id):
    if tag_id in SKILLS and SKILLS[tag_id]['category'] < 3:
        skill = SKILLS[tag_id]
        if skill['category'] in [0, 2]:#, 1]:
            return {util.getName(tag_id): ActivePage(skill)}
        elif skill['category'] in [1,2]:
            print(util.TODO + 'Unsupported skill: ' + util.getName(skill['name_id']))
    elif tag_id in SKILLS and not tag_id[-1] in '12345':
        skill = SKILLS[tag_id]
        if skill['category'] in [3,4,5,6]:
            return PassivePage([SKILLS[tag_id]])
        else:
            print(util.TODO + f"Unknow skill: {util.getName(tag_id)} ({tag_id})")
            return {}
    else:
        if tag_id in SKILLS and tag_id[-1] in '12345':
            tag_id = tag_id[:-1]
        i = 1
        skills = []
        while f"{tag_id}{i}" in SKILLS:
            skills += [SKILLS[f"{tag_id}{i}"]]
            i += 1
        if len(skills) == 0:
            return {}
        else:
            return PassivePage(skills)

def SkillsFrom(tag_id: str):
    datas = util.readFehData('Common/SRPG/Skill/' + tag_id + '.json')
    res = {}
    for data in datas:
        if data['id_tag'] != data['name_id'][1:] or util.getName(data['name_id']) == data['name_id']:
            print('Skipping ' + util.getName(data['id_tag']))
        else:
            name = re.sub(r' (%d+|I|II|III|IV|V)$', '', util.getName(data['name_id']))
            if not name in res:
                try:
                    res.update(Skill(re.sub(r'%d*$', '', data['id_tag'])))
                except:
                    print(util.TODO + f"Error with skill: {util.getName(name)} ({name})")
    return res

from sys import argv
if __name__ == '__main__':
    for arg in argv[1:]:
        try:
            if re.match(r'SID_\S+', arg):
                print(Skill(arg))
            elif re.match(r'\d+_\w+', arg):
                print(SkillsFrom(arg))
            else:
                print('Invalid argument:', arg)
        except:
            print('Error with ' + arg)