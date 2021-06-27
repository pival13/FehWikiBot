#! /usr/bin/env python3

import re
import json
from num2words import num2words

import util
import wikiUtil
from reward import COLOR, MOVE

SEALS = util.fetchFehData('Common/SRPG/SkillAccessory')
CREATABLE_SEALS = util.fetchFehData('Common/SRPG/SkillAccessoryCreatable')
_REFINES = util.fetchFehData('Common/SRPG/WeaponRefine', None)
REFINES = {}
for refine in _REFINES:
    REFINES[refine['orig']] =  (REFINES[refine['orig']] if refine['orig'] in REFINES else []) + [refine]
SKILLS = util.fetchFehData('Common/SRPG/Skill')

WEAPON_CATEGORY = {
    0b111111111111111111111111: "All",
    0b000000000000000000000000: "None",

    0b111111110000000000000111: "Close",
    0b000000001111111111111000: "Ranged",

    0b111100000000011111111111: "Physical",
    0b000011111111100000000000: "Magical",

    0b000000000000011111111000: "Missile",

    0b000100010000100010001001: "Red",
    0b001000100001000100010010: "Blue",
    0b010001000010001000100100: "Green",
    0b100010001100010001000000: "Colorless",

    0b000000000000000000000111: "Melee",
    0b000000000000000001111000: "Bow",
    0b000000000000011110000000: "Dagger",
    0b000000000111100000000000: "Magic",
    0b000011110000000000000000: "Dragonstone",
    0b111100000000000000000000: "Beast",

    0b000000000000000000000001: "Sword",
    0b000000000000000000000010: "Lance",
    0b000000000000000000000100: "Axe",
    0b000000000000000000001000: "Red Bow",
    0b000000000000000000010000: "Blue Bow",
    0b000000000000000000100000: "Green Bow",
    0b000000000000000001000000: "Colorless Bow",
    0b000000000000000010000000: "Red Dagger",
    0b000000000000000100000000: "Blue Dagger",
    0b000000000000001000000000: "Green Dagger",
    0b000000000000010000000000: "Colorless Dagger",
    0b000000000000100000000000: "Red Tome",
    0b000000000001000000000000: "Blue Tome",
    0b000000000010000000000000: "Green Tome",
    0b000000000100000000000000: "Colorless Tome",
    0b000000001000000000000000: "Colorless Staff",
    0b000000010000000000000000: "Red Dragonstone",
    0b000000100000000000000000: "Blue Dragonstone",
    0b000001000000000000000000: "Green Dragonstone",
    0b000010000000000000000000: "Colorless Dragonstone",
    0b000100000000000000000000: "Red Beast",
    0b001000000000000000000000: "Blue Beast",
    0b010000000000000000000000: "Green Beast",
    0b100000000000000000000000: "Colorless Beast",
}

PATHS = { 1: 'Skill1', 2: 'Skill2', 101: 'ATK', 102: 'SPD', 103: 'DEF', 104: 'RES' }

def refinePath(baseSkill, refSkill, refData):
    STATS_PATH = {
        '': ([3,0,0,0,0], [0,0,0,0,0]),
        'ATK': ([5,2,0,0,0], [2,1,0,0,0]),
        'SPD': ([5,0,3,0,0], [2,0,2,0,0]),
        'DEF': ([5,0,0,4,0], [2,0,0,3,0]),
        'RES': ([5,0,0,0,4], [2,0,0,0,3])
    }
    ICONS = {'神': 'Wrathful Staff W.png', '幻': 'Dazzling Staff W.png'}
    path = PATHS[refSkill['refine_sort_id']] if refSkill['refine_sort_id'] in PATHS else 'Unknow'
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
    paths = [PATHS[ref['refine_sort_id']] if ref['refine_sort_id'] in PATHS else 'Unknow' for ref in refSkills]
    if any([path == 'Unknow' for path in paths]): print(util.TODO + util.getName(baseSkill['id_tag']) + ": Unknow refine path")
    if  (baseSkill['exclusive'] and baseSkill['wep_equip'] == 0b000000001000000000000000 and paths == ['Skill1']) or \
        (baseSkill['exclusive'] and baseSkill['wep_equip'] != 0b000000001000000000000000 and paths == ['ATK','SPD','DEF','RES','Skill1']) or \
        (not baseSkill['exclusive'] and baseSkill['wep_equip'] == 0b000000001000000000000000 and paths == ['Skill1', 'Skill2']) or \
        (not baseSkill['exclusive'] and baseSkill['wep_equip'] != 0b000000001000000000000000 and paths == ['ATK','SPD','DEF','RES']):
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
    for key, val in enumerate(MOVE):
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
        pattern = r'(Weapon Infobox.*?)(?=\|\s*properties|\}\})' if i == 0 else f'(\\|\\s*{list(refData.keys())[i-1]}\\s*=[^|}}]*)'
        value = ','.join(map(str, value)) if isinstance(value, list) else str(value).replace('\n\n', '<br /><br />').replace('\n',' ')
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

from sys import argv
if __name__ == '__main__':
    for arg in argv[1:]:
        pass
        #skills = SacredSeal(arg)
        #for name in skills:
        #    print(name, skills[name])
        #wikiUtil.exportSeveralPages(SealsFrom(arg), 'Bot: Sacred Seal', True)
        #wikiUtil.exportSeveralPages(RefinesFrom(arg), 'Bot: Refine', True)