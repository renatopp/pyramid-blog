#-*- coding:utf-8 -*-
from pyramid.response import Response
from pyramid_handlers import action
from pyramid.httpexceptions import HTTPFound

from blog.libs.paginates import Page
from blog.libs.forms import FieldSet, Grid
from blog.handlers import BaseHandler, CrudHandler
from blog.models import Session, Comment

class CommentHandler(CrudHandler):
    model = Comment
    url_base = 'comment'
