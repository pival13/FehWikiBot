#!/usr/bin/env python3

import requests
import json
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
                "where": "_pageName LIKE \""+nameLike.replace('"', '\\"')+"\"",
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

def getPageContent(pages: list) -> dict:
    if len(pages) > 0:
        try:
            S = util.fehBotLogin()
            result = requests.get(url=util.URL, params={
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
    redirectR = S.post(url=util.URL, data={
        "action": "edit",
        "title": pageToDelete,
        "text": "#REDIRECT [[" + redirectionTarget + "]]",
        "summary": "Bot: redirect",
        "createonly": True,
        "bot": True,
        "tags": "automated",
        "watchlist": "nochange",
        "token": util.getToken(),
        "format": "json"
    }).json()
    return (deleteR, redirectR)

def exportPage(name: str='User:'+util.USER+'/sandbox/Bot', content: str='', summary: str=None, minor: bool=False, create: bool=False):
    try:
        S = util.fehBotLogin()
        result = S.post(url=util.URL, data={
            "action": "edit",
            "title": name,
            "text": content,
            "summary": summary,
            "minor": minor,
            "nocreate": not create,
            #"createonly": create,
            "bot": True,
            "tags": "automated",
            "watchlist": "nochange",
            "token": util.getToken(),
            "format": "json"
        }).json()
        return result
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return exportPage(name, content, summary, minor)


if __name__ == '__main__':
    pass
