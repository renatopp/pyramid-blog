#-*- coding:utf-8 -*-
from pyramid.response import Response
from pyramid_handlers import action
from pyramid.httpexceptions import HTTPFound

from blog.libs.paginates import Page
from blog.libs.forms import FieldSet, Grid
from blog.handlers import BaseHandler, CrudHandler
from blog.models import Session, User
from blog import globals as g

class UserHandler(CrudHandler):
    model = User
    url_base = 'user'
