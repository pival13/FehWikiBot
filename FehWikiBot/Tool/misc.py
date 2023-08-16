#! /usr/bin/env python3

import re as _R

__all__ = [ 'waitSec', 'timeDiff', 'cleanStr', 'askFor', 'askAgreed' ]

_now = 0
def waitSec(time):
    from time import sleep
    from datetime import datetime, timedelta
    global _now
    
    if _now != 0 and datetime.now() < _now+timedelta(seconds=time):
        sleep((_now+timedelta(seconds=time)-datetime.now()).total_seconds())
    _now = datetime.now()


def timeDiff(time: str, diff: int=1) -> str:
    """
    Return the ISO8601 format of `time` with a difference of `diff`.

    Args:
        time (str): An ISO8601 formatted datetime.
        diff (int) (1): Time to substract, in seconds.
    """
    from datetime import datetime, timedelta
    from .globals import TIME_FORMAT
    try:
        return (datetime.strptime(time, TIME_FORMAT) - timedelta(seconds=diff)).strftime(TIME_FORMAT)
    except ValueError:
        return ''

def timeFormat(time: str, format='%b %Y'):
    from datetime import datetime
    from .globals import TIME_FORMAT
    try:
        return datetime.strptime(time, TIME_FORMAT).strftime(format)
    except ValueError:
        return time

def maskToInt(mask: list) -> int:
    v = 0
    for n in mask:
        v |= 1 << n
    return v

def cleanStr(string: str):
    """Replace any non-ascii caractere with an ascii approximation.
    
    Remove non alphanumeric, space, dot, dash or underscore caracteres."""
    from unidecode import unidecode
    return _R.sub(r'\s{2,}', ' ', _R.sub(r"[^A-Za-z0-9 ._-]", "", unidecode(string)))

def askFor(pattern: str=None, intro=None, ignoreCase=False):
    """Ask the user for an answer. Wait until that user respond something (or does not respond)

    Args:
        pattern (str): The format of the expected answer, regex compliant
        intro (str): A string to print before the user answer
        ignoreCase (bool) (False): Whether the pattern should be case sensitiv or not

    Return:
        The user answer if it match the pattern, or None
    """
    from sys import stderr, stdin
    if intro:
        print(intro, file=stderr, end=" ", flush=True)
    s = stdin.readline()
    if s and s[-1] == '\n':
        s = s[:-1]
    if s != None and (not pattern or _R.fullmatch(pattern, s, _R.IGNORECASE if ignoreCase else 0)):
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
    elif _R.fullmatch("no|n", answer, _R.IGNORECASE):
        if askFalse:
            answer = askFor(intro=askFalse)
        else:
            answer = defaultFalse
    elif _R.fullmatch("yes|y|o", answer, _R.IGNORECASE):
        if askTrue:
            answer = askFor(intro=askTrue)
        else:
            answer = defaultTrue
    return answer
