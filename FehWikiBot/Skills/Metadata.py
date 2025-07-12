#! /usr/bin/env python3

from ..Tool import Container
from .Reader import SkillAbilityReader, SkillLimitReader, SkillTimingReader

class SkillAbility(Container):
    _reader = SkillAbilityReader
    _key = None

class SkillLimit(Container):
    _reader = SkillLimitReader
    _key = None

class SkillTiming(Container):
    _reader = SkillTimingReader
    _key = None
