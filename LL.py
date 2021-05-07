#! /usr/bin/env python3

import json
import re
from os.path import isfile
from num2words import num2words

from util import DATA, DIFFICULTIES
import util
from Reverse import reverseLostLore
from reward import parseReward, MOVE, WEAPON
from mapUtil import InOtherLanguage, Availability

extraTeams = [20,60]

def LLInfobox(data: dict, strikes: list):
    foes = []
    for strike in strikes: foes += [util.getName(f"MID_TRIP_ENEMY_{strike['id_tag']}_{enemy['name_id']}") for enemy in strike['units']]
    return "{{Lost Lore Infobox\n" + \
        f"|name={util.getName('MID_TRIP_TITLE_' + data['id_tag'])}\n" + \
        f"|world={util.getName('MID_TRIP_WORLD_'+'_'.join([str(d) for d in data['bonusEntry']][:data['entryCount']]))}\n" + \
        f"|locations={','.join([util.getName('MID_TRIP_PLACE_'+d['id_tag']) for d in data['maps']])}\n" + \
        f"|strikeFoes=" + ",".join(list(dict.fromkeys(foes))) + "\n" + \
        f"|startTime={data['avail']['start']}\n" + \
        f"|endTime={util.timeDiff(data['avail']['finish'])}"+"\n}}"

def LLRewards(data: dict):
    s = "==Rewards==\n{{#invoke:Reward/LostLore|lines|extraTeams=" + ",".join([str(t) for t in extraTeams]) + "\n"
    for r in data['loreRewards']:
        if int(r['lines'] / 3600) in extraTeams: r['reward'] += [{"kind": -1, "_type": "Lost Lore Team", "count": 1}]
        #First format will transform it into {:<nb}, second format will return the number right padded to nb spaces
        score = "{{:<{}}}".format(len(str(int(data['loreRewards'][-1]['lines']/3600)))).format(int(r['lines']/3600))
        s += f" | {score} = " + parseReward(r['reward']) + "\n"
    return s + "}}"

def LLSaga(data: dict, tag: str):
    s = "==Heroes' Saga==\n{| class=\"wikitable\" style=\"text-align: center;font-family:feh\"\n" + \
        "!rowspan=\"2\"|Act\n!colspan=\"2\"|Heroes' Saga\n!rowspan=\"2\"|Image\n|-\n" + \
        "!style=\"width:20em;\"|English\n!style=\"width:20em;\"|Japanese\n|-\n"
    name = util.cleanStr(util.getName('MID_TRIP_TITLE_'+data['id_tag']))
    fileJPJA = {d['key']: d['value'] for d in util.readFehData("JPJA/Message/Data/Data_" + tag + ".json")}
    messageJp = fileJPJA['MID_TRIP_SAGA_'+data['id_tag']+'_PROLOGUE'].replace('\n', '<br>')
    s += "|Prologue\n|"+util.getName('MID_TRIP_SAGA_'+data['id_tag']+'_PROLOGUE').replace('\n', '<br>')+"\n" + \
        f"|lang=\"ja\"|{messageJp}\n" + \
        f"|rowspan=\"2\"|[[File:{name} Prologue.png|300px]]\n"
    s += f"|-\n|1st Act\n|\n|lang=\"ja\"|\n"
    s += f"|-\n|2nd Act\n|\n|lang=\"ja\"|\n|[[File:{name} Act 2.png|300px]]\n"
    s += f"|-\n|3rd Act\n|\n|lang=\"ja\"|\n|rowspan=\"2\"|[[File:{name} Act 3.png|300px]]\n"
    s += f"|-\n|4th Act\n|\n|lang=\"ja\"|\n"
    s += f"|-\n|Final Act\n|\n|lang=\"ja\"|\n|[[File:{name} Final Act.png|300px]]\n"
    return s + "|}"

def LLLocation(data: dict):
    require = {}
    for location in data["maps"]:
        loc = {
            "name": util.getName(f"MID_TRIP_PLACE_{location['id_tag']}"),
            "image": re.sub(r".+/([^/]+)\..*", r"\1.webp", location['backgroundPath']),
            ("linesReq" if location['lines'] != 0 else "isCombat"): int(location['lines'] / 3600) if location['lines'] != 0 else 1,
            "rewards": parseReward(location['clearReward'] + [{"kind": -1, "_type": "Saga's " + util.getName(f"MID_TRIP_SAGA_SECTION_{data['maps'].index(location)+1}"), "count": 1}])
        }
        #Convert a json object into lua object
        loc = re.sub('": "?', "=", re.sub(r'"?, "', ";", json.dumps(loc).replace("{\"", "{").replace("\"}", "}")))
        req = ",".join([str(d["map_idx"]) for d in location['required'] if d["map_idx"] != -1])
        if (req or "") in require: require[req or ""] += [loc]
        else: require[req or ""] = [loc]
    locations = list(require.values())
    for i in range(len(locations)):
        if len(locations[i]) == 1:
            locations[i] = "[" + locations[i][0] + "]"
        else:
            locations[i] = "[\n  " + ";\n  ".join(locations[i]) + ";\n ]"
    return "==Locations==\n{{#invoke:Reward/LostLore|location|extraTeams=" + ",".join([str(t) for t in extraTeams]) + "\n" + \
        "|locations=[\n " + ";\n ".join(locations) + ";\n]}}"

def LLUnit(data: dict, strikes: list):
    s = "==Unit data==\n"
    for i, strike in enumerate(strikes):
        if len(strikes) != 1: s += f"===Strike {i+1}===\n"
        s += "{|class=\"wikitable\" style=\"text-align:center;\"\n!Foe!!HP!!Atk!!Spd!!Def!!Res\n"
        for foe in strike['units']:
            s += "|-\n|{{LostLoreEnemy\n|file=" + re.sub(r".*/([^/]*)\..*", r"\1.webp", foe["facePath"]) + "|size=100\n"
            s += f"|rarity={foe['rarity']}\n|weapon={WEAPON[foe['weapon']]}\n|move={MOVE[foe['move']]}\n}}}}\n"
            s += ("[[" if foe['rarity'] != 3 else "") + util.getName(f"MID_TRIP_ENEMY_{strike['id_tag']}_{foe['name_id']}") + ("]]" if foe['rarity'] != 3 else "") + "\n"
            s += f"|\n|{foe['Atk']}\n|{foe['Spd']}\n|{foe['Def']}\n|{foe['Res']}\n"
    return s + "|-\n|colspan=\"6\"|<nowiki/>*The order of foes is randomized at the start of every strike.\n|}"

def LostLore(tag: str):
    datas = reverseLostLore(tag)

    ret = {}
    for data in datas:
        if data['isSpoil']:
            print(util.TODO + "New Lost Lore Spoils: " + str(data['avail']))
            continue
        enemies = [d['strike'] for d in data['maps'] if d['strike']]
        s = LLInfobox(data, enemies) + "\n"
        s += Availability(data['avail'], f"Lost Lore ({util.getName('MID_TRIP_TITLE_' + data['id_tag'])}) (Notification)", "[[Lost Lore]] event") + "\n"
        s += LLRewards(data) + "\n"
        s += LLSaga(data, tag) + "\n"
        s += LLLocation(data) + "\n"
        s += LLUnit(data, enemies) + "\n"
        s += InOtherLanguage('MID_TRIP_TITLE_' + data['id_tag'])
        s += "{{Main Events Navbox}}"
        ret[util.getName('MID_TRIP_TITLE_' + data['id_tag'])] = s
    return ret

from sys import argv

if __name__ == '__main__':
    if len(argv) <= 1:
        print("Enter at least one update tag")
        exit(1)
    for arg in argv[1:]:
        if not isfile(util.BINLZ_ASSETS_DIR_PATH + 'Common/Trip/Terms/' + arg + '.bin.lz'):
            print(f'No Lost Lore are related to the tag "{arg}"')
            continue
        ls = LostLore(arg)
        for l in ls:
            print(l, ls[l])