#-*- coding:utf-8 -*-
from pyramid.response import Response
from pyramid_handlers import action
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import desc

from blog.libs.paginates import Page
from blog.libs.forms import FieldSet, Grid
from blog.handlers import CrudHandler
from blog.models import Session, Post
from blog import globals as g

class PostHandler(CrudHandler):
    model = Post
    renderer_base = '/controllers/posts'
    url_base = 'post'
    order_by = 'id desc'

    def index(self):
        if self.auth():
            return HTTPFound(location=self.urlLogin)

        page = self.request.params.get('page', '1')
        query = Session.query(Post).order_by(desc(Post.id))
        if self.request.params.get('type'):
            query = query.filter(Post.type=='page')
        else:
            query = query.filter(Post.type!='page')
        items = Page(query, page=page, items_per_page=10)
        
        grid = Grid(self.model, items)
        Post._configure_grid(grid)
            
        return self.render('/bases/crud_index.jinja2', dict(grid=grid, items=items, url_base=self.url_base))

    @action(renderer='/controllers/posts/edit.jinja2')
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

    @action(renderer='/controllers/posts/view.jinja2')
    def view(self):
        if self.auth():
            return HTTPFound(location=self.urlLogin)
            
        post = Session.query(Post).get(self.get_id())
        return dict(post=post)

    def save_draft(self):
        pass

    @action(renderer='/controllers/blogs/view.jinja2')
    def preview(self):
        if self.auth():
            return HTTPFound(location=self.urlLogin)

        post = Post()
        post.title = u'Preview'
        post.content = self.request.POST['content']

        return dict(post=post)

    def titlelize(self):
        if self.auth():
            return HTTPFound(location=self.urlLogin)

        from blog.libs.blogs import titlelize
        return Response(titlelize(self.request.GET['title']))