#-*- coding:utf-8 -*-

__author__="renatopp"
__date__ ="$Jul 22, 2010 8:06:16 PM$"

from docutils import core
import blog.libs.rest.reSTyoutube
import blog.libs.rest.reSTpygments
import blog.libs.rest.reSTblog

def reST2HTML(text, cut_at_break=False):
    if not text:
        return u''
        
    if cut_at_break:
        if '.. breakpoint::' in text:
            text = text[:text.find('.. breakpoint::')]

    parts = core.publish_parts(source=text, writer_name='html')
    return parts['body_pre_docinfo'] + parts['fragment']


