#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.Special import StageEventReader

class SpecialContainer(ArticleContainer):
    _DATA = {}
    _reader = StageEventReader

    def __init_subclass__(cls):
        d = cls._DATA
        super().__init_subclass__()
        cls._DATA = d

    @property
    def id_tag(self):
        return self.data['maps'][0]['id_tag'][:-1]
