#-*- coding:utf-8 -*-
from pyramid.response import Response
from pyramid_handlers import action
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc

from blog.libs.paginates import Page
from blog.libs.forms import FieldSet, Grid
from blog.handlers import BaseHandler
from blog.models import Session, Post
from blog import globals as g

import os

class MediaHandler(BaseHandler):
    @action(renderer='/controllers/medias/index.jinja2')
    def index(self):
        if self.auth():
            return HTTPFound(location=self.urlLogin)
            
        walk = os.walk('blog/statics/images/blogs')
        return dict(walk=walk)#Response(unicode(os.walk('blog/statics/images/blogs').next()[2]))

    @action(renderer='/controllers/medias/edit.jinja2')
    def edit(self):
        if self.auth():
            return HTTPFound(location=self.urlLogin)

        file = os.path.isfile(self.get_id())
