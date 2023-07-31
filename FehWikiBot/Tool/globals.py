#! /usr/bin/env python3

#! /usr/bin/env python3

from datetime import datetime as _datetime

__all__ = [
    'TODO', 'ERROR', 'TIME_FORMAT', 'MIN_TIME', 'MAX_TIME',
    'DIFFICULTIES', 'ROMAN', 'COLOR',
    'MOVE_TYPE', 'WEAPON_TYPE', 'WEAPON_CATEGORY', 'WEAPON_MASK', 'REFINE_TYPE',
    'ITEM_KIND'
]

GREEN_TEXT = '\33[1;92m'
GREY_TEXT = '\33[1;30m'
YELLOW_BG = '\33[1;30;103m'
RED_BG = '\33[1;37;101m'
RESET_TEXT = '\33[0m'
TODO = f'{YELLOW_BG}TODO{RESET_TEXT}: '
WARNING = f'{YELLOW_BG}WARNING{RESET_TEXT}: '
ERROR = f'{RED_BG}ERROR{RESET_TEXT}: '

TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
MIN_TIME = _datetime.utcfromtimestamp(0).strftime(TIME_FORMAT)
MAX_TIME = _datetime.utcfromtimestamp(0x7FFFFFFF).strftime(TIME_FORMAT)

DIFFICULTIES = ['Normal', 'Hard', 'Lunatic', 'Infernal', 'Abyssal']
ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

MOVE_TYPE = [ 'Infantry', 'Armored', 'Cavalry', 'Flying' ]
WEAPON_TYPE = [
    'Red Sword',  'Blue Lance',  'Green Axe',
    'Red Bow',    'Blue Bow',    'Green Bow',    'Colorless Bow',
    'Red Dagger', 'Blue Dagger', 'Green Dagger', 'Colorless Dagger',
    'Red Tome',   'Blue Tome',   'Green Tome',   'Colorless Tome',
                                                 'Colorless Staff',
    'Red Breath', 'Blue Breath', 'Green Breath', 'Colorless Breath',
    'Red Beast',  'Blue Beast',  'Green Beast',  'Colorless Beast',
]

WEAPON_CATEGORY = {
    0b111111111111111111111111: 'All',
    0b000000000000000000000000: 'None',

    0b111111110000000000000111: 'Close',
    0b000000001111111111111000: 'Ranged',

    0b111100000000011111111111: 'Physical',
    0b000011111111100000000000: 'Magical',

    0b000000000000011111111000: 'Missile',

    0b000100010000100010001001: 'Red',
    0b001000100001000100010010: 'Blue',
    0b010001000010001000100100: 'Green',
    0b100010001100010001000000: 'Colorless',

    0b000000000000000000000111: 'Melee',
    0b000000000000000001111000: 'Bow',
    0b000000000000011110000000: 'Dagger',
    0b000000000111100000000000: 'Magic',
    0b000011110000000000000000: 'Dragonstone',
    0b111100000000000000000000: 'Beast',

    0b000000000000000000000001: 'Sword',
    0b000000000000000000000010: 'Lance',
    0b000000000000000000000100: 'Axe',
    0b000000000000000000001000: 'Red Bow',
    0b000000000000000000010000: 'Blue Bow',
    0b000000000000000000100000: 'Green Bow',
    0b000000000000000001000000: 'Colorless Bow',
    0b000000000000000010000000: 'Red Dagger',
    0b000000000000000100000000: 'Blue Dagger',
    0b000000000000001000000000: 'Green Dagger',
    0b000000000000010000000000: 'Colorless Dagger',
    0b000000000000100000000000: 'Red Tome',
    0b000000000001000000000000: 'Blue Tome',
    0b000000000010000000000000: 'Green Tome',
    0b000000000100000000000000: 'Colorless Tome',
    0b000000001000000000000000: 'Colorless Staff',
    0b000000010000000000000000: 'Red Dragonstone',
    0b000000100000000000000000: 'Blue Dragonstone',
    0b000001000000000000000000: 'Green Dragonstone',
    0b000010000000000000000000: 'Colorless Dragonstone',
    0b000100000000000000000000: 'Red Beast',
    0b001000000000000000000000: 'Blue Beast',
    0b010000000000000000000000: 'Green Beast',
    0b100000000000000000000000: 'Colorless Beast',
}
WEAPON_MASK = {weapon: mask for mask, weapon in WEAPON_CATEGORY.items()}

REFINE_TYPE = {1: 'Skill1', 2: 'Skill2', 101: 'Atk', 102: 'Spd', 103: 'Def', 104: 'Res'}

ITEM_KIND = {
    0: 'Orb', 1: 'Hero', 2: 'Hero Feather', 3: 'Stamina Potion',
    4: 'Dueling Crest', 5: 'Light\'s Blessing', 6: 'Shard', 12: 'Badge',
    13: 'Battle Flag', 14: 'Sacred Seal', 15: 'AA Item', 16: 'Sacred Coin',
    17: 'Refining Stone', 18: 'Divine Dew', 19: 'Arena Medal',
    20: 'Blessing', 21: 'Conquest Lance', 22: 'Accessory',
    23: 'FB Conversation', 25: 'Arena Crown', 26: 'Heroic Grail',
    27: 'AR Item', 28: 'Throne', 29: 'Summoning Ticket',
    30: 'Dragonflower', 33: 'R&R Affinity', 34: 'Havoc Axe', 35: 'Music', 36: 'Forma Torch',
    37: 'Midgard Gem', 39: 'Divine Code', 43: 'Forma Soul', 
    44: 'Guardian Shield', 45: 'Trait Fruit', 50: 'Binding Torch',
    'Lost Lore Team': 'Lost Lore Team', 'Memento Points': 'Memento Point'
}

COLOR = [
    'Universal', 'Scarlet', 'Azure', 'Verdant', 'Transparent'
]

BLESSING = [
    '', 'Fire', 'Water', 'Wind', 'Earth', 'Light', 'Dark', 'Astra', 'Anima'
]
