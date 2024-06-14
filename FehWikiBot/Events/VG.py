#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.VG import VotingGauntletReader

class VotingGauntlet(ArticleContainer):
    @classmethod
    def fromWiki(cls, name: str):
        o = super(ArticleContainer).fromWiki(name)
        o.data = None
        return o

    @classmethod
    def fromAssets(cls) -> list[Self]:
        if len(cls._DATA) == 0: cls.load()
        os = []
        for data in cls._DATA.values():
            o = cls()
            o.data = data
            os.append(o)
        return os

    @classmethod
    def load(cls) -> bool:
        if len(cls._DATA) != 0: return False
        reader = VotingGauntletReader.fromUnique()
        if not reader.isValid() or reader.object is None: return False
        cls._DATA = {o[cls._key]: o for o in reader.object}
        return True


    @ArticleContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import EN
        return super().name or EN('MID_VOTE_TERM_' + self.data['id_tag']) if self.data is not None else None

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page = ''
        return self

    def update(self) -> Self:
        if self.data is None or self.page == '': return self
        return self


VG = VotingGauntlet
