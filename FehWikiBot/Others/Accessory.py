#! /usr/bin/env python3

from ..Tool.ArticleContainer import ArticleContainer, Container
from .Reader.Accessory import AccessoryReader as Reader,\
                              AccessoryPurchaseData as ShopReader

class AccessoriesPurchasable(Container):
    _reader = ShopReader

class Accessories(ArticleContainer):
    _reader = Reader
    _linkArticleData = (r'tagid\s*=\s*(DAID_[^|}\n]+)', 'id_tag')

    @classmethod
    def load(cls, name: str) -> bool:
        ret = super().load(name)
        if not ret: return False

        datas = cls._DATA.get(name)
        for data in (datas.values() if isinstance(datas, dict) else datas or []):
            data['@Shop'] = AccessoriesPurchasable.get(data['id_tag']).data if AccessoriesPurchasable.get(data['id_tag']) else None

        return True

    @ArticleContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import Messages
        if self.data['id_tag'] == 'DAID_黄金の呪い': return 'Golden Curse (Accessory)'
        return super().name or Messages.EN(self.data['id_tag'])

    def Infobox(self):
        from ..Utility.Messages import Messages
        return super().Infobox('Accessory', {
            'tagid': self.data['id_tag'],
            'sort': self.data['sort_id'],
            'type': self.data['type'],
            'isSummoner': 1 if self.data['summoner'] else None,
            'description': Messages.EN(self.data['id_tag'].replace('_','_H_',1)).replace('\n',' ')
        })

    def Availability(self):
        s = "==Obtained from==\n"
        if self.data['id_tag'][-2:] == '・金':
            s += '{{Gold accessory}}\n'
        elif self.data['id_tag'][-2:] == '・極' or Accessories.get(self.data['id_tag']+'・極') is not None:
            s += '{{Forging Bonds accessory}}\n'
        elif self.data['id_tag'][:8] == 'DAID_旅先の':
            s += '{{Heroes Journey accessory}}\n'
        #{{Rokkr Sieges accessory}}
        #{{Tap Battle accessory}}
        if self.data['@Shop'] is not None:
            s += '{{Shop accessory|' + str(self.data['@Shop']['cost']) + '}}\n'
        return s[:-1]

    def OtherLanguage(self):
        return super().OtherLanguage(self.data['id_tag'])

    def createArticle(self):
        if self.data is None: return self

        self.page  = self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Accessories Navbox|'+self.data['type']+'}}'

        return self
        