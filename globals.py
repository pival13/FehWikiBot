#! /usr/bin/env python3

import json
from datetime import datetime
from util import fetchFehData, getName

from util import DATA, SOUNDS, BGMS

from util import URL, TODO, ERROR, TIME_FORMAT
MIN_TIME = datetime.utcfromtimestamp(0).strftime(TIME_FORMAT)
MAX_TIME = datetime.utcfromtimestamp(0x7FFFFFFF).strftime(TIME_FORMAT)
DIFFICULTIES = ['Normal', 'Hard', 'Lunatic', 'Infernal', 'Abyssal']
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

_persons = fetchFehData("Common/SRPG/Person", False)
_enemies = fetchFehData("Common/SRPG/Enemy", False)

UNITS = {u['id_tag']: u for u in _enemies + _persons}
UNIT_NAMES = {getName(u['id_tag']): u for u in _enemies + _persons}
RESPLENDENTS = fetchFehData("Common/SubscriptionCostume", 'hero_id')

UNIT_IMAGE = {u['face_name2']: u for u in _enemies + _persons}
UNIT_IMAGE.update({
    "ch00_00_Eclat_X_Normal":       {'name': "Kiran"},
    "ch00_00_Eclat_X_Avatar00":     {'name': "Kiran: Hero Summoner",    'id_tag': "EID_アバター"},
    "ch00_00_Eclat_M_Avatar01":     {'name': "Kiran: Hero Summoner M01"},
    "ch00_00_Eclat_M_Avatar02":     {'name': "Kiran: Hero Summoner M02"},
    "ch00_00_Eclat_M_Avatar03":     {'name': "Kiran: Hero Summoner M03"},
    "ch00_00_Eclat_M_Avatar04":     {'name': "Kiran: Hero Summoner M04"},
    "ch00_00_Eclat_F_Avatar01":     {'name': "Kiran: Hero Summoner F01"},
    "ch00_00_Eclat_F_Avatar02":     {'name': "Kiran: Hero Summoner F02"},
    "ch00_00_Eclat_F_Avatar03":     {'name': "Kiran: Hero Summoner F03"},
    "ch00_00_Eclat_F_Avatar04":     {'name': "Kiran: Hero Summoner F04"},
    "ch00_13_Gustaf_M_Normal":      {'name': "Gustav",                  'id_tag': 'PID_グスタフ'},
    "ch00_14_Henriette_F_Normal":   {'name': "Henriette",               'id_tag': 'PID_ヘンリエッテ'},
    "ch00_16_Freeze_M_Normal":      {'name': "Hríd"},
    "ch00_22_Tor_F_Normal":         {'name': "Thórr",                   'id_tag': 'PID_トール'},
    "ch00_35_Eitri_F_Normal":       {'name': 'Eitri',                   'id_tag': 'EID_エイトリ'},
    "ch00_36_MysteryHood_X_Normal": {'name': 'Mystery Hood'},
    "ch90_02_FighterAX_M_Normal":   {'name': ''} # This is the tag used for non-face unit on scenarios
})

SKILLS = fetchFehData("Common/SRPG/Skill")
WEAPONS = {skillTag: SKILLS[skillTag] for skillTag in SKILLS if SKILLS[skillTag]['might'] != 0}
SEALS = fetchFehData('Common/SRPG/SkillAccessory')

# Dict[orig_tag, list[ref]]
REFINES = {}
for refine in fetchFehData('Common/SRPG/WeaponRefine', None):
    REFINES[refine['orig']] = (REFINES[refine['orig']] if refine['orig'] in REFINES else []) + [refine]
CREATABLE_SEALS = fetchFehData('Common/SRPG/SkillAccessoryCreatable')

MOVE_TYPE = [ "Infantry", "Armored", "Cavalry", "Flying" ]
WEAPON_TYPE = [
    "Sword", "Lance", "Axe",
    "Red Bow", "Blue Bow", "Green Bow", "Colorless Bow",
    "Red Dagger", "Blue Dagger", "Green Dagger", "Colorless Dagger",
    "Red Tome", "Blue Tome", "Green Tome", "Colorless Tome",
    "Staff",
    "Red Breath", "Blue Breath", "Green Breath", "Colorless Breath",
    "Red Beast", "Blue Beast", "Green Beast", "Colorless Beast",
]

WEAPON_CATEGORY = {
    0b111111111111111111111111: "All",
    0b000000000000000000000000: "None",

    0b111111110000000000000111: "Close",
    0b000000001111111111111000: "Ranged",

    0b111100000000011111111111: "Physical",
    0b000011111111100000000000: "Magical",

    0b000000000000011111111000: "Missile",

    0b000100010000100010001001: "Red",
    0b001000100001000100010010: "Blue",
    0b010001000010001000100100: "Green",
    0b100010001100010001000000: "Colorless",

    0b000000000000000000000111: "Melee",
    0b000000000000000001111000: "Bow",
    0b000000000000011110000000: "Dagger",
    0b000000000111100000000000: "Magic",
    0b000011110000000000000000: "Dragonstone",
    0b111100000000000000000000: "Beast",

    0b000000000000000000000001: "Sword",
    0b000000000000000000000010: "Lance",
    0b000000000000000000000100: "Axe",
    0b000000000000000000001000: "Red Bow",
    0b000000000000000000010000: "Blue Bow",
    0b000000000000000000100000: "Green Bow",
    0b000000000000000001000000: "Colorless Bow",
    0b000000000000000010000000: "Red Dagger",
    0b000000000000000100000000: "Blue Dagger",
    0b000000000000001000000000: "Green Dagger",
    0b000000000000010000000000: "Colorless Dagger",
    0b000000000000100000000000: "Red Tome",
    0b000000000001000000000000: "Blue Tome",
    0b000000000010000000000000: "Green Tome",
    0b000000000100000000000000: "Colorless Tome",
    0b000000001000000000000000: "Colorless Staff",
    0b000000010000000000000000: "Red Dragonstone",
    0b000000100000000000000000: "Blue Dragonstone",
    0b000001000000000000000000: "Green Dragonstone",
    0b000010000000000000000000: "Colorless Dragonstone",
    0b000100000000000000000000: "Red Beast",
    0b001000000000000000000000: "Blue Beast",
    0b010000000000000000000000: "Green Beast",
    0b100000000000000000000000: "Colorless Beast",
}
WEAPON_MASK = {weapon: mask for mask, weapon in WEAPON_CATEGORY.items()}

ACCESSORIES = fetchFehData("Common/DressAccessory/Data", "sprite")

REFINE_TYPE = {1: 'Skill1', 2: 'Skill2', 101: 'Atk', 102: 'Spd', 103: 'Def', 104: 'Res'}

ITEM_KIND = {
    0: "Orb", 1: "Hero", 2: "Hero Feather", 3: "Stamina Potion",
    4: "Dueling Crest", 5: "Light's Blessing", 6: "Shard", 12: "Badge",
    13: "Battle Flag", 14: "Sacred Seal", 15: "AA Item", 16: "Sacred Coin",
    17: "Refining Stone", 18: "Divine Dew", 19: "Arena Medal",
    20: "Blessing", 21: "Conquest Lance", 22: "Accessory",
    23: "FB Conversation", 25: "Arena Crown", 26: "Heroic Grail",
    27: "Aether Stone", 28: "Throne", 29: "Summoning Ticket",
    30: "Dragonflower", 34: "Havoc Axe", 35: "Music", 36: "Forma Torch",
    37: "Midgard Gem", 39: "Divine Code", 43: "Forma Soul", 
    44: "Guardian Shield", 45: "Trait Fruit",
    'Lost Lore Team': 'Lost Lore Team', 'Memento Points': 'Memento Point'
}

AA_ITEM = [
    "Elixir", "Fortifying Horm", "Special Blade", "Infantry Boots", "Naga's Tear",
    "Dancer's Veil", "Lightning Charm", "Panic Charm", "Fear Charm", "Pressure Charm"
]

COLOR = [
    "Universal", "Scarlet", "Azure", "Verdant", "Transparent"
]

BLESSING_ELEMENT = [
    "", "Fire", "Water", "Wind", "Earth", "Light", "Dark", "Astra", "Anima"
]

SUPPORT_RANK = [
    "C", "B", "A", "S"
]
