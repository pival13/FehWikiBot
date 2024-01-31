#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.HoF import HallOfFormsReader

class HallOfForms(ArticleContainer):
    _reader = HallOfFormsReader
    _linkArticleData = (r'startTime\s*=\s*([0-9TZ\-:]{20})', ['avail','start'])

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or 'Hall of Forms ' + str(self.number)

    @property
    def number(self) -> int:
        from ..Tool.Wiki import Wiki
        return int(Wiki.cargoQuery('HallOfForms', 'COUNT(DISTINCT _pageName)=Nb', where='StartTime < "'+self.data['avail']['start']+'"', limit=1))+1


    def Infobox(self):
        from ..Utility.Units import Heroes
        return super().Infobox('Hall of Forms', {
            'number': self.number,
            'promoArt': f'Hall of Forms {self.number}.jpg',
            'forma': ';'.join(Heroes.get(u).name for u in self.data['formas']['units']),
            'startTime': self.data['avail']['start'],
            'endTime': self.data['avail']['end'],
        })

    def Availability(self):
        from ..Tool.misc import timeFormat
        return super().Availability('[[Hall of Forms]]', self.data['avail'],
                                    timeFormat(self.data['avail']['start'], 'Hall of Forms (%b %Y)'),
                                    [('Formas recruitable', self.data['forma_avail'])])

    def Rewards(self):
        from ..Utility.Reward import Reward
        from ..Utility.Messages import EN
        s =  '==Rewards==\n'
        s += '===Daily rewards===\n'
        s += '{{#invoke:Reward/HallOfForms|daily\n'
        for i,r in enumerate(self.data['daily_rewards']):
            s += f" |{i+1}={Reward(r['reward'])}\n"
        s += '}}\n===Chamber cleared===\n'
        s += '{{#invoke:Reward/HallOfForms|chambers\n'
        for c in self.data['chambers']:
            s += f" | {EN('MID_IDOL_TOWER_STAGE_'+c['id_tag'])} = {Reward(c['reward'])}\n"
        return s + '}}'

    def loadArticle(self, canCreate=True, revision=0) -> Self:
        from ..Tool.Wiki import Wiki
        from ..Utility.Units import Heroes
        name = Wiki.cargoQuery('HallOfForms',where=' AND '.join(['Forma HOLDS \''+Heroes.get(h).name.replace('\'','\\\'')+'\'' for h in self.data['formas']['units']]), limit=1)
        s = Wiki.getPageContent(name, revision) if name else None
        if s is not None:
            self.name = name
            self.page = s
        elif canCreate:
            self.createArticle()
        else:
            self.page = ''
        return self

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += '{{Main Events Navbox}}'
        return self

    def update(self) -> Self:
        import re
        from ..Tool.misc import timeFormat

        if self.data is None or self.page == '': return self
        if self.page.find(self.data['avail']['start']) != -1: return self

        self.page = re.sub(r'(\|startTime=[^\n|}]*)\n', f"\\1,{self.data['avail']['start']}\n", self.page, 1)
        self.page = re.sub(r'(\|endTime=[^\n|}]*)\n', f"\\1,{self.data['avail']['end']}\n", self.page, 1)

        avail = super().Availability('', self.data['avail'], timeFormat('Hall of Forms Revival (%b %Y)'))
        self.page = re.sub(r'(\{\{HT\|.+)\n(==Rewards==)', '\\1\n' + avail[46:] + '\n\\2', self.page, 1)

        rewards = self.Rewards()
        if not re.search(r'===\s*Daily rewards\s*===\n\{\{Tab/start\}\}', self.page):
            self.page = re.sub(r'(===\s*Daily rewards\s*===)(.+?)(?=\n+==)', '\\1\n{{Tab/start}}\n{{Tab/header|Original}}\\2\n{{Tab/end}}', self.page, flags=re.DOTALL)
        if not re.search(r'#invoke:Reward/HallOfForms\|daily\s*\|startTime', self.page):
            self.page = self.page.replace('#invoke:Reward/HallOfForms|daily','#invoke:Reward/HallOfForms|daily|startTime=' + re.search(r'startTime\s*=\s*([\dTZ:\-]+)',self.page)[1])
        if not re.search(r'\|daily\s*\|startTime='+self.data['avail']['start'], self.page):
            r = rewards[32 : rewards.find('}}')+2].replace('|daily','|daily|startTime='+self.data['avail']['start'])
            self.page = re.sub(r'(#invoke:Reward/HallOfForms\|daily.*?)\n(\{\{Tab/end\}\})', '\\1\n{{Tab/header|Revival}}\n'+r+'\n\\2', self.page, flags=re.DOTALL)

        if not re.search(r'===\s*Chamber cleared\s*===\n\{\{Tab/start\}\}', self.page):
            self.page = re.sub(r'(===\s*Chamber cleared\s*===)(.+?)(?=\n+==)', '\\1\n{{Tab/start}}\n{{Tab/header|Original}}\\2\n{{Tab/end}}', self.page, flags=re.DOTALL)
        if not re.search(r'#invoke:Reward/HallOfForms\|chambers\s*\|startTime', self.page):
            self.page = self.page.replace('#invoke:Reward/HallOfForms|chambers','#invoke:Reward/HallOfForms|chambers|startTime=' + re.search(r'startTime\s*=\s*([\dTZ:\-]+)',self.page)[1])
        if not re.search(r'\|chambers\s*\|startTime='+self.data['avail']['start'], self.page):
            r = rewards[rewards.find('}}')+25 :].replace('|chambers','|chambers|startTime='+self.data['avail']['start'])
            self.page = re.sub(r'(#invoke:Reward/HallOfForms\|chambers.*?)\n(\{\{Tab/end\}\})', '\\1\n{{Tab/header|Revival}}\n'+r+'\n\\2', self.page, flags=re.DOTALL)

        return self

HoF = HallOfForms
