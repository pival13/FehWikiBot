#! /usr/bin/env python3

import util
from globals import ITEM_KIND, AA_ITEM, COLOR, BLESSING_ELEMENT, SUPPORT_RANK, MOVE_TYPE

def parseReward(rewards: list):
    s = []
    for reward in rewards:
        kind = ITEM_KIND[reward['kind']] if reward['kind'] in ITEM_KIND else f"<!--{reward['_type']}-->"

        if kind == "Hero":
            s += ["{hero=" + util.getName(reward['id_tag']) + ";rarity=" + str(reward['rarity']) + "}"]
        elif kind == "FB Conversation":
            s += ["{hero=" + util.getName(reward['id_tag']) + ";fbrank=" + (SUPPORT_RANK[reward['support_rank']] or reward['support_rank']) + "}"]
        elif kind == "Accessory":
            s += ["{accessory=" + util.getName(reward['id_tag']) + "}"]
        elif kind == "Sacred Seal":
            s += ["{seal=" + util.getName(reward['id_tag']) + "}"]
        else:
            if kind == "Shard":
                kind = COLOR[reward['shard_color']] + (reward['great'] and ' Crystal' or ' Shard')
            elif kind == "Badge":
                kind = (reward['great'] and 'Great ' or '') + COLOR[reward['badge_color']+1] + ' Badge'
            elif kind == 'AA Item':
                kind = AA_ITEM[reward['aa_kind']]
            elif kind == 'Aether Stone':
                if reward['id_tag'] != 'STONE': kind = f"<!--{reward['id_tag']} Aether Stone-->"
            elif kind == 'Summoning Ticket':
                kind = f"<!--Summoning Ticket: {[reward['id_tag']]}-->"
            elif kind == 'Dragonflower':
                kind = 'Dragonflower (' + MOVE_TYPE[reward['move_type']][0] + ')'
            elif kind == 'Blessing':
                kind = BLESSING_ELEMENT[reward['element']] + ' Blessing'
            elif kind == 'Divine Code':
                if len(reward['id_tag']) == 6:
                    kind += f": Ephemera {int(reward['id_tag'][-2:])}"
                elif len(reward['id_tag']) == 4:
                    kind += f": Part {int(reward['id_tag'])-2019}"
                else:
                    kind = f"<!--Divine Code: {reward['id_tag']}-->"
            s += ["{kind=" + kind + (reward['count'] != 1 and (";count=" + str(reward['count'])) or "") + "}"]

    return ('[' + ';'.join(s) + ']') if len(s) > 1 else s[0] if s != [] else ""
