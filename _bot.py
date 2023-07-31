#! /usr/bin/env python3

from FehWikiBot.Others.Accessory import Accessories
from FehWikiBot.Others.AetherRaids import Structure
from FehWikiBot import Skills, SacredSeals, SacredSealsForge, CaptainSkill
from FehWikiBot.Utility.Units import Heroes
from FehWikiBot.Stages.HO import HeroicOrdeals
from FehWikiBot.Stages.TD import TacticsDrills
from FehWikiBot.Stages.RD import RivalDomains
from FehWikiBot.Stages.MainStories import MainStory
from FehWikiBot.Stages.Paralogues import Paralogue
from FehWikiBot.Events.SS import SeersSnare

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1: exit(0)

    dones = []
    for o in Accessories.fromAssets(argv[1]):
        o.createArticle().export('Accessory ('+argv[1]+')')
    for o in Structure.fromAssets(argv[1]):
        o.loadArticle().update().export('Structure ('+argv[1]+')', create=-1)

    for refSkill in Skills.fromAssets(argv[1], 'Refine'):
        refWep = Skills.get(refSkill.data['id_tag'], 'refine_id')
        Skills.get(refWep.data['pre_refine']).loadArticle(False).update().export('Refine ('+argv[1]+')', create=False)
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
        o.createArticle().export('Captain Skill ('+argv[1]+')', create=True)

    for o in Heroes.fromAssets(argv[1]):
        HeroicOrdeals.get(str(o.data['num_id'])).createArticle().export('Heroic Ordeals ('+argv[1]+')')
    MainStory.exportGroups([o.createArticle() for o in MainStory.fromAssets(argv[1])], 'Story maps ('+argv[1]+')')
    Paralogue.exportGroups([o.createArticle() for o in Paralogue.fromAssets(argv[1])], 'Paralogue maps ('+argv[1]+')')
    for o in TacticsDrills.fromAssets(argv[1]):
        o.createArticle().export('Tactics Drills ('+argv[1]+')')
    for o in RivalDomains.fromAssets(argv[1]):
        o.createArticle().export('Rival Domains ('+argv[1]+')')

    for o in SeersSnare.fromAssets(argv[1]):
        o.createArticle().export('Seer\'s Snare ('+argv[1]+')')
