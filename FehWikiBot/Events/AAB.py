#! /usr/bin/env python3

from typing_extensions import Self
from ..Tool import ArticleContainer
from .Reader.AAB import AffinityAutoBattlesReader

class AffinityAutoBattles(ArticleContainer):
    _reader = AffinityAutoBattlesReader
    _linkArticleData = (r'', 'id_tag')

    @ArticleContainer.name.getter
    def name(self) -> str:
        return super().name or 'Affinity Auto-Battles ' + str(self.number)

    @property
    def number(self) -> int:
        from ..Tool.Wiki import Wiki
        return int(Wiki.cargoQuery('AffinityAutoBattles', 'COUNT(DISTINCT _pageName)=Nb', where='StartTime < "'+self.data['avail']['start']+'"', limit=1))+1

    def Infobox(self):
        return super().Infobox('Affinity Auto-Battles', {
            'mapImage': self.MapImage(),
            'bonusTitles': ';'.join(map(str,[0,9])),
            'start': self.data['avail']['start'],
            'end': self.data['avail']['end']
        })
    
    def Availability(self):
        from ..Tool.misc import timeFormat
        return super().Availability('[[Affinity Auto-Battles]]', self.data['avail'],
                                    timeFormat(self.data['avail']['start'], 'Affinity Auto-Battles (%b %Y)'))

    def Rewards(self):
        from ..Utility.Reward import Reward
        s =  '==Rewards==\n'
        s += '===Daily rewards===\n{{#invoke:Reward/AffinityAutoBattles|daily\n'
        for i,r in enumerate(self.data['daily_rewards']):
            s += f" |{i+1}={Reward(r['reward'])}\n"
        s += '}}\n===Score rewards===\n{{#invoke:Reward/AffinityAutoBattles|score\n'
        for i,r in enumerate(self.data['rewards']):
            s += f" |{r['score']}={Reward(r['reward'])}\n"
        s += '}}'
        return s

    def Trivia(self):
        return '==Trivia==\n* This map layout is the same as ' + self.dup + '.'

    def createArticle(self) -> Self:
        if self.data is None: return self
        self.page =  self.Infobox() + '\n'
        self.page += self.Availability() + '\n'
        self.page += self.Rewards() + '\n'
        self.page += self.Trivia() + '\n'
        self.page += '{{Main Events Navbox}}'
        return self

    def MapImage(self) -> str:
        from ..Tool.Wiki import Wiki
        import re

        if self.data['map_id'][0] == 'O':
            page = Wiki.getPageContent('Grand Conquests ' + str((int(self.data['map_id'][1:])-1) // 30 + 1))
            GCLayout = re.search(r'\|\s*(\d+)\s*\n\|\s*\{\{MapLayout\D+'+self.data['map_id']+'.*\n(?:(?!\}\}\n).*\n)+\}\}', page)
            self.dup = 'Area ' + GCLayout[1] + ' of [[Grand Conquests ' + str((int(self.data['map_id'][1:])-1) // 30 + 1) + ']]'
        elif self.data['map_id'][0] == 'Q':
            self.dup = '[[' + Wiki.cargoQuery('Maps',where='Map="'+self.data['map_id']+'"',limit=1) + ']]'
            page = Wiki.getPageContent(self.dup[2:-2])
            GCLayout = re.search(r'\{\{MapLayout\D+' + self.data['map_id'] + '.*\n(?:(?!\}\}\n).*\n)+\}\}', page)

        if not GCLayout: raise Exception('Failed to find the layout of ' + self.data['map_id'])

        bg = re.search(r'backdrop\s*=\s*(\w*)', GCLayout[0])[1]
        objects1 = [ re.findall('[a-h]'+str(i)+r'=\s*(\{\{.+?\}\}|)\s*(?:\n|\|\s*(?=[a-h]\d))', GCLayout[0]) for i in range(10,0,-1) ]

        reEnemyCamp = re.compile(r'\{\{RDTerrain\|color=Enemy\|type=Camp(?: Spawn)?\}\}')
        reEnemySpawn = re.compile(r'\{\{RDTerrain\|color=Enemy\|type=Spawn\}\}')
        reEnemyWarpSpawn = re.compile(r'\{\{RDTerrain\|color=Enemy\|type=Warp Spawn\}\}')
        reWarp = re.compile(r'\{\{RDTerrain\|color=\w+\|type=Warp\}\}')
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
        # Remove all warps
        objects0 = [[reWarp.sub('', cell).replace('Warp ','') for cell in line] for line in objects0]

        key = [[ c + str(n) for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] ] for n in range(10, 0, -1) ]
        s = '{{MapLayout|type=RD|baseMap=' + self.data['map_id'] + '|backdrop=' + bg + '\n'
        for lKey,lMap in zip(key,objects0):
            for cKey,cMap in zip(lKey,lMap):
                s += '| ' + cKey + '=' + cMap + ' '
            s = s[:-1] + '\n'
        s += '}}'
        return s


AAB = AffinityAutoBattles
