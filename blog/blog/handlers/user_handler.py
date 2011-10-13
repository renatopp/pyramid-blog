#-*- coding:utf-8 -*-
from pyramid.response import Response
from pyramid_handlers import action
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url as url

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
        if self.auth():
            return HTTPFound(location=self.urlLogin)

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

    @action(renderer='/controllers/users/login.jinja2')
    def login(self):
        form = FieldSet(User, data=self.request.POST if self.request.POST else None)
        form.configure(
            include=[form.email, form.password],
            options=[
                form.password.password()
            ]
        )

        if self.request.POST:
            user = Session.query(User).filter(
                (User.email==self.request.POST['User--email']) &
                (User.password==User.get_pass_hash(self.request.POST['User--password']))
            ).first()

            if user is not None:
                session = self.request.session
                session['user_id'] = user.id
                session['user_name'] = user.nickname
                session['user_email'] = user.email

                return HTTPFound(location=self.request.GET.get('back_to', url('post', self.request)))
        
        print '\n\n\n\n\n'
        return dict(form=form)

    def logout(self):
        session = self.request.session
        try:
            del session['user_id']
            del session['user_name']
            del session['user_email']
        except KeyError as e:
            pass

        return HTTPFound(location='/users/login')