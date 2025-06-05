#! /usr/bin/env python3

from FehWikiBot.Others.Accessory import Accessories
from FehWikiBot.Others.AetherRaids import Structure
from FehWikiBot.Others.CompileManual import CompileManual
from FehWikiBot.Skills import *
from FehWikiBot.Stages import *
from FehWikiBot.Events import *
from FehWikiBot.Tool.globals import TODO

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1: exit(0)

    dones = []
    for o in Accessories.fromAssets(argv[1]):
        o.createArticle().export('Accessory ('+argv[1]+')')
    for o in Structure.fromAssets(argv[1]):
        o.loadArticle().update().export('Structure ('+argv[1]+')', create=-1)
    CompileManual.updateExportFromAssets(argv[1])

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

    MainStory.exportGroups([o.createArticle() for o in MainStory.fromAssets(argv[1])], 'Story maps ('+argv[1]+')')
    Paralogue.exportGroups([o.createArticle() for o in Paralogue.fromAssets(argv[1])], 'Paralogue maps ('+argv[1]+')')
    for o in TacticsDrills.fromAssets(argv[1]):
        o.createArticle().export('Tactics Drills ('+argv[1]+')')
    for o in HeroicOrdeals.fromAssets(argv[1]):
        o.createArticle().export('Heroic Ordeals ('+argv[1]+')')
    for o in MergedOrdeals.fromAssets(argv[1]):
        o.createArticle().export('Merged Ordeals ('+argv[1]+')')
    # Chain Challenge
    for o in SquadAssault.fromAssets(argv[1]):
        o.createArticle().export('Squad Assault ('+argv[1]+')')
    for o in RivalDomains.fromAssets(argv[1]):
        o.createArticle().export('Rival Domains ('+argv[1]+')')
    for o in HeroBattle.fromAssets(argv[1]):
        o.createArticle().export(o.category + ' ('+argv[1]+')')
    for o in LimitedHeroBattle.fromAssets(argv[1]):
        o.loadArticle().update().export(o.category + ' ('+argv[1]+')', create=False)
    for o in HeroBattle.upcomingRevivals(argv[1]):
        o.loadArticle(False).update().export('Revival ('+argv[1]+')', create=False)
    if unsupportedSpecialMaps(argv[1]) != []:
        print(TODO + 'Unsupported Special maps: ' + str(unsupportedSpecialMaps(argv[1])))

    for o in VotingGauntlet.upcomingEvents():
        o.createArticle().export('Voting Gauntlet ('+argv[1]+')')
    for o in TempestTrials.fromAssets(argv[1]):
        o.createArticle().export('Tempest Trials ('+argv[1]+')')
    for o in ForgingBonds.fromAssets(argv[1]):
        o.loadArticle().update().export('Forging Bonds ('+argv[1]+')', create=-1)
    for o in HallOfForms.fromAssets(argv[1]):
        o.loadArticle().update().export('Hall of Forms ('+argv[1]+')', create=-1)
    for o in MjolnirsStrike.fromAssets(argv[1]):
        o.createArticle().export('Mjölnir\'s Strike ('+argv[1]+')')
    for o in PawnsOfLoki.fromAssets(argv[1]):
        o.createArticle().export('Pawns of Loki ('+argv[1]+')')
    for o in HeroesJourney.fromAssets(argv[1]):
        o.createArticle().export('Heroes Journey ('+argv[1]+')')
    for o in BindingWorlds.fromAssets(argv[1]):
        o.createArticle().export('Binding Worlds ('+argv[1]+')')
    for o in SummonerDuelsR.fromAssets(argv[1]):
        o.createArticle().export('Summoner Duels R ('+argv[1]+')')
    for o in SummonerDuelsS.fromAssets(argv[1]):
        o.createArticle().export('Summoner Duels S ('+argv[1]+')')
    for o in SeersSnare.fromAssets(argv[1]):
        o.createArticle().export('Seer\'s Snare ('+argv[1]+')')
    for o in AffinityAutoBattles.fromAssets(argv[1]):
        o.createArticle().export('Affinity Auto Battle ('+argv[1]+')')
    for o in UnitedWarfront.fromAssets(argv[1]):
        o.createArticle().export('United Warfront ('+argv[1]+')')
