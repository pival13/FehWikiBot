#! /usr/bin/env python3

from ..Tool import ArticleContainer
from .Reader.Special import StageEventReader

class SpecialMapContainer(ArticleContainer):
    _DATA = {}
    _reader = StageEventReader

    def __init_subclass__(cls):
        d = cls._DATA
        super().__init_subclass__()
        cls._DATA = d

    @property
    def id_tag(self):
        return self.data['maps'][0]['id_tag'][:-1]

def unsupportedSpecialMaps(file: str) -> list[SpecialMapContainer]:
    from .HB import HeroBattle, LimitedHeroBattle
    from .RD import RivalDomains
    tags = [o.data['id_tag'] for o in HeroBattle.fromAssets(file)] + \
            [o.data['id_tag'] for o in LimitedHeroBattle.fromAssets(file)] + \
            [o.data['id_tag'] for o in RivalDomains.fromAssets(file)]
    return [o for o in SpecialMapContainer.fromAssets(file) if o.data['id_tag'] not in tags]