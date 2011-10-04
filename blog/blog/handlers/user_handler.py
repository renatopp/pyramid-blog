#-*- coding:utf-8 -*-
from pyramid.response import Response
from pyramid_handlers import action
from pyramid.httpexceptions import HTTPFound

from blog.libs.paginates import Page
from blog.libs.forms import FieldSet, Grid
from blog.handlers import BaseHandler, CrudHandler
from blog.models import Session, User
from blog import globals as g

class UserHandler(CrudHandler):
    model = User
    url_base = 'user'
    order_by = 'nickname'

    def update(self):
        item = Session.query(self.model).get(self.get_id())
        params = self.request.params.copy()
    
        k = 'User-%d-password'%item.id
        if params and params[k] != item.password:
            if not params[k]:
                params[k] = item.password
            else:
                params[k] = self.model.get_pass_hash(params[k])

        form = FieldSet(item, data=params or None)
        self.model._configure_form(form)

        if self.request.params:
            if form.validate():
                form.sync()
                self.model._before_update(item, form, params)
                Session.add(form.model)
                self.request.session.flash(u'Item atualizado com sucesso.', 'success')
                return HTTPFound(location=g.url(self.url_base))
            else:
                self.request.session.flash(u'Dados inválidos', 'error')

        params = dict(form=form, url_base=self.url_base)
        
        if self.renderer_base:
            renderer = self.renderer_base+'/edit.jinja2'
        else:
            renderer = '/bases/crud_edit.jinja2'

        return self.render(renderer, params)