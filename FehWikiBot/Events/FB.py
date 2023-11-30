#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.FB import ForgingBondsReader

class ForgingBonds(ArticleContainer):
    _reader = ForgingBondsReader
    _linkArticleData = (r'', 'id_tag')

    def __init__(self):
        self.pages = {}
        super().__init__()

    @ArticleContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import EN
        k = self.data['title_id'].replace(self.data['id_tag'],self.data['scenario_id'])
        return super().name or EN(k) if self.data is not None else None

    @property
    def number(self) -> int:
        from ..Tool.Wiki import Wiki
        return 1 + int(Wiki.cargoQuery('ForgingBonds', 'COUNT(DISTINCT _pageName)=Nb', where=f"StartTime < '{self.data['avail']['start']}'", limit=1))

    @property
    def page(self) -> str:
        return self.pages[''] if '' in self.pages else ''

    @page.setter
    def page(self, v):
        self.pages[''] = v

    def Infobox(self):
        from ..Utility.Units import Units
        from ..Others.Accessory import Accessories
        return super().Infobox('Forging Bonds', {
            'number': self.number,
            'characters': ','.join([Units.get(u).name for u in self.data['units']]),
            'accessories': ','.join([Accessories.get(a).name for a in self.data['accessories']]),
            'startTime': self.data['avail']['start'], 'endTime': self.data['avail']['end'],
        })

    def Availability(self):
        return super().Availability('[[Forging Bonds]]', self.data['avail'], 'Forging Bonds: ' + self.name)

    def Rewards(self):
        from ..Tool.misc import cleanStr
        from ..Utility.Reward import Rewards
        FB_COLORS = ['Red', 'Orange', 'Green', 'Blue']
        s  = '==Rewards==\n{{#invoke:Reward/ForgingBonds|main\n'
        s += '|wikiname=' + cleanStr(self.name) + ' ' + self.data['avail']['start'][:10].replace('-','') + '\n'
        for i, color in enumerate(FB_COLORS):
            s += '|' + color + '='
            s += Rewards({r['score']: r['reward'] for r in self.data['hero_rewards'] if r['unit'] == i+1}) + '\n'
        s += '}}'
        return s
    
    def Story(self):
        from ..Utility.Units import Units
        from ..Utility.Scenario import Scenario
        s  = '==Special conversations==\n'
        s += '===' + self.name + '===\n'
        s += '{{/Story}}\n'
        for u in self.data['units']:
            u = Units.get(u)
            s += '===' + u.name + '===\n'
            s += '{{/' + u.name + '}}\n'
        s += Scenario.StoryNavbar(self.data['title_id'])

        for k in ['/Story'] + ['/'+Units.get(u).name for u in self.data['units']]:
            self.pages[k]  = '{{#invoke:Scenario|forgingBonds\n'
            if k == '/Story':
                scenar = Scenario.get('PORTRAIT_'+self.data['scenario_id'])
                if 'MID_SCENARIO_OPENING' in scenar and len(scenar) == 1:
                    self.pages[k] += '|opening=' + str(scenar['MID_SCENARIO_OPENING']) + '\n'
                else:
                    from ..Tool.globals import WARNING
                    print(WARNING + 'Unexpected FB story: ' + str(scenar.keys()))
                    self.pages[k] += '|opening=\n'
                self.pages[k] += '|C=\n|B=\n|A=\n'
            else:
                self.pages[k] += '|C=\n|B=\n|A=\n|S=\n'
            self.pages[k] += '}}\n'
            self.pages[k] += '<noinclude>\n' + Scenario.Navbar('fb') + '\n' + Scenario.Navbox('fb') + '\n</noinclude>'

        return s

    def OtherLanguage(self):
        return super().OtherLanguage(self.data['title_id'])

    def createArticle(self) -> Self:
        if self.data is None: return self
        
        self.page  = self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += self.Story() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Main Events Navbox}}'

        return self

    def update(self) -> Self:
        import re
        
        if self.data is None or self.page == '': return self
        if self.page.find(self.data['avail']['start']) != -1: return self

        self.page = re.sub(r'(\|startTime=[^|\n}]*)', '\\1;'+self.data['avail']['start'], self.page)
        self.page = re.sub(r'(\|endTime=[^|\n}]*)', '\\1;'+self.data['avail']['end'], self.page)

        avail = super().Availability('', self.data['avail'], 'Forging Bonds Revival: ' + self.name)[46:]
        self.page = re.sub(r'((?:\*\s*\{\{\s*HT\s*\|.*\n)+)', '\\1'+avail+'\n', self.page)

        if not re.search(r'===\s*Original [rR]un\s*===', self.page):
            self.page = re.sub(r'(==\s*Rewards\s*==\n)', '\\1===Original run===\n', self.page)
        self.page = re.sub(r'\}\}\n(\n*==\s*Special [cC]onversations\s*==)', '}}\n===Rerun===\n'+self.Rewards()[12:]+'\n\\1', self.page)

        return self

    def export(self, summary: str, *, minor=False, create=True):
        from ..Tool.Wiki import Wiki
        Wiki.exportPages({
            self.name + k: v
        for k,v in self.pages.items()}, summary, minor, create)

FB = ForgingBonds
