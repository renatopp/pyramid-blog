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

class BlogHandler(BaseHandler):
    def __get_posts_query(self):
        query = Session.query(Post)
        query = query.filter(Post.status=='Published')
        query = query.filter(Post.type!='page')
        query = query.order_by(desc(Post.id))

        return query

    def index(self):
        '''
        display:
            front: shows the first post in a large box
            list: shows all posts in a small box
        '''
        page = self.request.params.get('page', '1')
        query = self.__get_posts_query()
        posts = Page(query, page=page, items_per_page=6)
    
        display = 'front' if page=='1' else 'list'
        
        return self.render('/controllers/blogs/index.jinja2', dict(display=display, posts=posts))

    def article(self):
        page = self.request.params.get('page', '1')
        query = self.__get_posts_query(filter_type='article')
        posts = Page(query, page=page, items_per_page=6)
    
        display = 'front' if page=='1' else 'list'
        
        return self.render('/controllers/blogs/index.jinja2', dict(display=display, posts=posts))

    @action(renderer='/controllers/blogs/view.jinja2')
    def page(self):
        query = Session.query(Post)
        query = query.filter(Post.alias==self.request.matchdict.get('alias'))
        query = query.filter(Post.type=='page')
        query = query.filter(Post.status=='Published')

        post = query.first()
        return dict(post=post)

    @action(renderer='/controllers/blogs/view.jinja2')
    def view(self):
        post = Session.query(Post).get(self.get_id())
        return dict(post=post)

    