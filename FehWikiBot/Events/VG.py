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
    def upcomingEvents(cls) -> list[Self]:
        from datetime import datetime, timedelta
        from ..Tool.globals import TIME_FORMAT
        now = (datetime.now() - timedelta(days=1)).strftime(TIME_FORMAT)
        os = []
        for evt in cls.fromAssets():
            if evt.data['avail']['start'] > now:
                os.append(evt)
        return os

    @classmethod
    def incompleteArticles(cls) -> list[Self]:
        from ..Tool.Wiki import Wiki
        os = Wiki.cargoQuery('VotingGauntlets', where='Scores3 IS NULL')
        pages = Wiki.getPagesContent(os)
        os = []
        for page,content in pages.values():
            o = cls()
            o.name = page
            o.page = content
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


    def Infobox(self):
        from num2words import num2words
        from ..Tool import Wiki
        from ..Utility.Units import Heroes
        nb = int(Wiki.cargoQuery('VotingGauntlets', 'COUNT(DISTINCT _pageName)=Nb', where='StartTime < "'+self.data['avail']['start']+'"', limit=1))+1
        return super().Infobox('Voting Gauntlet', {
            'tournamentNumber': nb,
            'heroes': ';'.join([Heroes.get(h).name for h in self.data['units']]),
            'scores1': '',
            'scores2': '',
            'scores3': '',
            'startTime': self.data['avail']['start'],
            'endTime': self.data['avail']['end'],
            'banner1': '',
            'description': 'The ' + num2words(nb, to='ordinal') + ' [[Voting Gauntlet]] event.',
        }).replace(' Infobox','')
    
    def OtherLanguage(self):
        return super().OtherLanguage('MID_VOTE_TERM_' + self.data['id_tag'])

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Main Events Navbox}}'
        return self

    def update(self) -> Self:
        import re
        import requests

        if self.page.find('scores3=\n') == -1: return self

        nb = re.search(r'\|tournamentNumber=(\d+)', self.page)[1]
        content = requests.get(url=f'https://support.fire-emblem-heroes.com/voting_gauntlet/tournaments/{nb}?locale=en-US').content.decode()
        
        scores = re.findall(r'tournaments-art-name.*?<p>((?:\d+,?)*)</p>', content)
        scores1 = scores[-8:]
        scores2 = scores[-12:-8]
        scores3 = scores[-14:-12]

        self.page = re.sub(r'(\|scores1=).*\n', '|scores1='+';'.join(scores1)+'\n', self.page)
        self.page = re.sub(r'(\|scores2=).*\n', '|scores2='+';'.join(scores2)+'\n', self.page)
        self.page = re.sub(r'(\|scores3=).*\n', '|scores3='+';'.join(scores3)+'\n', self.page)

        return self


VG = VotingGauntlet
