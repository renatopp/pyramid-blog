#-*- coding:utf-8 -*-

from webhelpers.html import literal, lit_sub
from webhelpers.html.tags import *
from blog import globals as g

def pdate(datetime):
    return datetime.strftime('%d/%m/%Y')

def ptime(datetime):
    return datetime.strftime('%H:%M')

def less_stylesheet_link(*urls):
    return stylesheet_link(*urls, rel='stylesheet/less')

patterns = (r'<span class="([\w|\s|_]*)">([\w|\s|&|;\.]*)</span>', literal(r'<li class="\1"><a href="#">\2</a><li>'))
def paginate(page, **attrs):
    p = page.pager('$link_previous ~2~ $link_next',
        symbol_first=u'First',
        symbol_previous=u'Previous',
        symbol_next=u'Next',
        symbol_last=u'Last',
        show_if_single_page=True,
        link_attr={'class':None},
        curpage_attr={'class': 'active'},
        dotdot_attr={'class': 'disabled'},
        **attrs
    )

    p = lit_sub(u'<a', literal('<li><a'), p)
    p = lit_sub(patterns[0], patterns[1], p)
    return literal(u'<ul>')+p+literal(u'</ul>')

def post_link(post):
    return g.url('blog_entry', id=post.id, alias=post.alias)