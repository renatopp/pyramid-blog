#-*- coding: utf-8 -*-
from pyramid.url import route_url

request = None
SALT = '[3}~@&d%(*g%$#' # salt for passwords
context = {}

def print_request():
    global request

    s = ''
    for k in dir(request):
        try:
            s += '<b>%s</b>: %s<br>'%(k, str(getattr(request, k)))
        except:
            s += '<b>%s</b>: %s<br>'%(k, 'ERRO AQUI')

    return s

def url(route_name, *elements, **kw):
    global request
    if 'params' not in kw:
        kw['params'] = []
    return route_url(route_name, request, *elements, **kw)

def route_url_filter(route_name, *elements, **kw):
    global request
    return url(route_name, *elements, **kw)