#! /usr/bin/env python3

from FehWikiBot.Tool.Reader import IReader
from FehWikiBot.Others.Reader.Accessory import AccessoryReader, AccessoryAideData, AccessoryPurchaseData
from FehWikiBot.Others.Reader.AetherRaids import StructureReader, ConsumableReader
from FehWikiBot.Others.Reader.Summon import FocusReader
from FehWikiBot.Others.Reader.CompileManual import CompileCombatManualReader
from FehWikiBot.Utility.Reader.Message import MessageReader
from FehWikiBot.Utility.Reader.Sound import SoundReader, MapBGMReader, HOBGMReader
from FehWikiBot.Utility.Reader.Unit import HeroReader, EnemyReader
from FehWikiBot.Skills.Reader import SkillReader, RefineryReader, SealReader, SealForgeReader, CaptainSkillReader
from FehWikiBot.Stages.Reader.Terrain import MapReader, EnvironmentReader, CellEnvironmentReader
from FehWikiBot.Stages.Reader.Story import StoryMapReader
from FehWikiBot.Stages.Reader.Special import SpecialMapReader
from FehWikiBot.Stages.Reader.HO import HeroicOrdealsReader
from FehWikiBot.Stages.Reader.TD import TacticsDrillsReader
# from FehWikiBot.Stages.Reader.CC
# from FehWikiBot.Stages.Reader.SA
from FehWikiBot.Events.Reader.VG import VotingGauntletReader
from FehWikiBot.Events.Reader.TT import TempestTrialsReader
from FehWikiBot.Events.Reader.TB import TapBattleReader
from FehWikiBot.Events.Reader.GC import GrandConquestReader, GrandConquestWorldReader
from FehWikiBot.Events.Reader.FB import ForgingBondsReader
from FehWikiBot.Events.Reader.RS import RokkrSiegesReader
from FehWikiBot.Events.Reader.LL import LostLoreReader
from FehWikiBot.Events.Reader.HoF import HallOfFormsReader
from FehWikiBot.Events.Reader.MS import MjolnirsStrikeReader, MechanismReader
from FehWikiBot.Events.Reader.FP import FrontlinePhalanxReader
from FehWikiBot.Events.Reader.PoL import PawnsOfLokiReader
from FehWikiBot.Events.Reader.HJ import HeroesJourneyReader
from FehWikiBot.Events.Reader.SD import SummonerDuelsReader, SummonerDuelsRankedReader, SummonerDuelsSurvivalReader, SummonerDuelsSeasonReader
from FehWikiBot.Events.Reader.BW import BindingWorldsReader
from FehWikiBot.Events.Reader.SS import SeersSnareReader
from FehWikiBot.Events.Reader.AAB import AffinityAutoBattlesReader
from FehWikiBot.Events.Reader.UW import UnitedWarfrontReader

READERS : list[IReader] = [ AccessoryReader, AccessoryAideData, AccessoryPurchaseData, StructureReader, MechanismReader, ConsumableReader, FocusReader, CompileCombatManualReader, SoundReader, MapBGMReader, HOBGMReader, HeroReader, EnemyReader,
                            SkillReader, RefineryReader, SealReader, SealForgeReader, CaptainSkillReader,
                            MapReader, EnvironmentReader, CellEnvironmentReader, StoryMapReader, SpecialMapReader, HeroicOrdealsReader, TacticsDrillsReader,
                            VotingGauntletReader, TempestTrialsReader, TapBattleReader, GrandConquestReader, GrandConquestWorldReader, ForgingBondsReader, RokkrSiegesReader, LostLoreReader, HallOfFormsReader, MjolnirsStrikeReader, FrontlinePhalanxReader, PawnsOfLokiReader, HeroesJourneyReader, SummonerDuelsReader, SummonerDuelsRankedReader, SummonerDuelsSurvivalReader, SummonerDuelsSeasonReader, BindingWorldsReader, SeersSnareReader, AffinityAutoBattlesReader, UnitedWarfrontReader ]


from FehWikiBot.PersonalData import BINLZ_ASSETS_DIR_PATH
from FehWikiBot.Tool.globals import WARNING
from sys import argv
from os.path import realpath

if __name__ == '__main__':
    if len(argv) != 2: exit(1)
    arg = realpath(argv[1])
    if arg.find(realpath(BINLZ_ASSETS_DIR_PATH)) != 0:
        print(WARNING + 'Invalid path')
        exit(1)
    if arg[-7:] != '.bin.lz':
        print(WARNING + 'Invalid path')
        exit(1)
    arg = arg[:-7]

    if arg.replace('\\','/').find('/Common/') == -1:
        f = arg.replace(realpath(BINLZ_ASSETS_DIR_PATH),'')[1:] + '.bin.lz'
        o = MessageReader.fromAssets(f)
        if not o.isValid():
            print(WARNING + 'File not found')
            exit(1)
        print(o.object)
        exit(0)

    for r in READERS:
        if arg.find(realpath(BINLZ_ASSETS_DIR_PATH+'/'+r._basePath)) != 0: continue
        f = arg.replace(realpath(BINLZ_ASSETS_DIR_PATH+'/'+r._basePath), '')[1:]
        if f.replace('\\','/').find('/') != -1: continue

        o = r.fromAssets(f)
        if not o.isValid():
            print(WARNING + 'File not found')
            exit(1)
        print('Header:', o._header)
        print('String table', o._strTbl)
        print(o.object)
        exit(0)

    print(WARNING + 'Reversal method not found')
    IReader(open(realpath(argv[1]),'rb').read())
    exit(1)
