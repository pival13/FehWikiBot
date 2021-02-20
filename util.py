#! /usr/bin/env python3

from PersonalData import JSON_ASSETS_DIR_PATH, WEBP_ASSETS_DIR_PATH, APK_ASSETS_DIR_PATH, BINLZ_ASSETS_DIR_PATH, USER, BOT, PASSWD

import requests
import json
from os import listdir
from os.path import isfile
from sys import stdin, stderr
from datetime import datetime
import re

URL = "https://feheroes.gamepedia.com/api.php"
TODO = "\33[1;30;103mTODO\33[0m: "
ERROR = "\33[1;101mERROR\33[0m: "
DIFFICULTIES = ['Normal', 'Hard', 'Lunatic', 'Infernal', 'Abyssal']
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
MIN_TIME = datetime.utcfromtimestamp(0).strftime(TIME_FORMAT)
MAX_TIME = datetime.utcfromtimestamp(0x7FFFFFFF).strftime(TIME_FORMAT)

SESSION = None

# ð á ø þ í ú
REMOVE_ACCENT = {
    "Á": "A", "À": "A", "Â": "A", "Ä": "A", "Ǎ": "A", "Ă": "A", "Ā": "A", "Ã": "A", "Å": "A", "Ą": "A", "á": "a", "à": "a", "â": "a", "ä": "a", "ǎ": "a", "ă": "a", "ā": "a", "ã": "a", "å": "a", "ą": "a", "ắ": "a", "ă": "a", "ằ": "a", "ắ": "a", "ẳ": "a", "ẵ": "a", "ặ": "a", "â": "a", "ầ": "a", "ẩ": "a", "ẫ": "a", "ấ": "a", "ậ": "a",
    "Æ": "Ae", "Ǣ": "Ae", "Ǽ": "Ae", "æ": "ae", "ǣ": "ae", "ǽ": "ae",
    "Ć": "C", "Ċ": "C", "Ĉ": "C", "Č": "C", "Ç": "C", "ć": "c", "ċ": "c", "ĉ": "c", "č": "c", "ç": "c",
    "Ď": "D", "Đ": "D", "Ḍ": "D", "Ð": "D", "Ḑ": "D", "ď": "d", "đ": "d", "ḍ": "d", "ð": "d", "ḑ": "d",
    "É": "E", "È": "E", "Ė": "E", "Ê": "E", "Ë": "E", "Ě": "E", "Ĕ": "E", "Ē": "E", "Ẽ": "E", "Ę": "E", "Ẹ": "E", "Ɛ": "E", "Ǝ": "E", "Ə": "E", "Ề": "E", "Ể": "E", "Ễ": "E", "Ế": "E", "Ệ": "E", "é": "e", "è": "e", "ė": "e", "ê": "e", "ë": "e", "ě": "e", "ĕ": "e", "ē": "e", "ẽ": "e", "ę": "e", "ẹ": "e", "ɛ": "e", "ǝ": "e", "ə": "e", "ề": "e", "ể": "e", "ễ": "e", "ế": "e", "ệ": "e",
    "Ġ": "G", "Ĝ": "G", "Ğ": "G", "Ģ": "G", "ġ": "g", "ĝ": "g", "ğ": "g", "ģ": "g",
    "Ĥ": "H", "Ħ": "H", "Ḥ": "H", "ĥ": "h", "ħ": "h", "ḥ": "h", "ḩ": "h",
    "İ": "I", "Í": "I", "Ì": "I", "Î": "I", "Ï": "I", "Ǐ": "I", "Ĭ": "I", "Ī": "I", "Ĩ": "I", "Į": "I", "Ị": "I", "ı": "i", "í": "i", "ì": "i", "î": "i", "ï": "i", "ǐ": "i", "ĭ": "i", "ī": "i", "ĩ": "i", "į": "i", "ị": "i",
    "Ĵ": "J", "ĵ": "j",
    "Ķ": "K", "ķ": "k",
    "Ĺ": "L", "Ŀ": "L", "Ľ": "L", "Ļ": "L", "Ł": "L", "Ḷ": "L", "Ḹ": "L", "ĺ": "l", "ŀ": "l", "ľ": "l", "ļ": "l", "ł": "l", "ḷ": "l", "ḹ": "l",
    "Ṃ": "M", "ṃ": "m",
    "Ń": "N", "Ň": "N", "Ñ": "N", "Ņ": "N", "Ṇ": "N", "Ŋ": "N", "ń": "n", "ň": "n", "ñ": "n", "ņ": "n", "ṇ": "n", "ŋ": "n",
    "Ó": "O", "Ò": "O", "Ô": "O", "Ö": "O", "Ǒ": "O", "Ŏ": "O", "Ō": "O", "Õ": "O", "Ǫ": "O", "Ọ": "O", "Ő": "O", "Ø": "O", "Ɔ": "O", "ó": "o", "ò": "o", "ô": "o", "ö": "o", "ǒ": "o", "ŏ": "o", "ō": "o", "õ": "o", "ǫ": "o", "ọ": "o", "ő": "o", "ø": "o", "ɔ": "o", "ơ": "o", "ồ": "o",
    "Œ": "Oe", "œ": "oe",
    "Ŕ": "R", "Ř": "R", "Ŗ": "R", "Ṛ": "R", "Ṝ": "R", "ŕ": "r", "ř": "r", "ŗ": "r", "ṛ": "r", "ṝ": "r",
    "Ś": "S", "Ŝ": "S", "Š": "S", "Ş": "S", "Ș": "S", "Ṣ": "S", "ś": "s", "ŝ": "s", "š": "s", "ş": "s", "ș": "s", "ṣ": "s",
    "ß": "ss",
    "Ť": "T", "Ţ": "T", "Ț": "T", "Ṭ": "T", "ť": "t", "ţ": "t", "ț": "t", "ṭ": "t",
    "Þ": "Th", "þ": "th",
    "Ú": "U", "Ù": "U", "Û": "U", "Ü": "U", "Ǔ": "U", "Ŭ": "U", "Ū": "U", "Ũ": "U", "Ů": "U", "Ų": "U", "Ụ": "U", "Ű": "U", "Ǘ": "U", "Ǜ": "U", "Ǚ": "U", "Ǖ": "U", "ú": "u", "ù": "u", "û": "u", "ü": "u", "ǔ": "u", "ŭ": "u", "ū": "u", "ũ": "u", "ů": "u", "ų": "u", "ụ": "u", "ű": "u", "ǘ": "u", "ǜ": "u", "ǚ": "u", "ǖ": "u",
    "Ŵ": "W", "ŵ": "w",
    "Ý": "Y", "Ŷ": "Y", "Ÿ": "Y", "Ỹ": "Y", "Ȳ": "Y", "ý": "y", "ŷ": "y", "ÿ": "y", "ỹ": "y", "ȳ": "y",
    "Ź": "Z", "Ż": "Z", "Ž": "Z", "ź": "z", "ż": "z", "ž": "z"
}

BGM_FILEPATH = __file__[:__file__.rfind('/')] + '/bgm.json'

class LoginError(RuntimeError):
    def __init__(self, arg):
        self.args = arg
    def __str__(self):
        return self.arg

def cleanStr(string: str):
    for accent in REMOVE_ACCENT:
        string = string.replace(accent, REMOVE_ACCENT[accent])
    return re.sub(r"[^A-Za-z0-9 ._-]", "", string)

def readFehData(path: str, isFull: bool=False):
    if not isFull:
        path = JSON_ASSETS_DIR_PATH + path
    data = {}
    try:
        f = open(path)
        data = json.load(f)
        f.close()
    except:
        stderr.write("Error with file: " + path + "\n")
    return data

def fetchFehData(path: str=None, easySort="id_tag"):
    files = []
    if not path:
        directory = JSON_ASSETS_DIR_PATH + "USEN/Message"
        files = [directory + "/Data/" + f for f in listdir(directory + "/Data") if isfile(directory + "/Data/" + f)]
        files += [directory + "/Menu/" + f for f in listdir(directory + "/Menu") if isfile(directory + "/Menu/" + f)]
    else:
        directory = JSON_ASSETS_DIR_PATH + path
        files = [directory + "/" + f for f in listdir(directory) if isfile(directory + "/" + f)]

    data = []
    for file in files:
        d = readFehData(file, isFull=True)
        data += d if isinstance(d, list) else [d]

    if not path:
        return { data[i]['key'] : data[i]['value'] for i in range(len(data)) }
    elif easySort and easySort in data[0]:
        return { data[i][easySort] : data[i] for i in range(len(data)) }
    else:
        return data

def otherLanguages():
    USEN = fetchFehData("USEN/Message/Data", "key")
    JPJA = fetchFehData("JPJA/Message/Data", "key")
    EUDE = fetchFehData("EUDE/Message/Data", "key")
    EUES = fetchFehData("EUES/Message/Data", "key")
    USES = fetchFehData("USES/Message/Data", "key")
    EUFR = fetchFehData("EUFR/Message/Data", "key")
    EUIT = fetchFehData("EUIT/Message/Data", "key")
    TWZH = fetchFehData("TWZH/Message/Data", "key")
    USPT = fetchFehData("USPT/Message/Data", "key")

    language = { key:  {'USEN': USEN[key]['value'] if key in USEN else '',
                        'JPJA': JPJA[key]['value'] if key in JPJA else '',
                        'EUDE': EUDE[key]['value'] if key in EUDE else '',
                        'EUES': EUES[key]['value'] if key in EUES else '',
                        'USES': USES[key]['value'] if key in USES else '',
                        'EUFR': EUFR[key]['value'] if key in EUFR else '',
                        'EUIT': EUIT[key]['value'] if key in EUIT else '',
                        'TWZH': TWZH[key]['value'] if key in TWZH else '',
                        'USPT': USPT[key]['value'] if key in USPT else ''} for key in USEN}

    USEN = fetchFehData("USEN/Message/Menu", "key")
    JPJA = fetchFehData("JPJA/Message/Menu", "key")
    EUDE = fetchFehData("EUDE/Message/Menu", "key")
    EUES = fetchFehData("EUES/Message/Menu", "key")
    USES = fetchFehData("USES/Message/Menu", "key")
    EUFR = fetchFehData("EUFR/Message/Menu", "key")
    EUIT = fetchFehData("EUIT/Message/Menu", "key")
    TWZH = fetchFehData("TWZH/Message/Menu", "key")
    USPT = fetchFehData("USPT/Message/Menu", "key")

    for key in USEN:
        language[key] = {'USEN': USEN[key]['value'] if key in USEN else '',
                         'JPJA': JPJA[key]['value'] if key in JPJA else '',
                         'EUDE': EUDE[key]['value'] if key in EUDE else '',
                         'EUES': EUES[key]['value'] if key in EUES else '',
                         'USES': USES[key]['value'] if key in USES else '',
                         'EUFR': EUFR[key]['value'] if key in EUFR else '',
                         'EUIT': EUIT[key]['value'] if key in EUIT else '',
                         'TWZH': TWZH[key]['value'] if key in TWZH else '',
                         'USPT': USPT[key]['value'] if key in USPT else ''}

    return language

DATA = fetchFehData()
DATA.update({
    "MSID_ファルシオン": "Falchion (Mystery)",
    "MSID_ファルシオン外伝": "Falchion (Gaiden)",
    "MSID_ファルシオン覚醒": "Falchion (Awakening)",
    "MSID_レーヴァテイン": "Laevatein (weapon)",
    "MSID_ミステルトィン": "Missiletainn (sword)",
    "MSID_魔書ミステルトィン": "Missiletainn (tome)",
    "MSID_ナーガ": "Naga (tome)",
    "MID_STAGE_X0041": "Legendary Hero (map)"
})

def getName(id: str, complete=True):
    if not id:
        return None
    if id in DATA:
        return DATA[id]
    elif "M" + id in DATA:
        pos = id.find('_')
        if complete and "M" + id[:pos] + "_HONOR" + id[pos:] in DATA:
            return DATA["M" + id] + ": " + DATA["M" + id[:pos] + "_HONOR" + id[pos:]]
        return DATA["M" + id]
    elif "MID_STAGE_" + id in DATA:
        if complete and "MID_STAGE_HONOR_" + id in DATA:
            return DATA["MID_STAGE_" + id] + ": " + DATA["MID_STAGE_HONOR_" + id]
        return DATA["MID_STAGE_" + id]
    elif "MID_CHAPTER_" + id in DATA:
        if complete and "MID_CHAPTER_TITLE_" + id in DATA:
            return DATA["MID_CHAPTER_TITLE_" + id] + ": " + DATA["MID_CHAPTER_" + id]
        return DATA["MID_CHAPTER_" + id]
    return id

def getHeroJson(heroId: int):
    HERO = fetchFehData("Common/SRPG/Person", False)

    for hero in HERO:
        if hero['id_num'] == heroId:
            return hero
    return {}

def getHeroName(heroId: int):
    hero = getHeroJson(heroId)
    if hero == {}:
        return ""
    return getName(hero['id_tag'])

BGM = {
    "BGM_BATTLE_BOSS_01": "bgm_battle_boss.ogg",
    "BGM_BATTLE_BOSS_02": "bgm_menu_theme01.ogg",
    "BGM_BATTLE_BOSS_03": "bgm_boss3.ogg",
    "BGM_BATTLE_BOSS_04": "bgm_boss4.ogg",
    "BGM_BATTLE_BOSS_05": "bgm_boss5.ogg",
    "BGM_BATTLE_BOSS_06": "bgm_boss6.ogg",
    "BGM_BATTLE_BOSS_07": "bgm_boss7.ogg",
    "BGM_BATTLE_BOSS_08": "bgm_boss8.ogg",
    "BGM_MAP_BRAVE_01": "bgm_map_Brave_01.ogg",
    "BGM_MAP_BRAVE_02": "bgm_map_Brave_02.ogg",
    "BGM_MAP_BRAVE_03": "bgm_map_Brave_03.ogg",
    "BGM_MAP_BRAVE_03_SAME": "bgm_map_Brave_03.ogg",
    "BGM_MAP_BRAVE_04": "bgm_map_FEH_04.ogg",
    "BGM_MAP_BRAVE_05": "bgm_map_FEH_05.ogg",
    "BGM_MAP_BRAVE_06": "bgm_map_FEH_06.ogg",
    "BGM_MAP_BRAVE_07": "bgm_map_FEH_07.ogg",
    "BGM_MAP_EVT_HAPPY_01": "bgm_event_happy1.ogg",
    "BGM_MAP_EVT_SERIOUS_01": "bgm_event_serious1.ogg",
    "BGM_MAP_EVT_SERIOUS_02": "bgm_event_serious2.ogg",
    "BGM_MAP_EVT_SERIOUS_03": "bgm_event_serious3.ogg",
    "BGM_MAP_EVT_SERIOUS_04": "bgm_event_serious4.ogg",
    "BGM_MAP_FES_01_SAME": "bgm_map_fes_01.ogg",
    "BGM_MAP_FES_02_SAME": "bgm_map_fes_02.ogg",
    "BGM_MAP_FES_03_SAME": "bgm_map_fes_03.ogg",
    "BGM_MAP_FES_04_SAME": "bgm_map_fes_04.ogg",
    "BGM_MAP_FES_05_SAME": "bgm_map_fes_05.ogg",
    "BGM_MAP_FE08_04": "bgm_mns_FE08_04.ogg",
    "BGM_MAP_FE10_07": "bgm_mns_FE10_01.ogg",
    "BGM_MAP_FE10_09": "bgm_mns_FE10_03.ogg",
    "BGM_MAP_FE10_10": "bgm_mns_FE10_04.ogg",
    "BGM_MAP_FE10_11": "bgm_mns_FE10_05.ogg",
    "BGM_MAP_FE11_02": "bgm_mns_FE11_03.ogg",
    "BGM_MAP_FE13_14": "bgm_mns_FE13_06.ogg",
    "BGM_MAP_FE14_05_SAME": "bgm_map_FE14_05.ogg",
    "BGM_MAP_FE14_14_SAME": "bgm_mns_FE14_07.ogg",
    "BGM_MAP_FE14_16": "bgm_mns_FE14_06.ogg",
    "BGM_MAP_FE14_17": "bgm_mns_FE14_09.ogg",
}

bgmNames = []
bgms = {}
def getBgm(mapId: str):
    global bgmNames
    if len(bgmNames) == 0: bgmNames = [m['Filename'] for m in cargoQuery('BackgroundMusic', fields='Filename')]
    global bgms
    if len(bgms) == 0: bgms = readFehData(BGM_FILEPATH, True)

    if not mapId in bgms:
        return []
    tmp = bgms[mapId]
    bgm = ""
    if tmp["unknow_id"]:
        askFor("", "Map "+mapId+" has 'unknow_id': "+tmp["unknow_id"])
    if tmp["bgm2_id"]:
        if tmp["bgm2_id"] in BGM: bgm = BGM[tmp["bgm2_id"]]
        else: bgm = tmp["bgm2_id"].lower().replace('fe','FE')+".ogg"
        if not bgm in bgmNames: bgm = '<!--'+bgm+'-->'
        bgm += '<!--'+(BGM[tmp["bgm_id"]] if tmp["bgm_id"] in BGM else (tmp["bgm_id"].lower().replace('fe','FE')+".ogg"))+'-->'
    else:
        if tmp["bgm_id"] in BGM: bgm = BGM[tmp["bgm_id"]]
        else: bgm = tmp["bgm_id"].lower().replace('fe','FE')+".ogg"
        if not bgm in bgmNames: bgm = '<!--'+bgm+'-->'
    if tmp["useGenericBossMusic"]:
        return [bgm, BGM["BGM_BATTLE_BOSS_01"]]
    elif tmp["nbBossMusic"] > 0:
        boss = []
        for b in tmp["bossMusics"]:
            if not b["bgm"] in boss: boss += [b["bgm"]]
        for i in range(len(boss)):
            if boss[i] in BGM: boss[i] = BGM[boss[i]]
            else: boss[i] = boss[i].lower().replace('fe','FE')+".ogg"
            if not boss[i] in bgmNames: boss[i] = '<!--'+boss[i]+'-->'; print(TODO + "Unknow boss: " + boss[i] + " on " + mapId)
        return [bgm] + boss
    else:
        return [bgm]


def askFor(pattern: str=None, intro=None, ignoreCase=False):
    if intro:
        print(intro, file=stderr, end=" ", flush=True)
    s = stdin.readline()
    if s and s[-1] == '\n':
        s = s[:-1]
    if s != None and (not pattern or re.fullmatch(pattern, s, re.IGNORECASE if ignoreCase else 0)):
        return s
    
def askAgreed(intro, askYes: str=None, askNo: str=None, defaultTrue=None, defaultFalse=None, useTrueDefault=True):
    answer = askFor(None, intro)
    if not answer and useTrueDefault:
        return defaultTrue
    elif not answer and not useTrueDefault:
        return defaultFalse
    if re.fullmatch("no|n", answer, re.IGNORECASE):
        if askNo:
            answer = askFor(intro=askNo)
        else:
            return defaultFalse
    elif re.fullmatch("yes|y|o|", answer, re.IGNORECASE):
        if askYes:
            answer = askFor(intro=askYes)
        else:
            return defaultTrue
    return answer

def getToken():
    S = fehBotLogin()
    result = S.get(url=URL, params={
        "action": "query",
        "meta": "tokens",
        "type": "csrf",
        "format": "json"
    }).json()
    return result['query']['tokens']['csrftoken']

def fehBotLogin():
    global SESSION
    if SESSION:
        return SESSION
    try:
        SESSION = requests.Session()

        result = SESSION.get(url=URL, params={
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }).json()

        result = SESSION.post(url=URL, data={
            "action": "login",
            "lgname": USER + "@" + BOT,
            "lgpassword": PASSWD,
            "lgtoken": result['query']['tokens']['logintoken'],
            "format": "json"
        }).json()

        if result['login']['result'] != 'Success':
            raise LoginError(result['login']['reason'])
        return SESSION

    except LoginError:
        print("Error during login")
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return fehBotLogin()

def cargoQuery(tables: str, fields: str="_pageName=Page", where: str="1", join: str=None, group: str=None, order: str="_pageID", limit: int="max"):
    ret = []
    offset = 0
    try:
        S = fehBotLogin()
        while True:
            result = S.get(url=URL, params={
                "action": "cargoquery",
                "tables": tables,
                "fields": fields,
                "where": where,
                "join_on": join,
                "group_by": group,
                "limit": limit,
                "offset": offset,
                "order_by": order,
                "format": "json"
            }).json()
            if not 'cargoquery' in result:
                print({
                    "action": "cargoquery",
                    "tables": tables,
                    "fields": fields,
                    "where": where,
                    "join_on": join,
                    "group_by": group,
                    "limit": limit,
                    "offset": offset,
                    "order_by": order,
                    "format": "json"
                })
                print(result['error']['info'], file=stderr)
                raise Exception
            Rlimit = result['limits']['cargoquery'] if 'limits' in result else 0
            offset += len(result['cargoquery'])
            ret += [m['title'] for m in result['cargoquery']]
            if limit != "max" or len(result['cargoquery']) < Rlimit:
                break
        return ret
        
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return cargoQuery(tables, fields, where, join, group, order, limit)

from sys import argv

if __name__ == "__main__":
    print(getName(argv[1]))
    """print(cleanStr("Veðrfölnir's Egg"))
    print(cleanStr("Sæhrímnir"))
    print(cleanStr("Hliðskjálf"))
    print(cleanStr("Vafþrúðnir"))"""
    #json.dump(otherLanguages(), open("otherLanguages.json", 'w'), indent=2, ensure_ascii=False)
    #json.dump(DATA, open('data.json', 'w'), indent=2, ensure_ascii=False)