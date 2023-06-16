#! /usr/bin/env python3

from . import globals
from .misc import *
from .Wiki import *

from . import Reader

from .Container import Container
from .JsonContainer import JsonContainer
from .Article import Article
from .ArticleContainer import ArticleContainer

class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)
