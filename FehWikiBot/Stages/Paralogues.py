#! /usr/bin/env python3

from typing_extensions import Self
from .StoryContainer import StoryContainer

class Paralogue(StoryContainer):
    @classmethod
    def get(cls, key: str) -> Self | None:
        import re
        if re.match(r'^X\d{3}[1-3][A-C]?$',key):
            obj = super().get('CX'+key[1:4], 'id_tag')
            if obj is None: return None
            o = cls()
            o.data = obj.data
            o.idx = int(key[4])-1
            return o
        elif re.match(r'^XX\d{3}$',key):
            obj = super().get('CXX'+key[2:4], 'id_tag')
            if obj is None: return None
            o = cls()
            o.data = obj.data
            o.idx = 0
            return o
        else:
            return None

    @classmethod
    def getAll(cls, key: str, at: list = None) -> list[Self]:
        objs = super().getAll(key, at)
        os = []
        for obj in objs:
            if not obj.data['paralogue']: continue
            for i in range(len(obj.data['maps'])):
                o = cls()
                o.data = obj.data
                o.idx = i
                os.append(o)
        return os

    @classmethod
    def getGroup(cls, key: str, at: list=None) -> list[Self]:
        obj = super().get(key, at or 'id_tag')
        if obj is None or not obj.data['paralogue']: return []
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
            if not obj.data['paralogue']: continue
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
        ret[name] = '#REDIRECT [[Paralogue Maps#' + prefix + ': ' + name + ']]'

        from ..Utility.Scenario import Scenario
        from datetime import datetime
        from ..Tool.globals import TIME_FORMAT
        story = ''
        for i,map in enumerate(maps):
            story += f'==[[{map.name}|Part {i+1}]]==\n' + '{{:'+map.name+'/Story}}\n'
        # TODO Use Tempest Trials class
        time = datetime.strptime(maps[0].data['avail']['start'], TIME_FORMAT)
        tt = EN('MID_SEQUENTIAL_MAP_TERM_'+time.strftime('%Y%m'))
        story += f'==[[{tt}|Extra]]==\n' + '{{:'+tt+'/Story}}\n'
        story += Scenario.Navbar('paralogue', maps[0].category()) + '\n'
        story += Scenario.Navbox('paralogue')
        ret[name+'/Story'] = story

        from ..Tool.Article import Article
        o = Article.fromWiki('Paralogue Maps')
        if o.page.find(prefix + ': ' + name) == -1:
            s = '===' + prefix + ': ' + name + '===\n'
            s += '{{See also|'+name+'/Story}}'
            s += '{{#invoke:MapList|byGroup|'+prefix+': '+name+'}}\n'
            s += o.OtherLanguage('MID_CHAPTER_' + maps[0].data['id_tag']).replace('==', '====')
            ret['Paralogue Maps'] = o.page.replace('==Xenologues==', s+'\n==Xenologues==')

        import re
        o = Article.fromWiki('Template:Paralogue Maps Navbox')
        if o.page.find(prefix + ': ' + name) == -1:
            count = int(re.findall(r'\|list(\d+)', o.page)[-2]) # -1 is for xenologue
            s =  f' |group{count+1}=[[Paralogue Maps#{prefix}: {name}|{prefix}: {name}]]\n'
            s += f' |list{count+1}=\n'
            for i,map in enumerate(maps):
                s += f'# [[{map.name}]]\n'
            ret['Template:Paralogue Maps Navbox'] = o.page.replace('|group99', s+'|group99')

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
        type = '[[Paralogue]] map' if self.data['id_tag'][:2] != 'XX' else '[[Xenologue]]'
        notif = 'Special Heroes Summoning Event: ' + EN('MID_CHAPTER_'+self.data['id_tag'])
        return super().Availability(type, self.data['avail'], notif, isMap=True)

    def category(self):
        from datetime import datetime
        from ..Tool.globals import TIME_FORMAT, TODO
        start = datetime.strptime(self.data['avail']['start'], TIME_FORMAT)
        if (start.month == 12 and start.day > 25) or (start.month == 1 and start.day <= 5): return 'New Year Festival'
        elif start.month == 2: return 'Day of Devotion'
        elif start.month == 3: return 'Spring Festival'
        elif start.month == 4: return 'Children Adventure'
        elif start.month == 5: return 'Bridal Festival'
        elif start.month in (6,7): return 'Summer Vacation'
        elif start.month == 10: return 'Harvest Festival'
        elif start.month == 12 and start.day <= 25: return 'Winter Festival'
        else:
            print(TODO + 'Story category for '+self.name) # TODO
            return 'Unknown'

    def Story(self):
        from ..Utility.Scenario import Scenario
        self.story =  Scenario.Story(self.id_tag)
        self.story += '<noinclude>[[Category:'+self.category()+' scenarios]]</noinclude>'
        return '==Story==\n{{/Story}}\n' + Scenario.StoryNavbar(self.map['Normal']['id_tag'][:-1])

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Units() + '\n'
        self.page += '==Other appearances==\n{{BattleAppearances}}\n'
        self.page += self.Story() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Paralogue Maps Navbox}}'
        return self
