#! /usr/bin/env python3

import requests
import json
import re

URL = "https://feheroes.gamepedia.com/api.php"
USER = "Pival13"
BOT = "Pival13Test"
PASSWD = "hfq8oig3rcdrsro9jpnp7seko7k3hm7e"

import util

try:
    S = util.fehBotLogin()

    result = S.get(url=URL, params={
        "action": "cargoquery",
        "tables": "News",
        "fields": "News._pageName=Page",
        "where": "Page RLIKE 'What\\'s ([iI]n [sS]tore|New)'",
        "format": "json"
    }).json()
    """result = S.get(url=URL, params={
        "action": "query",
        "titles": "epitech",
        "prop": "extlinks|extracts|images",
        "ellimit": 5,
        "exintro": 1,
        "explaintext": 1,
        "redirects": 1,
        "format": "json"
    })"""
    """result = S.post(url=URL, data={
        "action": "edit",
        "title": "User:" + USER + "/sandbox",
        "section": "new",
        "sectiontitle": "Test API Python",
        "text": "A new test with Python API",
        "minor": 1,
        "watchlist": "unwatch",
        "token": token,
        "format": "json"
    }).json()"""
    """
    result = S.get(url=URL, params={
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }).json()
    loginToken = result['query']['tokens']['logintoken']

    result = S.post(url=URL, data={
        "action": "login",
        "lgname": USER + "@" + BOT,
        "lgpassword": PASSWD,
        "lgtoken": loginToken,
        "format": "json"
    }).json()

    if result['login']['result'] != 'Success':
        print("Login failed:")
        print(json.dumps(result, indent=2))
        exit(0)

    result = S.get(url=URL, params={
        "action": "query",
        "meta": "tokens",
        "type": "csrf",

        "titles": "User:" + USER + "/sandbox",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "*",

        "format": "json"
    }).json()

    token = result['query']['tokens']['csrftoken']

    for v in result['query']['pages']:
        if result['query']['pages'][v]['title'] == "User:" + USER + "/sandbox":
            text = result['query']['pages'][v]['revisions'][0]['slots']['main']['*']
            text = re.compile(r"\{\{!\}\}-\{\{!\}\}([^=]+)=").sub("{{tab/header|\\1}}", text).replace("{{#tag:tabber|", "{{tab/start}}").replace("}}\n==Quests==", "{{tab/end}}\n==Quests==")
            result = S.post(url=URL, data={
                "action": "edit",
                "title": "User:" + USER + "/sandbox",
                "text": text,
                "summary": "Test",
                "minor": True,
                "nocreate": True,
                "bot": True,
                "token": token,
                "format": "json"
            }).json()
"""
    print(json.dumps(result, indent=2))

except requests.exceptions.Timeout:
    print("Connection failure")
except requests.exceptions.ConnectTimeout:
    print("Connection failure")
except requests.exceptions.ConnectionError:
    print("Connection failure")
