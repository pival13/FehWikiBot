#!/usr/bin/env python3

import requests
import json
import re
from time import sleep
from datetime import datetime, timedelta

import util
from util import cargoQuery


now = 0
def waitSec(time: int):
    global now
    if now != 0 and datetime.now() < now+timedelta(seconds=time):
        sleep((now+timedelta(seconds=time)-datetime.now()).total_seconds())
    now = datetime.now()

def getPagesWith(content: str) -> list:
    try:
        S = util.fehBotLogin()
        result = S.get(url=util.URL, params={
            "action": "query",
            "list": "search",
            "srsearch": content,
            "srwhat": "text",
            "srinfo": "","gsrprop": "",
            "srlimit": "max",
            "format": "json",
        }).json()['query']['search']
        pages = getPageContent([r['title'] for r in result])
        pageList = [p if pages[p].find(content) != -1 else None for p in list(pages.keys())]
        while pageList.count(None): pageList.remove(None)
        return pageList
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return getPagesWith(content)

def getPages(nameLike: str) -> list:
    ret = []
    try:
        S = util.fehBotLogin()
        offset = 0
        while True:
            result = S.get(url=util.URL, params={
                "action": "cargoquery",
                "tables": "_pageData",
                "fields": "_pageName=Page",
                "where": "_pageName RLIKE \""+nameLike.replace('"', '\\"')+"\"",
                "limit": "max",
                "offset": offset,
                "order_by": "_ID",
                "format": "json"
            }).json()
            limit = result['limits']['cargoquery']
            offset += limit
            ret += [m['title']['Page'] for m in result['cargoquery']]
            if len(result['cargoquery']) < limit:
                break
        return ret
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return getPages(nameLike)

def getPageRevision(page: str, revision: int) -> str:
    try:
        S = util.fehBotLogin()
        result = S.get(url=util.URL, params={
            "action": "query",
            "titles": page,
            "prop": "revisions",
            "rvprop": "content",
            "rvlimit": revision+1,
            "rvslots": "*",
            "format": "json"
        }).json()['query']['pages']
        result = list(result.values())[0]['revisions']
        if len(result) > revision:
            return result[revision]['slots']['main']['*']
        else:
            return result[-1]['slots']['main']['*']
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return getPageContent(pages)

def getPageContent(pages: list) -> dict:
    if isinstance(pages, str): pages = [pages]
    if len(pages) > 0:
        try:
            S = util.fehBotLogin()
            result = S.get(url=util.URL, params={
                "action": "query",
                "titles": "|".join(pages[:50]),
                "prop": "revisions",
                "rvprop": "content",
                "rvslots": "*",
                "format": "json"
            }).json()['query']['pages']
            result = {result[pageId]['title']: result[pageId]['revisions'][0]['slots']['main']['*'] for pageId in result}
            result.update(getPageContent(pages[50:]))
            return result
        except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return getPageContent(pages)
    else:
        return {}

def deleteToRedirect(pageToDelete: str, redirectionTarget: str):
    S = util.fehBotLogin()
    deleteR = S.post(url=util.URL, data={
        "action": "delete",
        "title": pageToDelete,
        "reason": "Bot: delete to redirect",
        "tags": "automated",
        "watchlist": "nochange",
        "token": util.getToken(),
        "format": "json"
    }).json()
    redirectR = _exportPage(pageToDelete, f"#REDIRECT [[{redirectionTarget}]]", "Bot: redirect", create=True)
    return (deleteR, redirectR)

def _exportPage(name: str, content: str, summary: str=None, minor: bool=False, create: bool=False, attempt=0):
    if attempt >= 3:
        return {'error': {'code': "savefail"}}
    try:
        S = util.fehBotLogin()
        result = S.post(url=util.URL, data={
            "action": "edit",
            "title": name,
            "text": content,
            "summary": summary,
            "minor": minor,
            ("createonly" if create else "nocreate"): True,
            "bot": True,
            "tags": "automated",
            "watchlist": "nochange",
            "token": util.getToken(),
            "format": "json"
        }).json()
        return result
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return _exportPage(name, content, summary, minor, create, attempt+1)

def exportPage(name: str, content: str, summary: str=None, minor: bool=False, create: bool=False):
    result = _exportPage(name, content, summary, minor, create)
    if 'error' in result and result['error']['code'] == 'articleexists':
        print(f"Page already exist: " + name)
    elif 'edit' in result and result['edit']['result'] == 'Success':
        if 'nochange' in result['edit']:
            print(f"No change: " + name)
        elif create:
            print(f"Page created: " + name)
        else:
            print(f"Page edited: " + name)
    else:
        print(result)

def exportSeveralPages(group: dict, summary: str=None, minor: bool=False, create: bool=False):
    for name in group:
        exportPage(name, group[name], summary, minor, create)

from mapUtil import WEAPONS
from scenario import UNIT_IMAGE
from sys import stdin, stderr, stdout, argv
from os import stat, remove, rmdir
from uploadImage import exportImage, listdir

def exportImageUrl(name: str, fileUrl: str, content: str, comment: str, ignoreWarning: bool):
    try:
        S = util.fehBotLogin()
        result = S.post(url=util.URL, data={
            "action": "upload",
            "filename": util.cleanStr(name),
            "url": fileUrl,
            "comment": comment,
            "text": content,
            "ignorewarnings": ignoreWarning,
            "tags": "automated",
            "watchlist": "nochange",
            "token": util.getToken(),
            "format": "json"
        })
        if result.status_code == 200:
            result = result.json()
            if 'error' in result and result['error']['code'] == 'fileexists-no-change':
                print(f"Page already exist: {name}")
            elif 'upload' in result and result['upload']['result'] == 'Success':
                print(f"Page uploaded: {name}")
            elif 'error' in result:
                print(util.ERROR + json.dumps(result['error']))
            else:
                print(result)
        else: print(util.TODO + "Failed to fetch result")

    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        exportImage(name, file, content, comment, ignoreWarning)


def uploadMiniUnit():
    dirs = listdir("../../ssbp-Viewer/Screenshots")
    for c in dirs:
        #if c[:4] != "ch00" and c[:4] != "ch04": continue
        waitSec(1)
        name = "Idle"
        unit = c
        try:
            if unit in UNIT_IMAGE and 'name' in UNIT_IMAGE[unit]:
                name = UNIT_IMAGE[unit]['name'] + "_" + name
            else:
                if unit[-4:] == "EX01":
                    name =  "Resplendent_" + name
                    unit = unit[:-4]
                if unit[-8:] == "PairMain":
                    name = util.getName(UNIT_IMAGE[unit[:-4]]['id_tag']) + "_Main_" + name
                elif unit[-7:] == "PairSub":
                    name = util.getName(UNIT_IMAGE[unit[:-3]]['id_tag']) + "_Sub_" + name
                elif unit[-8:] == "TransMap":
                    name = util.getName(UNIT_IMAGE[unit[:-9]]['id_tag']) + "_TransformMap_" + name
                elif unit[-11:] == "TransBattle":
                    continue
                    name = util.getName(UNIT_IMAGE[unit[:-12]]['id_tag']) + "_Transform_" + name
                elif unit[-6:] == "Dragon":
                    if unit[:-7] in UNIT_IMAGE:
                        name = util.getName(UNIT_IMAGE[unit[:-7]]['id_tag']) + "_Transform_" + name
                    elif unit[:-6] in UNIT_IMAGE:
                        name = util.getName(UNIT_IMAGE[unit[:-6]]['id_tag']) + "_Transform_" + name
                    elif unit[:-6]+"Normal" in UNIT_IMAGE:
                        name = util.getName(UNIT_IMAGE[unit[:-6]+"Normal"]['id_tag']) + "_Transform_" + name
                    elif unit[:-6]+"Legend01" in UNIT_IMAGE:
                        name = util.getName(UNIT_IMAGE[unit[:-6]+"Legend01"]['id_tag']) + "_Transform_" + name
                    elif unit[:-11] in UNIT_IMAGE:
                        name = util.getName(UNIT_IMAGE[unit[:-11]]['id_tag']) + "_Transform_" + name
                    else:
                        print(util.ERROR + "Unknow name for " + unit + " -- " + filepath)
                        continue
                else:
                    name = util.getName(UNIT_IMAGE[unit]['id_tag']) + "_" + name
            print("> ", unit, " ==> ", name)
            if stat("../../ssbp-Viewer/ScreenShots/" + c + "/Idle.png").st_size > 10485760:
                print(util.ERROR + "File to big")
                continue
            exportImage(util.cleanStr(name) + ".png", open("../../ssbp-Viewer/ScreenShots/" + c + "/Idle.png", "rb"),
                "[[Category:Mini unit sprites]][[Category:Mini unit Idle sprites]][[Category:Mini unit animated sprites]][[Category:Mini unit animated Idle sprites]]",
                "Bot: Upload Idle unit", True)
            try:
                remove("../../ssbp-Viewer/ScreenShots/" + c + "/Idle.png")
                rmdir("../../ssbp-Viewer/ScreenShots/" + c)
            except:
                print("Failed to remove file or dir")
        except:
            print(util.ERROR + "Error with " + unit)


if __name__ == '__main__':
    pass
