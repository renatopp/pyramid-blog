#-*- coding:utf-8 -*-
from pyramid.response import Response
from pyramid_handlers import action
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound

from blog.libs.paginates import Page
from blog.libs.forms import FieldSet, Grid
from blog.handlers import CrudHandler
from blog.models import Session, Post
from blog import globals as g

class PostHandler(CrudHandler):
    model = Post
    renderer_base = '/controllers/posts'
    url_base = 'post'

    @action(renderer='/controllers/posts/edit.jinja2')
    def create(self):
        form = FieldSet(self.model, data=self.request.POST or None)
        self.model._configure_form(form)
        if self.request.POST:
            if form.validate():
                form.sync()
                self.model._before_add(form)
                Session.add(form.model)
                self.request.session.flash(u'Item incluído com sucesso.', 'success')
                return HTTPFound(location=g.url(self.url_base))
            else:
                self.request.session.flash(u'Dados inválidos.', 'error')

        return dict(form=form, url_base=self.url_base)

    @action(renderer='/controllers/posts/view.jinja2')
    def view(self):
        post = Session.query(Post).get(self.get_id())
        return dict(post=post)

    def save_draft(self):
        pass

    @action(renderer='/controllers/posts/view.jinja2')
    def preview(self):
        post = Post()
        post.title = u'Preview'
        post.content = self.request.POST['content']

        return dict(post=post)
        

    def titlelize(self):
        from weblog.libs.blogs import titlelize
        return Response(titlelize(self.request.GET['title']))