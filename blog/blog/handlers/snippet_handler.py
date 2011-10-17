#-*- coding:utf-8 -*-
from pyramid.response import Response
from pyramid_handlers import action
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc

from blog.libs.paginates import Page
from blog.libs.forms import FieldSet, Grid
from blog.handlers import BaseHandler, CrudHandler
from blog.models import Session, Snippet
from blog import globals as g

from urllib import urlopen
import json

class SnippetHandler(CrudHandler):
    model = Snippet
    url_base = 'snippet'
    order_by = 'id desc'

    @action(renderer='/controllers/snippets/edit.jinja2')
    def create(self):
        if self.auth():
            return HTTPFound(location=self.urlLogin)

        form = FieldSet(self.model, data=self.request.POST or None)
        self.model._configure_form(form)
        if self.request.POST:
            if form.validate():
                form.sync()
                self.model._before_create(form, self.request.POST)
                Session.add(form.model)
                self.request.session.flash(u'Item incluído com sucesso.', 'success')
                return HTTPFound(location=g.url(self.url_base))
            else:
                self.request.session.flash(u'Dados inválidos.', 'error')

        return dict(form=form, url_base=self.url_base)

    @action(renderer='/controllers/snippets/view.jinja2')
    def preview(self):
        if self.auth():
            return HTTPFound(location=self.urlLogin)

        snippet = Snippets()
        snippet.title = u'Preview'
        snippet.content = self.request.POST['content']

        return dict(snippet=snippet)

    def titlelize(self):
        if self.auth():
            return HTTPFound(location=self.urlLogin)

        from blog.libs.blogs import titlelize
        return Response(titlelize(self.request.GET['title']))