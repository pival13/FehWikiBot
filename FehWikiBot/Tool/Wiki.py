#! /usr/bin/env python3

from requests import Session as _Session, exceptions as _reqExcept
from time import sleep as _sleep

from .globals import ERROR as _ERROR, RESET_TEXT as _RESET_TEXT, GREEN_TEXT as _GREEN_TEXT, GREY_TEXT as _GREY_TEXT, YELLOW_BG as _YELLOW_BG

__all__ = [ 'APIError', 'CargoError', 'Wiki' ]

class APIError(IOError):
    """The API responded with an error"""

class CargoError(APIError):
    """Invalid Cargo request"""

class Wiki:
    URL = "https://feheroes.fandom.com/api.php"
    _S = None

    def __init__(self) -> None:
        pass

    @classmethod
    def login(cls, user, password):
        for _ in range(3):
            try:
                S = _Session()
                token = S.get(url=Wiki.URL, params={
                    "action": "query",
                    "meta": "tokens",
                    "type": "login",
                    "format": "json"
                }).json()['query']['tokens']['logintoken']
                result = S.post(url=Wiki.URL, data={
                    "action": "login",
                    "lgname": user,
                    "lgpassword": password,
                    "lgtoken": token,
                    "format": "json"
                }).json()['login']['result']
                if result != 'Success':
                    cls._S = None
                    raise APIError('Failed to login')
                else:
                    cls._S = S
                    return
            except (_reqExcept.ConnectTimeout,_reqExcept.ConnectionError) as e:
                pass
        raise e


    ##################################################################
    #
    # Get functions
    #
    ##################################################################

    @classmethod
    def get(cls, params):
        params['format'] = 'json'
        res = cls._get(params)
        if 'error' in res:
            raise APIError(res['error']['info'] if 'info' in res['error'] else res['error'])
        return res

    @classmethod
    def cargoQuery(cls, tables: str, fields: str="_pageName=Page", where: str="1", join: str=None, group: str=None, having: str=None, order: str="_pageID", limit: int="max") -> list[dict | str] | dict | str | None:
        """Return the result of a cargo query.

        Args:
            tables (str)
            fields (str): Default "_pageName=Page"
            where (str): Default "1"
            join (str): Default None
            group (str): Default None
            having (str): Default None
            order (str): Default "_pageID"
            limit (str): Default "max"
        
        Returns:
            Return a list of objects, corresponding to the result of the query.
            If `limit` is 1, the object itself is returned instead of a list.
            If `fields` has a single element, the returned objects are the values, otherwise
            they are a dict with the field as key.
        """
        # Several tables are joined
        if tables.find(',') != -1:
            if order == '_pageID': order = None
            if fields == '_pageName=Page':
                raise CargoError("Using several tables requires an overload of `fields`")
        
        S = cls()
        ret = []
        offset = 0
        lim = limit
        while lim != 0:
            obj = {
                "action": "cargoquery",
                "tables": tables,
                "fields": fields,
                "where": where,
                "join_on": join,
                "group_by": group,
                "having": having,
                "limit": lim,
                "offset": offset,
                "order_by": order
            }
            result = S._get(obj)
            if 'error' in result and 'info' in result['error']:
                raise CargoError(result['error']['info'] + ': ' + str(obj))
            elif not 'cargoquery' in result:
                raise APIError('No response: ' + str(result))

            ret += [m['title'] for m in result['cargoquery']]
            count = len(result['cargoquery'])
            Rlimit = result['limits']['cargoquery'] if 'limits' in result else lim
            if count < Rlimit: break
            offset += count
            if lim != 'max': lim -= count

        if len(ret) >= 1 and (len(ret[0]) == 1 or fields.find(',') == -1):
            field = fields.split('=')[-1]
            if field not in ret[0]: field = list(ret[0].keys())[0] # For safety
            ret = [o[field] for o in ret]
        if limit == 1:
            ret = ret[0] if len(ret) == 1 else None
        return ret

    @classmethod
    def getPageContent(cls, page: str, revision: int=0) -> str | None:
        result = cls.get({
            "action": "query",
            "titles": page,
            "prop": "revisions",
            "rvprop": "content",
            "rvlimit": revision+1,
            "rvslots": "*",
        })['query']['pages']
        if len(result) == 0 or 'revisions' not in list(result.values())[0]: return None
        result = list(result.values())[0]['revisions']
        if len(result) > revision:
            return result[revision]['slots']['main']['*']
        else:
            return result[-1]['slots']['main']['*']

    @classmethod
    def getPagesContent(cls, pages: list) -> dict:
        pages = list(pages)
        contents = {}
        for i in range((len(pages)+49) // 50):
            result = cls.get({
                "action": "query",
                "titles": "|".join(pages[i*50:(i+1)*50]),
                "prop": "revisions",
                "rvprop": "content",
                "rvslots": "*",
            })['query']['pages']
            result = {result[pageId]['title']: result[pageId]['revisions'][0]['slots']['main']['*'] for pageId in result if 'revisions' in result[pageId]}
            contents.update(result)
        return contents

    @classmethod
    def getPageCategories(cls, page):
        result = cls.get({
            "action": 'query',
            'prop': 'categories',
            'titles': page,
            'cllimit': 'max',
            'format': 'json'
        })['query']['pages']
        result = list(result.values())[0]
        return [c['title'] for c in result['categories']] if 'categories' in result else []

    @classmethod
    def getPageReferences(cls, page):
        result = cls.get({
            "action": "query",
            "prop": "linkshere|transcludedin|fileusage",
            "titles": page,
            "lhprop": "title",
            "lhlimit": "max",
            "tiprop": "title",
            "tilimit": "max",
            "fuprop": "title",
            "fulimit": "max",
            "format": "json",
        })['query']['pages']
        result = list(result.values())[0]
        res = []
        for k in 'linkshere','transcludein','fileusage':
            res += [c['title'] for c in result[k]] if k in result else []
        return list(set(res))

    @classmethod
    def getCategoryContent(cls, category):
        result = cls.get({
            "action": "query",
            "list": "categorymembers",
            "cmtitle": ('Category:' if category[:9] != 'Category:' else '') + category,
            "cmprop": "title",
            "cmlimit": "max",
            "format": "json",
        })['query']['categorymembers']
        return [o['title'] for o in result]


    ##################################################################
    #
    # Post functions
    #
    ##################################################################

    @classmethod
    def post(cls, params, **kwargs):
        params['format'] = 'json'
        res = cls._post(params, **kwargs)
        if 'error' in res:
            raise APIError(res['error']['info'] if 'info' in res['error'] else res['error'])
        return res

    @classmethod
    def exportPage(cls, name: str, content: str, summary: str=None, minor: bool=False, create: bool=False):
        result = cls._exportPage(name, content, summary, minor, create)
        if 'edit' in result and result['edit']['result'] == 'Success':
            if 'nochange' in result['edit']:
                print(f"{_GREY_TEXT}- No change{_RESET_TEXT}: {name}")
            elif 'new' in result['edit']:
                print(f"{_GREEN_TEXT}+ Created{_RESET_TEXT}: {name}")
            else:
                print(f"{_GREEN_TEXT}* Edited{_RESET_TEXT}: {name}")
        elif 'error' in result and 'code' in result['error'] and result['error']['code'] == 'articleexists':
            print(f"{_GREY_TEXT}- Already exist{_RESET_TEXT}: {name}")
        elif 'error' in result and 'code' in result['error'] and result['error']['info'] == 'timeout':
            print(f"{_YELLOW_BG}! Timeout{_RESET_TEXT}: {name}")
        elif 'error' in result and 'info' in result['error']:
            print(_ERROR + f"Failed to export \"{name}\": {result['error']['info']}")
        else:
            print(_ERROR + f"Failed to export \"{name}\": {result}")

    @classmethod
    def exportPages(cls, group: dict, summary: str=None, minor: bool=False, create: bool=False, noWait: bool=False):
        from .misc import waitSec
        for name in group:
            if not noWait:
                waitSec(10)
            cls.exportPage(name, group[name], summary, minor, create)

    @classmethod
    def uploadFile(cls, name: str, file, content: str, comment: str, ignoreWarning: bool=True):
        from .misc import cleanStr
        result = cls._post({
            "action": "upload",
            "filename": cleanStr(name),
            "comment": 'Bot: ' + comment,
            "text": content,
            ("ignorewarnings" if ignoreWarning else "warnings"): True,
        }, files={
            'file': (name, file, 'multipart/form-data')
        })
        if 'error' in result and 'code' in result['error'] and result['error']['code'] == 'mustbeloggedin':
            from ..PersonalData import USER, BOT, PASSWD
            cls.login(USER+'@'+BOT, PASSWD)
            cls.uploadFile(name, file, content, comment, ignoreWarning)
        elif 'upload' in result and result['upload']['result'] == 'Success':
            print(f"{_GREEN_TEXT}+ Uploaded{_RESET_TEXT}: {name}")
        elif 'error' in result and 'code' in result['error'] and result['error']['code'] == 'fileexists-no-change':
            print(f"{_GREY_TEXT}- Already exist{_RESET_TEXT}: {name}")
        elif 'error' in result and 'code' in result['error'] and result['error']['code'] == 'timeout':
            print(f"{_YELLOW_BG}! Timeout{_RESET_TEXT}: {name}")
        elif 'error' in result and 'info' in result['error']:
            print(_ERROR + f"Failed to upload \"{name}\": {result['error']['info']}")
        else:
            print(_ERROR + f"Failed to upload \"{name}\": {result}")

    @classmethod
    def uploadImage(cls, name: str, image, content: str, comment: str, ignoreWarning: bool=True):
        from io import BytesIO
        file = BytesIO()
        image.save(file, format='PNG')
        cls.uploadFile(name, file.getvalue(), content, comment, ignoreWarning)

    @classmethod
    def uploadFileUrl(cls, name: str, fileUrl: str, content: str, comment: str, ignoreWarning: bool=True):
        import requests
        for _ in range(3):
            try:
                data = requests.get(fileUrl).content
                cls.uploadFile(name, data, content, comment, ignoreWarning)
                return
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                _sleep(5)
        raise e

    @classmethod
    def movePage(cls, name: str, newName: str, summary: str=None, redirect: bool=True):
        result = cls._post({
            "action": "move",
            "from": name,
            "to": newName,
            "movetalk": True,
            "movesubpages": True,
            ("redirect" if redirect else "noredirect"): True,
            "reason": 'Bot: ' + summary,
        })
        if 'move' in result:
            print(f"{_GREEN_TEXT}* Moved{_RESET_TEXT}: {name}")
        elif 'error' in result and 'code' in result['error'] and result['error']['code'] == 'timeout':
            print(f"{_YELLOW_BG}! Timeout{_RESET_TEXT} on move: {name} → {newName}")
        elif 'error' in result and 'info' in result['error']:
            print(_ERROR + f"Failed to move \"{name}\": {result['error']['info']}")
        else:
            print(_ERROR + f"Failed to move \"{name}\": {result}")

    @classmethod
    def deletePage(cls, name: str, summary: str=None):
        result = cls._post({
            "action": "delete",
            "title": name,
            "reason": 'Bot: ' + summary,
        })
        if 'delete' in result:
            print(f"{_GREEN_TEXT}- Deleted{_RESET_TEXT}: {name}")
        elif 'error' in result and 'code' in result['error'] and result['error']['code'] == 'timeout':
            print(f"{_YELLOW_BG}! Timeout{_RESET_TEXT} on delete: {name}")
        elif 'error' in result and 'info' in result['error']:
            print(_ERROR + f"Failed to delete \"{name}\": {result['error']['info']}")
        else:
            print(_ERROR + f'Failed to delete \"{name}\": {result}')

    @classmethod
    def deleteToRedirect(cls, pageToDelete: str, redirectionTarget: str):
        result = cls._post({
            "action": "delete",
            "title": pageToDelete,
            "reason": 'Bot: Delete to redirect',
        })
        if 'error' in result:
            print(_ERROR + f'Failed to delete {pageToDelete}: {result["error"]["info"]}')
        elif 'delete' in result:
            result = cls._exportPage(pageToDelete, f"#REDIRECT [[{redirectionTarget}]]", "redirect", create=True)
            if 'edit' in result and result['edit']['result'] == 'Success':
                print(f'{_GREEN_TEXT}+ Redirected{_RESET_TEXT}: {pageToDelete} → {redirectionTarget}')
            if 'error' in result and 'code' in result['error'] and result['error']['info'] == 'timeout':
                print(f"{_YELLOW_BG}! Timeout{_RESET_TEXT} on redirect: {pageToDelete} → {redirectionTarget}")
            if 'error' in result:
                print(_ERROR + f'Failed to redirect \"{pageToDelete}\" → \"{redirectionTarget}\": {result["error"]["info"]}')
            else:
                print(f'Redirected page {pageToDelete} to {redirectionTarget}')


    ##################################################################
    #
    # Internal functions
    #
    ##################################################################

    @classmethod
    def _get(cls, params):
        if Wiki._S is None:
            from ..PersonalData import USER, BOT, PASSWD
            Wiki.login(USER+'@'+BOT, PASSWD)
        if 'format' not in params:
            params["format"] = "json"
        for _ in range(3):
            try:
                if params['format'] == 'json':
                    return cls._S.get(url=Wiki.URL, params=params).json()
                else:
                    return cls._S.get(url=Wiki.URL, params=params)
            except (_reqExcept.Timeout, _reqExcept.ConnectionError) as e:
                _sleep(5)
        raise e

    @classmethod
    def _post(cls, params, **kwargs):
        if Wiki._S is None:
            from ..PersonalData import USER, BOT, PASSWD
            Wiki.login(USER+'@'+BOT, PASSWD)
        if 'format' not in params: params['format'] = 'json'
        params['bot'] = True
        params['tags'] = 'automated'
        params['watchlist'] = 'nochange'
        params['token'] = cls._getToken()
        for _ in range(3):
            try:
                if params['format'] == 'json':
                    return cls._S.post(url=Wiki.URL, data=params, timeout=10, **kwargs).json()
                else:
                    return cls._S.post(url=Wiki.URL, data=params, timeout=10, **kwargs)
            except _reqExcept.ReadTimeout as e:
                if params['format'] == 'json': return {'error': {'info': 'Response timeout', 'code': 'timeout'}}
                else: raise e
            except (_reqExcept.ConnectTimeout, _reqExcept.ConnectionError) as e:
                _sleep(5)
        raise e

    @classmethod
    def _exportPage(cls, name: str, content: str, summary: str=None, minor: bool=False, create: bool=False):
        return cls._post({
            "action": "edit",
            "title": name,
            "text": content,
            "summary": ('Bot: ' + summary) if summary else None,
            ("minor" if minor else "major"): True,
            ("" if create == -1 else "createonly" if create else "nocreate"): True
        })

    @classmethod
    def _getToken(cls):
        return cls._S.get(url=Wiki.URL, params={
            "action": "query",
            "meta": "tokens",
            "type": "csrf",
            "format": "json"
        }).json()['query']['tokens']['csrftoken']