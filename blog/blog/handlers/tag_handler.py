#-*- coding:utf-8 -*-

from blog.handlers import CrudHandler
from blog.models import Tag

class TagHandler(CrudHandler):
    model = Tag
    url_base = 'tag'
