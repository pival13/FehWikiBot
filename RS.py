#! /usr/bin/env python3

from datetime import datetime
from math import trunc
from os.path import isfile

import util
from globals import DATA, WEAPON_CATEGORY, UNITS
from Reverse import reverseRokkrSieges
from reward import parseReward

def getStats(unitId: str, rarity: int=5, level: int=40):
    unit = UNITS[unitId]
    stats = {}
    statsOrder = list(unit['base_stats'].keys())
    statsOrder.sort(key=lambda k: unit['base_stats'][k], reverse=True)
    for key in unit['base_stats']:
        stats[key] = unit['base_stats'][key] - 1 + trunc((level - 1) * trunc(unit['growth_rates'][key] * (0.79+0.07*rarity)) / 100)
    for i in range(1, rarity):
        if i % 2 == 1:
            stats[statsOrder[1]] += 1
            stats[statsOrder[2]] += 1
        else:
            stats[statsOrder[0]] += 1
            stats[statsOrder[3]] += 1
            stats[statsOrder[4]] += 1
    return stats

def RSInfobox(data: dict, nb: int):
    units = []
    for unitGr in data['units']:
        for unit in unitGr:
            if not unit['id_tag'] in units: units += [unit['id_tag']]
    return "{{Rokkr Sieges Infobox\n" + \
        f"|number={nb}\n" + \
        f"|rokkrs={','.join([util.getName(u) for u in units])}\n" + \
        f"|startTime={data['battle_avail'][0]['start']}\n" + \
        f"|endTime={util.timeDiff(data['event_avail']['finish'])}\n" + \
        "}}"

def RSAvailability(data: dict):
    s = "==Availability==\nThis [[Røkkr Sieges]] event was made available:\n" + \
        f"* {{{{HT|{data['event_avail']['start']}}}}} – {{{{HT|{util.timeDiff(data['event_avail']['finish'])}}}}} " + \
        f"([[Røkkr Sieges ({datetime.strptime(data['battle_avail'][0]['start'], util.TIME_FORMAT).strftime('%b %Y').replace(' 0', ' ')}) (Notification)|Notification]])"
    for i, battle in enumerate(data['battle_avail']):
        s += f"\n** '''Battle {i+1}''': " + \
            f"{{{{HT|{battle['start']}}}}} – " + \
            f"{{{{HT|{util.timeDiff(battle['finish'])}}}}}"
    return s

def RSRewards(data: dict):
    s = "==Rewards==\n"
    
    s += "===Total damage===\nThe same items are rewarded in all three rounds.\n"
    s += "{{#invoke:Reward/RokkrSieges|total|time=" + data['battle_avail'][0]['start'] + "\n"
    for r in data['rewards']:
        if r['type'] == 1 and r['battle'] == 0:
            s += f" |{r['score_rank_hi']}=" + parseReward(r['reward']) + "\n"
    
    s += "}}\n===Rank===\nThe same items are rewarded in all three rounds.\n"
    s += "{{#invoke:Reward/RokkrSieges|rank|time=" + data['battle_avail'][0]['start'] + "\n"
    for r in data['rewards']:
        if r['type'] == 2 and r['battle'] == 0:
            s += f" |{r['score_rank_hi']}~{r['score_rank_lo'] if r['score_rank_lo'] > 0 else ' '}=" + parseReward(r['reward']) + "\n"
    
    s += "}}\n===World Damage Rewards===\nThe same items are rewarded in all three rounds.\n"
    s += "{{#invoke:Reward/RokkrSieges|world|time=" + data['battle_avail'][0]['start'] + "\n"
    length = len(str(data['rewards'][-1]['score_rank_hi']))
    for r in data['rewards']:
        if r['type'] == 3 and r['battle'] == 0:
            score = "{{:>{}}}~{{:>{}}}".format(length, length).format(r['score_rank_hi'],r['score_rank_lo'] if r['score_rank_lo'] > 0 else '')
            s += f" |{score}=" + parseReward(r['reward']) + "\n"
    
    s += "}}\n===Damage to Røkkr Rewards===\nEach Røkkr boss features its own set of rewards.\n{{#invoke:Reward/RokkrSieges|max\n"
    for i, r in enumerate(data['rokkr_damage_rewards']):
        if r['id'] != data['rokkr_damage_rewards'][i-1]['id']:
            s += ('}\n' if i != 0 else '') + f"|{r['id'] + 1}={{\n"
            s += f"  boss={util.getName(data['units'][0][r['id']]['id_tag'])};\n"
            battleNb = [(r['battle'] >> i) & 1 for i in range(8)].index(1)
            s += f"  since={data['battle_avail'][battleNb]['start']};\n"
        s += f"  {r['score']}=" + parseReward(r['reward']) + ';\n'

    s += "}\n}}\n'''Note''': If you reveive an accessory that you already have, you will obtain 300 {{It|Hero Feather}}s instead."
    return s

def RSUnits(data: dict):
    nameToWeapon = lambda id: WEAPON_CATEGORY[1 << UNITS[id]['weapon_type']].replace('Tome','Magic').replace('Red ','').replace('Blue ','').replace('Green ','').replace('Colorless ','')
    s = "==Unit data=="
    for iBattle in range(3):
        s += f"\n===Battle {iBattle+1}===\n{{{{#invoke:UnitData|main|no cargo=true|no ai=true\n"
        for iDiff, diffUnits in enumerate(data['units']):
            unitData = data['unit_data_common'][iDiff]
            s += f"|Lv. {unitData['level']} ({DATA['MID_SHADOW_STAGE_DIFFICULY_'+str(iDiff)]})=[\n"
            for i in range(2):
                unit = diffUnits[iBattle * 2 + i]
                stats = getStats(unit['id_tag'], unitData['rarity'], unitData['level'])
                s += "{unit=" + util.getName(unit['id_tag'])
                s += f";rarity={unitData['rarity']};slot=-"
                s += f";level={unitData['level']};"
                s += f"stats=[??;{';'.join([str(unitData['stats'][key] + trunc(stats[key]/5) + unit['stat_modifier'][key]) for key in ['atk','spd','def','res']])}];"
                s += f";weapon=Umbra Burst ({nameToWeapon(unit['id_tag'])})"
                s += f";assist={util.getName(unit['assist']) if unit['assist'] else '-'}"
                s += f";special={util.getName(unitData['special'])}"
                s += f";a={util.getName(unit['a']) if unit['a'] else '-'}"
                s += f";b={util.getName(unit['b']) if unit['b'] else '-'}"
                s += f";c={util.getName(unit['c']) if unit['c'] else '-'}"
                s += f";seal=" + util.getName(unitData['seal']) + "};\n"
            s += "]\n"
        s += "}}"
    return s

def RokkrSieges(tag: str):
    datas = reverseRokkrSieges(tag)

    ret = {}
    for data in datas:
        nb = int(util.cargoQuery('RokkrSieges', 'COUNT(_pageName)=Nb')[0]['Nb']) + 1
        s = RSInfobox(data, nb) + "\n"
        s += RSAvailability(data) + "\n"
        s += RSRewards(data) + "\n"
        s += "==Maps==\n<!--" + "\n".join(["{{MapLayout G000X}}"] * 6) + "-->" + "\n"
        s += RSUnits(data) + "\n"
        s += "==Trivia==\n*\n{{Main Events Navbox}}"
        ret[f"Røkkr Sieges {nb}"] = s
    return ret

from sys import argv

if __name__ == '__main__':
    if len(argv) <= 1:
        print("Enter at least one update tag")
        exit(1)
    for arg in argv[1:]:
        if not isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Shadow/' + arg + '.bin.lz'):
            print(f'No Røkkr Sieges are related to the tag "{arg}"')
            continue
        rss = RokkrSieges(arg)
        for rs in rss:
            print(rs, rss[rs])