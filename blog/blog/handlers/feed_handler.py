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
from blog.models import Session, Post, Snippet
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

        posts = Session.query(Post).filter(Post.type!='page').filter(Post.status=='Published').order_by(desc(Post.id)).limit(10).all()
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

    def snippets(self):
        feed = feedgenerator.Rss201rev2Feed(
            title="Renatopp's - Feed dos Snippets",
            link=self.request.host_url,
            description="Snippets do super ultra hyper mega site http://renatopp.com",
            author_name=self.author
        )

        snippets = Session.query(Snippet).order_by(desc(Snippet.id)).limit(10).all()
        for snippet in snippets:
            summary = snippet.summary or u'Sem descrição'
            language = snippet.language
            category = ', '.join([c.name for c in snippet.categorys]) or 'Sem Categoria'

            description = u"""
            %s<br>
            <br>
            Linguagem: %s <br>
            Categorias: %s <br>
            Visite o site para mais informações - 
            <a href="http://renatopp.com">renatopp.com</a>.
            """ % (summary, language, category)

            feed.add_item(
                title=snippet.title,
                link=url('snippet_entry', self.request, id=snippet.id, alias=snippet.alias), 
                description=description,
                author_name="Renato Pereira"
            )

        return Response(feed.writeString('utf-8'))

    def articles(self):
        feed = feedgenerator.Rss201rev2Feed(
            title="Renatopp's - Feed dos Artigos",
            link=self.request.host_url,
            description="Artigos do super ultra hyper mega site http://renatopp.com",
            author_name=self.author
        )

        posts = Session.query(Post).order_by(desc(Post.id)).filter(Post.type=='article').filter(Post.status=='Published').limit(10).all()
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

    def sitemaps(self):
        header = u'''<?xml version="1.0" encoding="UTF-8"?>\n
        <urlset xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'''
        footer = u'''</urlset>'''

        model = u'''<loc>%s</loc><changefreq>daily</changefreq>\n'''
        xmls = u''
        posts = Session.query(Post).filter(Post.status=='Published').order_by(desc(Post.id)).all()
        
        xmls += model%(u'http://renatopp.com')

        for post in posts:
            if post.type == 'page':
                xmls += model%url('page', self.request, alias=post.alias)
            else:
                xmls += model%url('blog_entry', self.request, id=post.id, alias=post.alias)
        
        return Response(header + xmls + footer)
        
