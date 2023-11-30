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
                if notif != '':
                    s += '|notification=' + notif + ' (Notification)'
                else:
                    s += '|notification='
            s += '}}'
        else:
            s += '* {{HT|' + (avail.get('start') or '') + '}}'
            if avail.get('end'):
                s += ' – {{HT|' + avail['end'] + '}}'
            if isinstance(notif, str):
                s += ' ([[' + notif + (' (Notification)' if notif != '' else '') + '|Notification]])'
        for subAvail in subAvails:
            s += '\n** {{HT|' + (subAvail.get('start') or '') + '}} – {{HT|' + subAvail.get('end') + '}}'
        return s

    def OtherLanguage(self, tag, tag2=None, swapJp=True):
        def lang(l,sep,swap):
            from ..Utility.Messages import Messages
            s = Messages.get(tag,l).replace('\n',' ')
            if s == '' or tag2 is None: return s
            if swap:
                return Messages.get(tag2,l).replace('\n',' ') + sep + s
            else:
                return s + sep + Messages.get(tag2,l).replace('\n',' ')

        s = '==In other languages==\n'
        s += '{{OtherLanguages\n'
        if lang('USEN', ': ', False) != self.name:
            s += '|english=' + lang('USEN', ': ', False) + '\n'
        s += '|japanese=' +    lang('JPJA', '　', swapJp) + '\n'
        s += '|german=' +      lang('EUDE', ': ', False) + '\n'
        s += '|spanishEU=' +   lang('EUES', ': ', False) + '\n'
        s += '|spanishLA=' +   lang('USES', ': ', False) + '\n'
        s += '|french=' +      lang('EUFR', ' : ', False) + '\n'
        s += '|italian=' +    (lang('EUIT', ': ', True) if swapJp else lang('EUIT', ', ', False)) + '\n'
        s += '|chineseTW=' +   lang('TWZH', '　', swapJp) + '\n'
        s += '|portuguese=' +  lang('USPT', ': ', False) + '\n'
        s += '}}'
        return s
