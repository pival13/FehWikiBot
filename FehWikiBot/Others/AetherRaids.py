#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer, Container
from .Reader.AetherRaids import ConsumableReader, StructureReader


class AetherRaidsConsumable(Container):
    _reader = ConsumableReader

    @property
    def name(self):
        from ..Utility.Messages import EN
        return EN('MID_ITEM_SKYCASTLE_'+self.data['id_tag']).replace('Stones','Stone')

AetherRaidsItem = AetherRaidsConsumable
ARConsumable = AetherRaidsConsumable
ARItem = AetherRaidsConsumable


class AetherRaidsStructure(ArticleContainer):
    _reader = StructureReader

    def __repr__(self) -> str:
        if self.data is None:
            return '<'+type(self).__name__+' "None">'
        elif not hasattr(self, 'levels'):
            return '<'+type(self).__name__+' "' + str(self.name) + '" (' + self.data['id_tag'] + ')>'
        else:
            return '<'+type(self).__name__+' "' + str(self.name) + '" (' + self.levels[self._i]['id_tag'] + ', ' + str(len(self.levels)-1) + ' others)>'


    @classmethod
    def get(cls, key: str, at: list = None) -> Self | None:
        o = super().get(key, at)
        if o is None or o.data is None or o.data['level'] == 0: return o
        if o.data['base_id'] == None:
            o.levels = [o.data]
            o._i = 0
            return o
        o2 = super().get(o.data['base_id'])
        o2.levels = sorted([v.data for v in super().getAll(o.data['base_id'], 'base_id') if v.data['is_offensive'] == o.data['is_offensive']], key=lambda v: v['level'])
        o2._i = o.data['level']-1
        return o2

    @classmethod
    def getAll(cls, key, at): raise TypeError

    @classmethod
    def fromAssets(cls, file: str) -> list[Self]:
        return [cls.get(o['id_tag']) for o in super().fromAssets(file)]

    @classmethod
    def fromWiki(cls, name: str):
        o = super(ArticleContainer).fromWiki(name)
        o.data = None
        return o


    @ArticleContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import EN
        if super().name or self.data is None: return super().name
        if not hasattr(self, 'levels'):
            return EN('MID_SCF_' + self.data['id_tag'])
        else:
            return EN('MID_SCF_' + self.levels[0]['id_tag'][:-1])


    def Infobox(self):
        from ..Utility.Messages import EN
        data = self.levels[0] if hasattr(self, 'levels') else self.data
        id = data['id_tag'][:-1] if hasattr(self, 'levels') else data['id_tag']
        return super().Infobox('Structure', {
            'category': data['kind'],
            'description': EN('MID_SCF_'+id+'_HELP').replace('\n',' '),
            'descriptionResort': (EN('MID_SCF_'+id+'_HOLIDAYHELP') or EN('MID_SCF_'+id+'_HELP')).replace('\n',' '),
            'parameters0': data['a0'] if data['level'] != 0 else None,
            'costs': data['required'],
            'currency': AetherRaidsItem.get(data['required_id']).name,
            'nolv': 1 if data['level'] == 0 else None,
        }).replace('Structure Infobox','Structure')
    
    def Availability(self):
        if self.data['kind'] == 'Ornaments':
            return super().Availability('[[structure]]', AetherRaidsItem.get(self.data['required_id']).data['avail'], '')
        else:
            return super().Availability('[[structure]]', {'start':''}, '')

    def OtherLanguage(self):
        if not hasattr(self, 'levels'):
            return super().OtherLanguage('MID_SCF_' + self.data['id_tag'])
        else:
            return super().OtherLanguage('MID_SCF_' + self.levels[0]['id_tag'][:-1])

    def createArticle(self) -> Self:
        if self.data is None: return self

        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.OtherLanguage() + '\n'
        self.page += '{{Structures Navbox}}'

        return self
    
    def update(self) -> Self:
        if not hasattr(self, 'levels') or self.page == '': return self

        import re
        params = ','.join(str(data['a0']) for data in self.levels)
        costs = ';'.join(str(data['required']) for data in self.levels)
        self.page = re.sub(r'parameters0=[^\n\}\|]*', 'parameters0='+params, self.page)
        self.page = re.sub(r'costs=[^\n\}\|]*', 'costs='+costs, self.page)
        for i,data in enumerate(self.levels):
            if data['required_id'] == self.levels[0]['required_id'] or self.page.find(f'currency{i+1}=') != -1:
                continue
            if self.page.find(f'currency{i}=') != -1:
                self.page = re.sub(r'(currency'+str(i)+r'=[^\n\|\}]*)', f'\\1\n|currency{i+1}='+AetherRaidsItem.get(data['required_id']).name, self.page)
            else:
                self.page = re.sub(r'(currency=[^\n\|\}]*)', f'\\1\n|currency{i+1}='+AetherRaidsItem.get(data['required_id']).name, self.page, 1)

        return self


ARStructure = AetherRaidsStructure
Structure = AetherRaidsStructure
