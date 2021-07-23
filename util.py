#! /usr/bin/env python3

from PersonalData import JSON_ASSETS_DIR_PATH, WEBP_ASSETS_DIR_PATH, APK_ASSETS_DIR_PATH, BINLZ_ASSETS_DIR_PATH, USER, BOT, PASSWD

import requests
import json
from os import listdir
from os.path import isfile
from sys import stdin, stderr
from datetime import datetime, timedelta
import re

URL = "https://feheroes.fandom.com/api.php"
TODO = "\33[1;30;103mTODO\33[0m: "
ERROR = "\33[1;101mERROR\33[0m: "
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

SESSION = None

# ð á ø þ í ú
REMOVE_ACCENT_TABLE = {
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

def timeDiff(time: str, diff: int=1) -> str:
    """
    Return the ISO8601 format of `time` with a difference of `diff`.

    Args:
        time (str): An ISO8601 formatted datetime.
        diff (int) (1): Time to substract, in seconds.
    """
    return (datetime.strptime(time, TIME_FORMAT) - timedelta(seconds=diff)).strftime(TIME_FORMAT)

def cleanStr(string: str):
    """Replace any non-ascii caractere with an ascii approximation.
    
    Remove non alphanumeric, space, dot, dash nor underscore caracteres."""
    for accent in REMOVE_ACCENT_TABLE:
        string = string.replace(accent, REMOVE_ACCENT_TABLE[accent])
    return re.sub(r"[^A-Za-z0-9 ._-]", "", string)

def readFehData(path: str, isFull: bool=False):
    """Args:
        path (str): The filepath of the file
        isFull (bool) (False): Whether it is an absolute path or not.
            If False, prepend JSON_ASSETS_DIR_PATH to it.

    Returns:
        list, object: the content of the file."""
    if not isFull:
        path = JSON_ASSETS_DIR_PATH + path
    data = []
    try:
        f = open(path, encoding="utf-8")
        data = json.load(f)
        f.close()
    except:
        stderr.write("Error with file: " + path + "\n")
    return data

def fetchFehData(path: str, easySort="id_tag"):
    """Return a list of all objects presents in all files from directory `path`. If `easySort`, return an object with keys as field `easySort` of each object.

    Args:
        path (str): Path to a directory. The path must be relativ to JSON_ASSETS_DIR_PATH
        easySort (str) (id_tag): The field to be use as key.
    
    Returns:
        list / object: All objects contain on all jsons from `path`
    """
    directory = JSON_ASSETS_DIR_PATH + path
    files = [directory + "/" + f for f in listdir(directory) if isfile(directory + "/" + f)]

    data = []
    for file in files:
        d = readFehData(file, isFull=True)
        data += d if isinstance(d, list) else [d]

    if easySort and easySort in data[0]:
        return { data[i][easySort] : data[i] for i in range(len(data)) }
    else:
        return data


DATA = {r["key"]: r["value"] for r in fetchFehData("USEN/Message/Data")}
DATA.update({r["key"]: r["value"] for r in fetchFehData("USEN/Message/Menu")})
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
SOUNDS = fetchFehData("Common/Sound/arc")
BGMS = fetchFehData("Common/SRPG/StageBgm")

def getName(id: str, complete=True):
    """Return the name relativ to `id`.
    
    Args:
        id (str): The id to retrieve name from.
        complete (bool) (True): Wheter to try search for additional information relativ to id.
    
    Can prepand 'M', 'MID_STAGE_' or 'MID_CHAPTER_' if necessary.
    
    If an 'HONOR' or 'TITLE' version is available, add it to the name."""
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

def getBgm(mapId: str):
    """Return the list of bgm relativ to an Id"""
    if not mapId in BGMS:
        return []
    
    mapBgms = BGMS[mapId]
    if mapBgms["unknow_id"]:
        askFor("", "Map "+mapId+" has 'unknow_id': "+mapBgms["unknow_id"])
    
    bgms = []
    for bgm in [mapBgms["bgm_id"], mapBgms["bgm2_id"]] + [boss["bgm"] for boss in mapBgms["bossMusics"]]:
        if bgm and bgm in SOUNDS:
            bgms += [files["file"] + ".ogg" for files in SOUNDS[bgm]["list"]]
        elif bgm:
            bgms.append(f"<!--{bgm}-->")
    if mapBgms["useGenericBossMusic"]:
        bgms += [files["file"] + ".ogg" for files in SOUNDS["BGM_BATTLE_BOSS_01"]["list"]]
    return bgms


def askFor(pattern: str=None, intro=None, ignoreCase=False):
    """Ask the user for an answer. Wait until that user respond something (or does not respond)

    Args:
        pattern (str): The format of the expected answer, regex compliant
        intro (str): A string to print before the user answer
        ignoreCase (bool) (False): Whether the pattern should be case sensitiv or not

    Return:
        The user answer if it match the pattern, or None
    """
    if intro:
        print(intro, file=stderr, end=" ", flush=True)
    s = stdin.readline()
    if s and s[-1] == '\n':
        s = s[:-1]
    if s != None and (not pattern or re.fullmatch(pattern, s, re.IGNORECASE if ignoreCase else 0)):
        return s
    
def askAgreed(intro, askTrue: str=None, askFalse: str=None, defaultTrue=None, defaultFalse=None, useTrueDefault=True):
    """Ask the user for a Yes/No answer.

    Args:
        intro (str): The string to print before the user answer
        askTrue (str) (None): A new question in case of an initial Yes.
        askFalse (str) (None): A new question in case of an initial No.
        defaultTrue (str) (None): Default value for a Yes.
        defaultFalse (str) (None): Default value for a No.
        useTrueDefault (bool) (True): Whether choose True as default or False.
    
    Return:
        If no answer is given, return defaultTrue/False depending of useTrueDefault.
        If answer if Yes, and askTrue is not present, return defaultTrue.
        If answer is No, and askFalse is not present, return defaultFalse.
        If answer is Yes, and askTrue is present, return the result of askFor with it.
        If answer is No, and askFalse is present, return the result of askFor with it.
    """
    answer = askFor(intro=intro)
    if not answer:
        answer = defaultTrue if useTrueDefault else defaultFalse
    elif re.fullmatch("no|n", answer, re.IGNORECASE):
        if askFalse:
            answer = askFor(intro=askFalse)
        else:
            answer = defaultFalse
    elif re.fullmatch("yes|y|o", answer, re.IGNORECASE):
        if askTrue:
            answer = askFor(intro=askTrue)
        else:
            answer = defaultTrue
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

def fehBotLogin(attempt=0):
    """Create a new connection to the FeH Wiki, or return the existing connection if any"""
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
            SESSION = None
            raise requests.exceptions.ConnectionError("Failed to login")
        return SESSION

    except (requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
        if attempt < 3:
            return fehBotLogin(attempt+1)
        raise e

def cargoQuery(tables: str, fields: str="_pageName=Page", where: str="1", join: str=None, group: str=None, order: str="_pageID", limit: int="max"):
    """Return the result of a cargo query.

    Args:
        tables (str)
        fields (str): Default "_pageName=Page"
        where (str): Default "1"
        join (str): Default None
        group (str): Default None
        order (str): Default "_pageID"
        limit (str): Default "max"
    
    Returns:
        Return a list of objects, corresponding to the result of the query.
    """
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

from sys import argv

if __name__ == "__main__":
    #print(getName(argv[1]))
    json.dump(DATA, open('jsons/data.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    json.dump(otherLanguages(), open("jsons/otherLanguages.json", 'w', encoding='utf-8'), indent=2, ensure_ascii=False)