#-*- coding:utf-8 -*-

from webhelpers.html.tags import *
from blog import globals as g

def pdate(datetime):
    return datetime.strftime('%d/%m/%Y')

def ptime(datetime):
    return datetime.strftime('%H:%M')

def less_stylesheet_link(*urls):
    return stylesheet_link(*urls, rel='stylesheet/less')

def paginate(page, **attrs):
    p = page.pager('$link_first $link_previous ~2~ $link_next $link_last',
        symbol_first='<<',
        symbol_previous='<',
        symbol_next=u'>',
        symbol_last=u'>>',
        show_if_single_page=True,
        link_attr={'class':'pagelink'},
        **attrs
    )

    return p

def post_link(post):
    return g.url('blog_entry', id=post.id, alias=post.alias)