#! /usr/bin/env python3

from util import DATA
import util

ITEM_KIND = [
    "Orb", "Hero", "Hero Feather", "Stamina Potion", "Dueling Crest",
    "Light's Blessing",	"Shard","","","",
    "","","Badge","Battle Flag","Sacred Seal",
    "AA Item","Sacred Coin", "Refining Stone", "Divine Dew","Arena Medal",
    "Blessing", "Conquest Lance","Accessory","FB Conversation",	"",
    "Arena Crown", "Heroic Grail","Aether Stone","Throne","Summoning Ticket",
    "Dragonflower","","","","Havoc Axe",
    "Music", "", "Midgard Gem", "", "Divine Code",
    "", "", "", "", "Guardian Shield",
    "Trait Fruit"
]

COLOR = [
    "Universal", "Scarlet", "Azure", "Verdant", "Transparent"
]

AA_ITEM = [
    "Elixir", "Fortifying Horm", "Special Blade", "Infantry Boots", "Naga's Tear",
    "Dancer's Veil", "Lightning Charm", "Panic Charm", "Fear Charm", "Pressure Charm"
]

ELEMENT = [
    "", "Fire", "Water", "Wind", "Earth", "Light", "Dark", "Astra", "Anima"
]

FB_RANK = [
    "C", "B", "A", "S"
]

THRONE = [
    "Golden Throne", "Silver Throne", "Bronze Throne"
]

MOVE = [
    "Infantry", "Armored", "Cavalry", "Flying"
]

AETHER_STONE = {
    'STONE': 'Aether Stone',
    '201811': 'SP Aether Stone',
    '201901': 'Frosty Aether Stone',
    '201902': 'SP Aether Stone',
    '201904': 'Spring Aether Stone',
    '201905': 'SP Aether Stone',
    '201907': 'Summer Aether Stone',
    '201910': 'Fall Aether Stone',
    '202001': 'Frosty Aether Stone',
    '202002': 'SP Aether Stones',
}

DIVINE_CODES = {
    '2020': ": Part 1",
    '202003': ": Ephemera 3",
    '202004': ": Ephemera 4",
    '202005': ": Ephemera 5",
    '202006': ": Ephemera 6",
    '202007': ": Ephemera 7",
    '202008': ": Ephemera 8",
    '202009': ": Ephemera 9",
    '202010': ": Ephemera 10",
    '202011': ": Ephemera 11",
    '202012': ": Ephemera 12",
}

def parseReward(rewards: list):
    s = ""
    for reward in rewards:
        if reward != rewards[0]:
            s += ';'
        kind = ITEM_KIND[reward['kind']] if len(ITEM_KIND) > reward['kind'] and ITEM_KIND[reward['kind']] != "" else (f"<!--{reward['_type']}-->")

        if kind == "Hero":
            s += "{hero=" + util.getName(reward['id_tag']) + ";rarity=" + str(reward['rarity']) + "}"
        elif kind == "FB Conversation":
            s += "{hero=" + DATA['M' + reward['id_tag']] + ";fbrank=" + (FB_RANK[reward['support_rank']] or reward['support_rank']) + "}"
        elif kind == "Accessory":
            s += "{accessory=" + util.getName(reward['id_tag']) + "}"
        elif kind == "Sacred Seal":
            s += "{seal=" + DATA['M' + reward['id_tag']] + "}"
        else:
            if kind == "Shard":
                kind = COLOR[reward['shard_color']] + (reward['great'] and ' Crystal' or ' Shard')
            elif kind == "Badge":
                kind = (reward['great'] and 'Great ' or '') + COLOR[reward['badge_color']+1] + ' Badge'
            elif kind == 'Aether Stone':
                kind = AETHER_STONE[reward['id_tag']] or (reward['id_tag'] + 'Aether Stone')
            elif kind == 'Summoning Ticket':
                kind = f"<!--Summoning Ticket: {[reward['id_tag']]}-->"
            elif kind == 'Dragonflower':
                kind = 'Dragonflower (' + MOVE[reward['move_type']][0] + ')'
            elif kind == 'Blessing':
                kind = ELEMENT[reward['element']] + ' Blessing'
            elif kind == 'Divine Code':
                kind += DIVINE_CODES[reward['id_tag']]
            s += "{kind=" + kind + (reward['count'] != 1 and (";count=" + str(reward['count'])) or "") + "}"

    return len(rewards) > 1 and ('[' + s + ']') or s
