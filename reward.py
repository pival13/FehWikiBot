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
    "Music", "Forma Torch", "Midgard Gem", "", "Divine Code",
    "", "", "", "Forma Soul", "Guardian Shield",
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

WEAPON = [
    "Sword", "Lance", "Axe",
    "Red Bow", "Blue Bow", "Green Bow", "Colorless Bow",
    "Red Dagger", "Blue Dagger", "Green Dagger", "Colorless Dagger",
    "Red Tome", "Blue Tome", "Green Tome", "Colorless Tome",
    "Staff",
    "Red Breath", "Blue Breath", "Green Breath", "Colorless Breath",
    "Red Beast", "Blue Beast", "Green Beast", "Colorless Beast",
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
    '202012': 'Frosty Aether Stones',
}

DIVINE_CODES = {
    '2020': ": Part 1",
    '2021': ": Part 2",
}

def parseReward(rewards: list):
    s = ""
    for reward in rewards:
        if reward != rewards[0]:
            s += ';'
        kind = ""
        if reward['kind'] == -1: kind = reward['_type']
        elif len(ITEM_KIND) > reward['kind'] and ITEM_KIND[reward['kind']] != "": kind = ITEM_KIND[reward['kind']]
        else: kind = f"<!--{reward['_type']}-->"

        if kind == "Hero":
            s += "{hero=" + util.getName(reward['id_tag']) + ";rarity=" + str(reward['rarity']) + "}"
        elif kind == "FB Conversation":
            s += "{hero=" + util.getName(reward['id_tag']) + ";fbrank=" + (FB_RANK[reward['support_rank']] or reward['support_rank']) + "}"
        elif kind == "Accessory":
            s += "{accessory=" + util.getName(reward['id_tag']) + "}"
        elif kind == "Sacred Seal":
            s += "{seal=" + util.getName(reward['id_tag']) + "}"
        else:
            if kind == "Shard":
                kind = COLOR[reward['shard_color']] + (reward['great'] and ' Crystal' or ' Shard')
            elif kind == "Badge":
                kind = (reward['great'] and 'Great ' or '') + COLOR[reward['badge_color']+1] + ' Badge'
            elif kind == 'Aether Stone':
                kind = AETHER_STONE[reward['id_tag']] if reward['id_tag'] in AETHER_STONE else ('<!--'+reward['id_tag'] + ' Aether Stone-->')
            elif kind == 'Summoning Ticket':
                kind = f"<!--Summoning Ticket: {[reward['id_tag']]}-->"
            elif kind == 'Dragonflower':
                kind = 'Dragonflower (' + MOVE[reward['move_type']][0] + ')'
            elif kind == 'Blessing':
                kind = ELEMENT[reward['element']] + ' Blessing'
            elif kind == 'Divine Code':
                if len(reward['id_tag']) == 6:
                    kind += f": Ephemera {int(reward['id_tag'][-2:])}"
                else:
                    kind += DIVINE_CODES[reward['id_tag']]
            s += "{kind=" + kind + (reward['count'] != 1 and (";count=" + str(reward['count'])) or "") + "}"

    return len(rewards) > 1 and ('[' + s + ']') or s
