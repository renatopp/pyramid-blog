#-*- coding:utf-8 -*-
import pygments

from pyramid.response import Response
from pyramid_handlers import action
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc

from blog.libs.paginates import Page
from blog.libs.forms import FieldSet, Grid
from blog.handlers import BaseHandler
from blog.models import Session, Post, Snippet
from blog import globals as g

class BlogHandler(BaseHandler):
    def __get_posts_query(self, filter_type=None):
        query = Session.query(Post)
        query = query.filter(Post.status=='Published')
        if filter_type:
            query = query.filter(Post.type==filter_type)
        else:
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

    def snippet_index(self):
        '''
        display:
            front: shows the first post in a large box
            list: shows all posts in a small box
        '''
        query = Session.query(Snippet).order_by(desc(Snippet.id))

        page = self.request.params.get('page', '1')
        snippets = Page(query, page=page, items_per_page=6)
    
        display = 'front' if page=='1' else 'list'
        
        return self.render('/controllers/blogs/snippet_index.jinja2', dict(display=display, snippets=snippets))

    @action(renderer='/controllers/blogs/snippet_view.jinja2')
    def snippet_view(self):
        snippet = Session.query(Snippet).get(self.get_id())
        
        try:
            lexer = pygments.lexers.get_lexer_by_name(snippet.language)
        except ValueError:
            lexer = pygments.lexers.TextLexer()
        DEFAULT = pygments.formatters.HtmlFormatter(noclasses=False)

        return dict(snippet=snippet, code=pygments.highlight(snippet.content, lexer, DEFAULT))
    