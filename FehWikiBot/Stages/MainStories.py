#! /usr/bin/env python3

from typing_extensions import Self
from .StoryContainer import StoryContainer

class MainStory(StoryContainer):
    @classmethod
    def get(cls, key: str) -> Self | None:
        import re
        if not re.match(r'^S\d{3}[1-5][A-C]?$', key): return None
        obj = super().get('C0'+key[1:4], 'id_tag')
        if obj is None: return None
        o = cls()
        o.data = obj.data
        o.idx = int(key[4])-1
        return o

    @classmethod
    def getAll(cls, key: str, at: list = None) -> list[Self]:
        objs = super().getAll(key, at)
        os = []
        for obj in objs:
            if obj.data['paralogue']: continue
            for i in range(len(obj.data['maps'])):
                o = cls()
                o.data = obj.data
                o.idx = i
                os.append(o)
        return os

    @classmethod
    def getGroup(cls, key: str, at: list=None) -> list[Self]:
        obj = super().get(key, at or 'id_tag')
        if obj is None or obj.data['paralogue']: return []
        os = []
        for i in range(len(obj.data['maps'])):
            o = cls()
            o.data = obj.data
            o.idx = i
            os.append(o)
        return os

    @classmethod
    def fromAssets(cls, file: str) -> list[Self]:
        objs = super().fromAssets(file)
        os = []
        for obj in objs:
            if obj.data['paralogue']: continue
            for i in range(len(obj.data['maps'])):
                o = cls()
                o.data = obj.data
                o.idx = i
                os.append(o)
        return os


    @classmethod
    def GroupArticle(cls, maps: list[Self]) -> dict[str,str]:
        from ..Utility.Messages import EN
        ret = {}
        name = EN('MID_CHAPTER_'+maps[0].data['id_tag'])
        prefix = EN('MID_CHAPTER_TITLE_'+maps[0].data['id_tag'])
        chapter = prefix[prefix.find('Chapter'):]
        ret[name] = '#REDIRECT [[Story Maps#' + chapter + ': ' + name + ']]'

        from ..Utility.Scenario import Scenario
        story = ''
        for i,map in enumerate(maps):
            if map.story == '': continue
            story += f'==[[{map.name}|Part {i+1}]]==\n' + '{{:'+map.name+'/Story}}\n'
        story += Scenario.Navbar('story') + '\n'
        story += Scenario.Navbox('story')
        ret[name+'/Story'] = story

        from ..Tool.Article import Article
        o = Article.fromWiki('Story Maps')
        if o.page.find(prefix + ': ' + name) == -1:
            s = '===' + chapter + ': ' + name + '===\n'
            s += '{{See also|'+name+'/Story}}'
            s += '{{#invoke:MapList|byGroup|'+prefix+': '+name+'}}\n'
            s += o.OtherLanguage('MID_CHAPTER_' + maps[0].data['id_tag']).replace('==', '====')
            ret['Story Maps'] = o.page.replace('{{Battle Screen Navbox}}', s+'\n{{Battle Screen Navbox}}')

        import re
        o = Article.fromWiki('Template:Story Maps Navbox')
        if o.page.find(chapter + ': ' + name) == -1:
            count = int(re.findall(r'\|list(\d+)', o.page)[-1])
            s =  f' |group{count+1}=[[Story Maps#{chapter}: {name}|{chapter}: {name}]]\n'
            s += f' |list{count+1}=\n'
            for i,map in enumerate(maps):
                s += f'# [[{map.name}]]\n'
            ret['Template:Story Maps Navbox'] = o.page.replace('}}}}{{InMain', s+'}}}}{{InMain')

        return ret

    @classmethod
    def exportGroups(cls, files: list[Self], summary: str, *, minor=False, create=True):
        while files != []:
            fs = [files.pop(0)]
            for i in range(len(fs[0].data['maps'])):
                if fs[0].idx == i: continue
                o = [f for f in files if f.data['id_tag'] == fs[0].data['id_tag'] and f.idx == i]
                if len(o) != 1: break
                fs += o
                for f in o: files.remove(f)
            if len(fs) != len(fs[0].data['maps']): continue

            from ..Tool.Wiki import Wiki
            for f in fs: f.export(summary, minor=minor, create=create)
            Wiki.exportPages(cls.GroupArticle(fs), summary, minor=minor, create=-1)

    def export(self, summary: str, *, minor=False, create=True):
        from ..Tool.Wiki import Wiki
        from ..Tool.misc import waitSec
        if self.page == '': return
        waitSec(10)
        Wiki.exportPage(self.name, self.page, summary, minor=minor, create=create)
        if self.story == '': return
        waitSec(10)
        Wiki.exportPage(self.name+'/Story', self.story, summary, minor=minor, create=create)


    def Availability(self):
        from ..Utility.Messages import EN
        notif = ''#'New Heroes Summoning Event: New Heroes & ' + 'Ascended Laegjarn' + '(Notification)'
        return super().Availability('[[Main Story]] map', self.data['avail'], '', isMap=True)

    def Story(self):
        from ..Utility.Scenario import Scenario
        from ..Tool.globals import ROMAN
        s = Scenario.Story(self.id_tag, isStory=True)
        if s[:8] == '{{#ifeq:' and s[-4:] == '}}}}':
            self.story = ''
            s = '==Story==\n' + s[48:-2]
        else:
            self.story = s + '<noinclude>[[Category:Book ' + ROMAN[self.data['book']] + ' scenarios]]</noinclude>'
            s = '==Story==\n{{/Story}}'
        return s + '\n' + Scenario.StoryNavbar(self.map['Normal']['id_tag'][:-1])

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Units() + '\n'
        self.page += '==Other appearances==\n{{BattleAppearances}}\n'
        self.page += self.Story() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Story Maps Navbox|book='+str(self.data['book'])+'}}'
        return self
