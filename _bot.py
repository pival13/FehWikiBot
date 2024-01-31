#! /usr/bin/env python3

from FehWikiBot.Others.Accessory import Accessories
from FehWikiBot.Others.AetherRaids import Structure
from FehWikiBot.Utility.Units import Heroes
from FehWikiBot.Skills import Skills, SacredSeals, SacredSealsForge, CaptainSkill
from FehWikiBot.Stages import MainStory, Paralogue, TacticsDrills, HeroicOrdeals, HeroBattle, LimitedHeroBattle, RivalDomains, unsupportedSpecialMaps
from FehWikiBot.Events import TempestTrials, ForgingBonds, HallOfForms, MjolnirsStrike, SeersSnare, AffinityAutoBattles
from FehWikiBot.Tool.globals import TODO

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
    for o in Skills.fromAssets(argv[1], ('A','B','C','Seal','Attuned')):
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
    for o in HeroBattle.fromAssets(argv[1]):
        o.createArticle().export(o.category + ' ('+argv[1]+')')
    for o in RivalDomains.fromAssets(argv[1]):
        o.createArticle().export('Rival Domains ('+argv[1]+')')
    for o in LimitedHeroBattle.fromAssets(argv[1]):
        o.loadArticle().update().export(o.category + ' ('+argv[1]+')', create=False)
    for o in HeroBattle.upcomingRevivals():
        o.loadArticle(False).update().export('Revival ('+argv[1]+')', create=False)
    if unsupportedSpecialMaps(argv[1]) != []:
        print(TODO + 'Unsupported Special maps: ' + str(unsupportedSpecialMaps(argv[1])))

    for o in TempestTrials.fromAssets(argv[1]):
        o.createArticle().export('Tempest Trials ('+argv[1]+')')
    for o in ForgingBonds.fromAssets(argv[1]):
        o.loadArticle().update().export('Forging Bonds ('+argv[1]+')', create=-1)
    for o in HallOfForms.fromAssets(argv[1]):
        o.loadArticle().update().export('Hall of Forms ('+argv[1]+')', create=-1)
    for o in MjolnirsStrike.fromAssets(argv[1]):
        o.createArticle().export('Mjölnir\'s Strike ('+argv[1]+')')
    for o in SeersSnare.fromAssets(argv[1]):
        o.createArticle().export('Seer\'s Snare ('+argv[1]+')')
    for o in AffinityAutoBattles.fromAssets(argv[1]):
        o.createArticle().export('Affinity Auto Battle ('+argv[1]+')')
