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
        symbol_previous=u'Anterior',
        symbol_next=u'Próxima',
        symbol_last=u'Last',
        show_if_single_page=False,
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


def googleplus(url):
    link = """<g:plusone size="medium" href="%s"></g:plusone>"""
    return link%url

def facebook(url):
    link = """
    <iframe
        style="height: 20px; width: 120px; border:none;"
        src="http://www.facebook.com/plugins/like.php?href=%s&amp;layout=button_count&amp;show_faces=false&amp;width=100&amp;action=recommend&amp;colorscheme=light&amp;height=21">
    </iframe>"""

    return link%url

def twitter(url, text=''):
    link = """
    <a
        style="float:right; width: 130px"
        href="http://twitter.com/share"
        class="twitter-share-button"
        data-url="%s"
        data-text="%s"
        data-count="horizontal"
        data-via="renatopp">Tweet
    </a>
    <script type="text/javascript" src="http://platform.twitter.com/widgets.js">
    </script>
    """

    return link%(url, text)