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
        pageList = [p for p in list(pages.keys()) if pages[p].find(content) != -1]
        return pageList
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return getPagesWith(content)

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
        return getPageRevision(page, revision)

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
            result = {result[pageId]['title']: result[pageId]['revisions'][0]['slots']['main']['*'] if 'revisions' in result[pageId] else None for pageId in result}
            result.update(getPageContent(pages[50:]))
            return result
        except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return getPageContent(pages)
    else:
        return {}

def deleteToRedirect(pageToDelete: str, redirectionTarget: str):
    S = util.fehBotLogin()
    deleteR = _deletePage(pageToDelete, 'Bot: Delete to redirect')
    if 'error' in deleteR:
        print(util.ERROR + f'Failed to delete page {pageToDelete}: {deleteR["error"]["info"]}')
    elif 'delete' in deleteR:
        redirectR = _exportPage(pageToDelete, f"#REDIRECT [[{redirectionTarget}]]", "Bot: redirect", create=True)
        if 'error' in redirectR:
            print(util.ERROR + f'Failed to redirect page {pageToDelete} to {redirectionTarget}: {redirectR["error"]["info"]}')
        else:
            print(f'Redirected page {pageToDelete} to {redirectionTarget}')

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
            ("minor" if minor else "major"): True,
            ("" if create == -1 else "createonly" if create else "nocreate"): True,
            "bot": True,
            "tags": "automated",
            "watchlist": "nochange",
            "token": util.getToken(),
            "format": "json"
        }).json()
        return result
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return _exportPage(name, content, summary, minor, create, attempt+1)

def _deletePage(name: str, summary: str=None, attempt=0):
    if attempt >= 3:
        return {'error': {'code':"deletefail",'info':'Maximum attempt reached.'}}
    try:
        S = util.fehBotLogin()
        result = S.post(url=util.URL, data={
            "action": "delete",
            "title": name,
            "reason": summary,
            "tags": "automated",
            "watchlist": "nochange",
            "token": util.getToken(),
            "format": "json"
        }).json()
        return result
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        return _exportPage(name, summary, attempt+1)

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
    elif 'error' in result and 'info' in result['error']:
        print(util.ERROR + f"Error on \"{name}\": {result['error']['info']}")
    else:
        print(util.ERROR + f'{result}')

def deletePage(name: str, summary: str=None):
    result = _deletePage(name, summary)
    if 'error' in result:
        print(util.ERROR + f"Failed to delete \"{name}\": {result['error']['info']}")
    elif 'delete' in result:
        print('Page deleted: ' + name)
    else:
        print(util.ERROR + f'{result}')

def exportSeveralPages(group: dict, summary: str=None, minor: bool=False, create: bool=False):
    for name in group:
        waitSec(5)
        exportPage(name, group[name], summary, minor, create)


if __name__ == '__main__':
    pass