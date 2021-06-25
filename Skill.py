#! /usr/bin/env python3

import re
import json
from num2words import num2words

import util
import wikiUtil
from reward import COLOR

SEALS = util.fetchFehData('Common/SRPG/SkillAccessory')
CREATABLE_SEALS = util.fetchFehData('Common/SRPG/SkillAccessoryCreatable')

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
        res.update(SacredSeal(data['id_tag']))
    return res

from sys import argv
if __name__ == '__main__':
    for arg in argv[1:]:
        skills = SacredSeal(arg)
        for name in skills:
            print(name, skills[name])