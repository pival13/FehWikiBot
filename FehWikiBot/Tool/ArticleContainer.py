#! /usr/bin/env python3

from typing_extensions import Self
from .Article import Article, IncompleteArticle
from .Container import Container
from .JsonContainer import JsonContainer

class ArticleContainer(Article, Container):
    """Parent class combining `Article` and `Container`.
    
    An instance should be created using either `get` or `fromAssets`, used for blank
    article, or `fromWiki` when based on already existing article.
    It is possible to fill a blank article with either `createArticle` or `loadArticle`.

    Any child need to overload `_reader` with the Reader class in use,
    `_linkArticleData` (see the variable for more detail) and optionnaly
    `_key` if `id_tag` is not used for the `Container` ordering.
    Additionally, the `createArticle` method need to be replaced, and it is
    highly recommended to provide a fallback in case of `None` on the `name` property.
    """

    _linkArticleData: tuple[str,str|int|list[str|int]] = None
    "Article pattern with a single match and path to the variable on data"

    def __repr__(self) -> str:
        return '<' + type(self).__name__ + ' "' + str(self.name) + '"' + (f" ({self.id_tag if hasattr(self,'id_tag') else self.data['id_tag']})" if self.data else '') + '>'

    @Article.name.getter
    def name(self) -> str | None:
        try:
            return super().name
        except IncompleteArticle:
            return None

    @classmethod
    def fromWiki(cls, name: str) -> Self | None:
        if cls._linkArticleData is None: raise IncompleteArticle
        from re import search
        o = super().fromWiki(name)
        if o is None: return None
        m = search(cls._linkArticleData[0], o.page)
        if m:
            o2 = super().get(m[1], cls._linkArticleData[1])
            if o2: o.data = o2.data
        return o

    def loadArticle(self, canCreate=True, revision=0) -> Self:
        from ..Tool.Wiki import Wiki
        s =  Wiki.getPageContent(self.name, revision)
        if s is not None:
            self.page = s
        elif canCreate:
            self.createArticle()
        else:
            self.page = ''
        return self

    def createArticle(self) -> Self:
        raise IncompleteArticle