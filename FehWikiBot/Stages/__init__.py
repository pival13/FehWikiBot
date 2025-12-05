#! /usr/bin/env pyhton3

from .MainStories import MainStory
from .Paralogues import Paralogue
from .TD import TacticsDrills
from .HO import HeroicOrdeals, MergedOrdeals
from .CC import StoryChainChallenge, ParalogueChainChallenge
from .SA import SquadAssault

from .HB import *
from .RD import RivalDomains
from .Event import EventMap
from .SpecialMapContainer import unsupportedSpecialMaps

from .Terrain import Map

def StageFromMap(map_id):
    import re
    from ..Events.TT import TempestTrials
    if   re.match(r'S[0-9A-F]\d{3}',map_id): return MainStory.get(map_id)
    elif re.match(r'X\d{4}',map_id): return Paralogue.get(map_id)
    elif re.match(r'XX\d{3}',map_id): return Paralogue.get(map_id) # Xenologue
    elif re.match(r'P[ABC]\d{3}',map_id): return TacticsDrills.get(map_id)
    elif re.match(r'H\d{4}',map_id): return HeroicOrdeals.get(str(int(map_id[1:])))
    elif re.match(r'J\d{4}',map_id): return MergedOrdeals.get(str(int(map_id[1:])))
    elif re.match(r'SB_\d{4}',map_id): return SquadAssault.get(map_id)
    elif re.match(r'ST_C\d{4}',map_id): return StoryChainChallenge.get(map_id)
    elif re.match(r'ST_CX\d{3}',map_id): return ParalogueChainChallenge.get(map_id)
    elif re.match(r'Q\d{4}',map_id): return RivalDomains.get(map_id)
    elif re.match(r'[TL]\d{4}',map_id): return HeroBattle.get(map_id)
    elif re.match(r'I\d{4}',map_id): return LimitedHeroBattle.get(map_id)
    elif re.match(r'V\d{4}',map_id): return EventMap.get(map_id)
    elif re.match(r'W\d{4}',map_id): return TempestTrials.get(map_id+'A',('sets',0,'battles',-1,'maps',0))
    # r'U\d{4}' == Hero Battle (1/2 star)
    # r'R\d{4}' == Relay Defense
    # r'Z\d{4}' == Arena
    # r'ZR\d{3}' == Summoner Duels
    # r'F\d{4}' == Allegiance Battle
    # r'Y\d{4}' == Resonant Battle
    # r'K0\d{3}' == Aether Raids
    # r'K1\d{3}' == Aether Resort
    # r'O\d{4}' == Grand Conquests
    # r'M\d{4}' == Mjölnir's Strike
    # r'BG\d{3}' == Pawns of Loki
    # r'G\d{4}' == Røkkr Sieges
    return None
