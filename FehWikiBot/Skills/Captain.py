#! /usr/bin/env python3

from typing_extensions import Self
from .Reader import CaptainSkillReader
from ..Tool.ArticleContainer import ArticleContainer

class CaptainSkill(ArticleContainer):
    _reader = CaptainSkillReader
    _linkArticleData = (r'', '')

    @ArticleContainer.name.getter
    def name(self):
        from ..Utility.Messages import EN
        return super().name or EN('MID_REALTIME_PVP_SKILL_' + self.data['id_tag'])

    def Infobox(self):
        from .Skills import Skills
        return super().Infobox('Captain Skill', {
            'name': self.name,
            'effect': Skills.description('MID_REALTIME_PVP_SKILL_H_' + self.data['id_tag']),
            'statModifiers': '',
            'properties': ''
        }).replace(' Infobox','',1)

    def OtherLanguage(self):
        return super().OtherLanguage('MID_REALTIME_PVP_SKILL_' + self.data['id_tag'])

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += '==Notes==\n\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '==See also==\n{{See also skills|cond= False }}\n'
        self.page += '{{Captain Skills Navbox}}'
        return self