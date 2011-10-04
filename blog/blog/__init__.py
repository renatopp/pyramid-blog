#-*- coding: utf-8 -*-
import os
from pyramid_beaker import session_factory_from_settings
from pyramid.url import route_url
from pyramid.events import BeforeRender
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from blog.models import initialize_sql
from blog.libs import helpers
from blog.libs import rest

URL_PREFIX = '/'

def get_route(*args):
    return os.path.join(URL_PREFIX, *args).replace('\\', '/')

def get_handler(handler):
    file = '%s_handler'%handler.lower()
    obj = '%sHandler'%handler.title()
    return 'blog.handlers.%s.%s'%(file, obj)

def get_resource(*path):
    return get_route('statics', *path)

def add_renderer_globals(event):
    event['url'] = route_url
    event['resource'] = get_resource
    event['h'] = helpers
    event['rest'] = rest.reST2HTML

def add_magic_handler(config, route_name, pattern=None, handler_name=None):
    """
    Magic Handler

    Combinations:
        > add_magic_handler('user', 'users', 'account')
        handler: blog.handlers.account_handler.AccountHandler
        routes:
            user         => /users           (action=index)
            user_        => /users/          (action=index)
            user_action  => /users/{action}/*params
            user_action_ => /users/{action}

    """
    pattern = pattern or route_name+'s'
    handler_name = handler_name or route_name

    config.add_handler(route_name, pattern=get_route(pattern),
                                   handler=get_handler(handler_name),
                                   action='index')
    
    config.add_handler(route_name+'_', pattern=get_route(pattern+'/'),
                                       handler=get_handler(handler_name),
                                       action='index')

    config.add_handler(route_name+'_action',
                       pattern=get_route(pattern, '{action}', '*params'),
                       handler=get_handler(handler_name))

    config.add_handler(route_name+'_action_',
                       pattern=get_route(pattern, '{action}'),
                       handler=get_handler(handler_name))

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

    config = Configurator(settings=settings)
    config.include('pyramid_handlers')
    config.include('pyramid_jinja2')
    config.include('pyramid_mailer')

    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    config.add_directive('add_magic_handler', add_magic_handler)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    config.add_static_view('statics', 'blog:statics')

    # Home route
    config.add_handler('home', get_route(), get_handler('test'), 'index')

    # Custom routes


    # Index/Action routes
    config.add_magic_handler('user')
    config.add_magic_handler('post')
    config.add_magic_handler('tag')


    return config.make_wsgi_app()

