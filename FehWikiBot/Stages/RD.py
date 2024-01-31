#! /usr/bin/env python3

from typing_extensions import Self
from .SpecialMapContainer import SpecialMapContainer

class RivalDomains(SpecialMapContainer):
    _linkArticleData = (r'baseMap=(Q\d+)', 'id_tag')

    @classmethod
    def fromAssets(cls, file: str) -> list[Self]:
        return [o for o in super().fromAssets(file) if o.data['rival_domain']]

    @SpecialMapContainer.name.getter
    def name(self) -> str:
        from ..Utility.Messages import EN
        return super().name or \
            (EN(self.data['maps'][0]['name_id']) + ': ' + EN(self.data['maps'][0]['honor_id']) + f" ({int(self.data['id_tag'][1:])})") \
                if self.data is not None else None

    def Infobox(self):
        from ..Utility.Messages import EN
        from ..Utility.Reward import Rewards
        GC_BONUS = { '歩行': 'Infantry', '重装': 'Armored', '騎馬': 'Cavalry', '飛行': 'Flying' }
        return super().Infobox('Battle', {
            'bannerImage': 'Banner_Rival_Domains_'+GC_BONUS[self.data['rd_bonus']]+'.png',
            'stageTitle': '',
            'stageName': EN(self.data['maps'][0]['name_id']),
            'stageEpithet': EN(self.data['maps'][0]['honor_id']),
            'mapGroup': 'Rival Domains',
            'mapMode': 'Reinforcement Map',
        } | self.RDTerrain() | {
            'lvlNormal': 30, 'lvlHard': 35, 'lvlLunatic': 40, 'lvlInfernal': 40,
            'rarityNormal': 3, 'rarityHard': 4, 'rarityLunatic': 5, 'rarityInfernal': 5,
            'stamNormal': 0, 'stamHard': 0, 'stamLunatic': 0, 'stamInfernal': 0,
            'reward': Rewards({m['diff']: m['reward'] for m in self.data['maps']}),
            'winReq': 'Reach the target [[Rival Domains#Scoring|score]] to earn<br>a reward. Bonus for defeating<br>foes with {{Mt|'+GC_BONUS[self.data['rd_bonus']]+'}} allies.',
            'BGM': ''
        })

    def Availability(self):
        return super().Availability('[[Rival Domains]]', self.data['avail'], isMap=True)

    def UnitData(self):
        s =  '==Unit data==\n'
        s += '===Enemy AI Settings===\n{{EnemyAI|activeall}}\n'
        s += '===Stats===\n{{RivalDomainsEnemyStats}}\n'
        s += '===List of enemy units===\n'
        s += 'These enemy units make up the brigade for this rival domains:\n{{RDEnemyBrigade|}}'
        return s

    def createArticle(self) -> Self:
        from num2words import num2words
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.UnitData() + '\n'
        self.page += '==Trivia==\n*'
        if self._dup:
            self.page += ' This map layout is the same as Area '+str(self._dup[1])+' of [[Grand Conquests '+str(self._dup[0])+'|the '+num2words(self._dup[0], to='ordinal')+' Grand Conquests event]].'
        self.page += '\n{{Special Maps Navbox}}'
        return self

    def RDTerrain(self):
        from ..Tool.Wiki import Wiki
        from ..Tool.globals import TODO
        import re
        mid = self.data['maps'][0]['base_id'][:5]
        try:
            o = Wiki.get({
                'action': 'query',
                'titles': 'File:Map '+mid+'.webp',
                'prop': 'duplicatefiles', 
            })
            o = list(o['query']['pages'].values())[0]
            o = o['duplicatefiles'] if 'duplicatefiles' in o else []
            o = [p['name'][4:9] for p in o if p['name'][:5] == 'Map_O']
            if o == []: raise Exception('No duplicate for ' + mid)

            nGC = (int(o[0][1:])-1) // 30 + 1
            page = Wiki.getPageContent('Grand Conquests ' + str(nGC))
            GCLayout = re.search(r'\|\s*(\d+)\s*\n\|\s*\{\{MapLayout\D+'+o[0]+'.*\n(?:(?!\}\}\n).*\n)+\}\}', page)
            if not GCLayout: raise Exception('Failed to find the layout of ' + o[0] + ' in GC ' + str(nGC))
            self._dup = (nGC, int(GCLayout[1]))
            bg = re.search(r'backdrop\s*=\s*(\w*)', GCLayout[0])[1]
            objects1 = [ re.findall('[a-h]'+str(i)+r'=\s*(\{\{.+?\}\}|)\s*(?:\n|\|\s*(?=[a-h]\d))', GCLayout[0]) for i in range(10,0,-1) ]

            reEnemyCamp = re.compile(r'\{\{RDTerrain\|color=Enemy\|type=Camp(?: Spawn)?\}\}')
            reEnemySpawn = re.compile(r'\{\{RDTerrain\|color=Enemy\|type=Spawn\}\}')
            reEnemyWarpSpawn = re.compile(r'\{\{RDTerrain\|color=Enemy\|type=Warp Spawn\}\}')
            cellIsKind = lambda a, b, regex: a >= 0 and b >= 0 and a < len(objects1) and b < len(objects1[a]) and regex.search(objects1[a][b])

            # 2 simple spawns.
            if   sum([sum([1 for cell in line if reEnemySpawn.search(cell)]) for line in objects1]) == 2:
                objects0 = [[reEnemySpawn.sub('', cell) for cell in line] for line in objects1]
            # 2 camps.
            elif sum([sum([1 for cell in line if reEnemyCamp.search(cell)]) for line in objects1]) == 2:
                cond = lambda i, j: cellIsKind(i, j, reEnemyWarpSpawn) and any([cellIsKind(i+x, j+y, reEnemyCamp) for x,y in [(0,-1),(0,1),(-1,0),(1,0)]])
                objects0 = [[re.sub('Warp Spawn', 'Warp', cell) if cond(i,j) else cell for j,cell in enumerate(line)] for i,line in enumerate(objects1)]
            # 6 warp spawns.
            # 3 around fortress + 3 around camp. The two opposite around camp are removed.
            elif sum([sum([1 for cell in line if reEnemyWarpSpawn.search(cell)]) for line in objects1]) == 6:
                cond = lambda i, j: cellIsKind(i, j, reEnemyWarpSpawn) and any([cellIsKind(i+x, j+y, reEnemyCamp) and cellIsKind(i+x*2, j+y*2, reEnemyWarpSpawn) for x,y in [(0,-1),(0,1),(-1,0),(1,0)]])
                objects0 = [[re.sub('Warp Spawn', 'Warp', cell) if cond(i,j) else cell for j,cell in enumerate(line)] for i,line in enumerate(objects1)]
            else:
                raise Exception('Failed to recognize an RD pattern: GC ' + str(nGC) + ', ' + o[0])

        except Exception as e:
            print(TODO + str(e))
            self._dup = None
            bg = ''
            objects0 = objects1 = [ ['']*8 ]*10

        key = [[ c + str(n) for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] ] for n in range(10, 0, -1) ]
        s1 = '{{MapLayout|type=RD|baseMap=' + mid + '|backdrop=' + bg + '\n'
        for lKey,lMap in zip(key,objects0):
            for cKey,cMap in zip(lKey,lMap):
                s1 += '| ' + cKey + '=' + cMap + ' '
            s1 = s1[:-1] + '\n'
        s1 += '}}'
        s2 = '{{MapLayout|type=RD|baseMap=' + mid + '|backdrop=' + bg + '\n'
        for lKey,lMap in zip(key,objects1):
            for cKey,cMap in zip(lKey,lMap):
                s2 += '| ' + cKey + '=' + cMap + ' '
            s2 = s2[:-1] + '\n'
        s2 += '}}'
        return {
            'version1': 'Standard', 'mapImage': s1,
            'version2': 'Infernal', 'mapImageV2': s2
        }

RD = RivalDomains