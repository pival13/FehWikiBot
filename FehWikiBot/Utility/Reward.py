#! /usr/bin/env python3

class Reward:
    def __init__(self, obj: dict | list[dict]):
        self._obj = obj if isinstance(obj,list) else [obj]

    def __str__(self) -> str:
        from ..Utility.Units import Heroes
        from ..Skills import SacredSeals
        from ..Others.Accessory import Accessories
        from ..Others.AetherRaids import AetherRaidsItem
        s = []
        for r in self._obj:
            kind = r['kind']
            if kind[:8] == 'Unknow (':
                s.append('{kind=<!-- '+kind+' -->}')
            elif kind == 'Hero':
                s.append('{hero=' + Heroes.get(r['id_tag']).name + ';rarity=' + str(r['rarity']) + '}')
            elif kind == 'FB Conversation':
                s.append('{hero=' + Heroes.get(r['id_tag']).name + ';fbrank=' + r['rank'] + '}')
            elif kind == 'Accessory':
                s.append('{accessory=' + Accessories.get(r['id_tag']).name + '}')
            elif kind == 'Sacred Seal':
                s.append('{seal=' + SacredSeals.get(r['id_tag']).skill.name + '}')
            else:
                if kind == 'Shard':
                    kind = r['color'] + ' ' + (r['great'] and 'Crystal' or 'Shard')
                elif kind == 'Badge':
                    kind = (r['great'] and 'Great ' or '') + r['color'] + ' Badge'
                elif kind == 'AA Item':
                    kind = r['item']
                elif kind == 'Blessing':
                    kind = r['element'] + ' Blessing'
                elif kind == 'AR Item':
                    kind = AetherRaidsItem.get(r['id_tag']).name
                elif kind == 'Summoning Ticket':
                    kind = '<!--Summoning Ticket: ' + r['id_tag'] + '-->' # TODO Get type (Special/Regular/I-VII)
                elif kind == 'Dragonflower':
                    kind = 'Dragonflower (' + r['move'][0] + ')'
                elif kind == 'Divine Code':
                    if len(r['id_tag']) == 6:
                        kind = 'Divine Code: Ephemera ' + str(int(r['id_tag'][-2:]))
                    elif len(r['id_tag']) == 4:
                        kind += 'Divine Code: Part ' + str(int(r['id_tag'])-2019)
                    else:
                        kind = f'<!--Divine Code: ' + r['id_tag'] + '-->'
                s.append('{kind=' + kind + (r['count'] != 1 and (';count=' + str(r['count'])) or '') + '}')
        return ('[' + ';'.join(s) + ']') if len(s) > 1 else s[0] if s != [] else ''


def Rewards(obj: dict[str,dict|list[dict]], indent=2) -> str:
    ret = []
    for k,v in obj.items():
        ret.append(k + '=' + str(Reward(v)) + ';')
    indent = '\n' + (' '*indent)
    return '{' + indent + indent.join(ret) + '\n}'