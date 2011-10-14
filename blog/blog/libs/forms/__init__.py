#-*- coding:utf-8 -*-

import os

from formalchemy import FieldSet as FAFieldSet, Grid as FAGrid, Field, types
from formalchemy import config
from formalchemy import templates
from formalchemy.fields import FieldRenderer
from jinja2 import Environment, FileSystemLoader, Template

from blog.models import Session
from blog import globals as g

import codecs

class Jinja2Engine(templates.TemplateEngine):
    extension = 'jinja2'
    _lookup = None
    
    def get_template(self, name, **kw):
        filename = '%s.jinja2'%name
        path = os.path.join(os.path.dirname(__file__), filename)
        f = codecs.open(path, 'rb', 'utf-8')
        
        return Template(f.read())
        
    def render(self, template_name, **kw):
        template = self.templates.get(template_name, None)
        return template.render(**kw)

config.from_config({'formalchemy.encoding':'utf-8'})
config.engine = Jinja2Engine(
    #directories=[os.path.dirname(__file__)]
)


from webhelpers.html import tags 
from webhelpers.html.builder import HTML

class MyRadioSet(FieldRenderer):
    def render(self, **kwargs):
        html = ''
        checked = kwargs['options'][0][1]
        for label, value in kwargs['options']:
            r = tags.radio(self.name, value, checked=value == checked)
            t = HTML.tag('span', c=label)
            l = HTML.tag('label', c=r+' '+t)
            html += HTML.tag('li', c=l)
        return HTML.tag('ul', class_='inputs-list', c=html)

FAFieldSet.default_renderers['radio'] = MyRadioSet

class Grid(FAGrid):
    def __init__(self, *args, **kwargs):
        super(Grid, self).__init__(*args, **kwargs)

    def add_operations(self, route_name):
        self.append(Field(' ', type=types.String, value=lambda item:self._operations_col(item, route_name)))

    def _operations_col(self, obj, route_name):
        route_name = route_name+'_action'
        result = '<span class="operations">'
        result += '<a href="%s">Editar</a>' % g.url(route_name, action='update', params=[obj.id])
        result += '&nbsp;'
        result += '<a href="%s" onclick="return confirm(\'Are you sure you want to delete?\')">Remover</a>' % g.url(route_name, action='delete', params=[obj.id])
        result += '</span>'
        return result

def FieldSet(*args, **kwargs):
    fs = FAFieldSet(*args, **kwargs)
    fs.session = Session
    return fs



# ========
