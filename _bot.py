#! /usr/bin/env python3

from FehWikiBot.Tool.Wiki import Wiki
from FehWikiBot.Others.Accessory import Accessories
from FehWikiBot import Skills, SacredSeals, SacredSealsForge, CaptainSkill

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1: exit(0)

    dones = []
    for o in Accessories.fromAssets(argv[1]):
        o.createArticle().export('Accessory ('+argv[1]+')')
    for o in Skills.fromAssets(argv[1], 'Refine'):
        Skills.get(o.data['id_tag'], 'refine_id').loadArticle().update().export('Refine ('+argv[1]+')', create=False)
    for o in Skills.fromAssets(argv[1], ('Weapon','Assist','Special')):
        o.createArticle().update().export('Skill ('+argv[1]+')', create=True)
    for o in Skills.fromAssets(argv[1], ('A','B','C','Seal')):
        if o.data['id_tag'] in dones: continue
        dones += [d['id_tag'] for d in o._datas]
        o.loadArticle().update().export('Skill ('+argv[1]+')', create=-1)
    for o in SacredSeals.fromAssets(argv[1]):
        if o.data['id_tag'] in dones: continue
        dones += [d['id_tag'] for d in o.skill._datas]
        o.skill.loadArticle().update().export('Sacred Seal ('+argv[1]+')', create=False)
    for o in SacredSealsForge.fromAssets(argv[1]):
        if o.data['id_tag'] in dones: continue
        dones += [d['id_tag'] for d in o.skill._datas]
        o.skill.loadArticle().update().export('Sacred Seal creatable ('+argv[1]+')', create=False)
    for o in CaptainSkill.fromAssets(argv[1]):
        o.createArticle().export('Captain Skill ('+argv[1]+')')
