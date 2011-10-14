#-*- coding:utf-8 -*-
from webhelpers import feedgenerator
from pyramid.response import Response
from pyramid_handlers import action
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url as url

from sqlalchemy import desc

from blog.libs.paginates import Page
from blog.libs.forms import FieldSet, Grid
from blog.handlers import BaseHandler
from blog.models import Session, Post
from blog import globals as g

import os

class FeedHandler(BaseHandler):
    author = 'Renato Pereira'

    def index(self):
        feed = feedgenerator.Rss201rev2Feed(
            title="Renatopp's - Feed do Blog",
            link=self.request.host_url,
            description="Postagens do super ultra hyper mega site http://renatopp.com",
            author_name=self.author
        )

        posts = Session.query(Post).filter(Post.type!='page').order_by(desc(Post.id)).limit(10).all()
        for post in posts:
            summary = post.content[:200].replace('\n', '<br>')
            categorys = ', '.join([c.name for c in post.categorys]) or 'Sem Categoria'
            description = u"""
            %s (...)<br><br>
            Categorias: %s<br>
            Visite <a href="http://renatopp.com">renatopp.com</a>
            """ % (summary, categorys)

            feed.add_item(
                title=post.title,
                link=url('blog_entry', self.request, id=post.id, alias=post.alias), 
                description=description,
                author_name=self.author
            )
        return Response(feed.writeString('utf-8'))

    def articles(self):
        feed = feedgenerator.Rss201rev2Feed(
            title="Renatopp's - Feed dos Artigos",
            link=self.request.host_url,
            description="Artigos do super ultra hyper mega site http://renatopp.com",
            author_name=self.author
        )

        posts = Session.query(Post).order_by(desc(Post.id)).filter(Post.type=='article').limit(10).all()
        for post in posts:
            summary = post.content[:200].replace('\n', '<br>')
            categorys = ', '.join([c.name for c in post.categorys]) or 'Sem Categoria'
            description = u"""
            %s (...)<br><br>
            Categorias: %s<br>
            Visite <a href="http://renatopp.com">renatopp.com</a>
            """ % (summary, categorys)

            feed.add_item(
                title=post.title,
                link=url('blog_entry', self.request, id=post.id, alias=post.alias), 
                description=description,
                author_name=self.author
            )
        return Response(feed.writeString('utf-8'))