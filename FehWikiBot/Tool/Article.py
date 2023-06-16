#! /usr/bin/env python3

__all__ = [
    'Article'
]

from typing_extensions import Self

class IncompleteArticle(TypeError):
    "Incomplete class"

class Article:
    """Base class for any class creating or using an article on the Wiki.

    Provides the `fromWiki` method to retrieve an article from the Wiki,
    and stock its `name` and `page`.
    """

    def __init__(self):
        self.page = ''

    @property
    def name(self) -> str:
        if hasattr(self, '_name'):
            return self._name
        raise IncompleteArticle

    @name.setter
    def name(self, v):
        self._name = v

    def export(self, summary:str, *, minor=False, create=True):
        from .Wiki import Wiki
        from .misc import waitSec
        if self.page == '': return
        waitSec(10)
        Wiki.exportPage(self.name, self.page, summary, minor, create)

    @classmethod
    def fromWiki(cls, name:str) -> Self | None:
        from .Wiki import Wiki
        content = Wiki.getPageContent(name)
        if content is None: return None
        o = cls()
        o.name = name
        o.page = content
        return o

    def Infobox(self, name: str, params: dict):
        return '{{' + name + ' Infobox\n|' + '\n|'.join([k+'='+str(v) for k,v in params.items() if v is not None]) + '\n}}'

    def Availability(self, type: str, avail, notif: str=None, subAvails=[], isMap=False):
        s = '==Availability==\n' if not isMap else '==Map availability==\n'
        s += f"This {type} was made available on:\n"
        if isMap:
            s += '* {{MapDates|start=' + (avail.get('start') or '')
            if avail.get('end'):
                s += '|end=' + avail['end']
            if (avail.get('avail_sec') or -1) != -1:
                s += '|cycle=' + avail['cycle_sec'] + '|avail=' + avail['avail_sec']
            if isinstance(notif, str):
                s += '|notification=' + notif
            s += '}}'
        else:
            s += '* {{HT|' + (avail.get('start') or '') + '}} – {{HT|' + avail.get('end') + '}}'
            if isinstance(notif, str):
                s += ' ([[' + notif + '|Notification]])'
        for subAvail in subAvails:
            s += '\n** {{HT|' + (subAvail.get('start') or '') + '}} – {{HT|' + subAvail.get('end') + '}}'
        return s

    def OtherLanguage(self, tag, tag2=None, swapJp=True):
        from ..Utility.Messages import Messages
        lang = lambda lang, sep, swap=False: ((Messages.get(tag2,lang).replace('\n',' ')+sep) if tag2 and swap else '') + Messages.get(tag,lang).replace('\n',' ') + ((sep+Messages.get(tag2,lang).replace('\n',' ')) if tag2 and not swap else '')
        s = '==In other languages==\n'
        s += '{{OtherLanguages\n'
        if lang('USEN', ': ') != self.name:
            s += '|english=' + lang('USEN', ': ') + '\n'
        s += '|japanese=' +    lang('JPJA', '　', swapJp) + '\n'
        s += '|german=' +      lang('EUDE', ': ') + '\n'
        s += '|spanishEU=' +   lang('EUES', ': ') + '\n'
        s += '|spanishLA=' +   lang('USES', ': ') + '\n'
        s += '|french=' +      lang('EUFR', ' : ') + '\n'
        s += '|italian=' +    (lang('EUIT', ': ', True) if swapJp else lang('EUIT', ', ', False)) + '\n'
        s += '|chineseTW=' +   lang('TWZH', '　', swapJp) + '\n'
        s += '|portuguese=' +  lang('USPT', ': ') + '\n'
        s += '}}'
        return s