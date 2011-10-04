#-*- coding:utf-8 -*-
from pyramid.response import Response
from pyramid_handlers import action
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc

from blog.libs.paginates import Page
from blog.libs.forms import FieldSet, Grid
from blog.handlers import BaseHandler
from blog.models import Session
from blog import globals as g

from urllib import urlopen
import json

class SnippetHandler(BaseHandler):
    @action(renderer='/controllers/snippets/index.jinja2')
    def index(self):
        page = self.request.params.get('page', '1')
        #query = Session.query(Post).filter(Post.status=='Published').order_by(desc(Post.id)).all()
        #posts = Page(query, page=page, items_per_page=6)
    
        #display = 'front' if page=='1' else 'list'
        
        url = urlopen('https://gist.github.com/api/v1/json/gists/renatopp').read()
        gists = json.loads(url)
        return dict(gists=gists['gists'])

        #return self.render('/controllers/blogs/index.jinja2', dict(display=display, posts=posts))