#-*- coding:utf-8 -*-

import os

from formalchemy import FieldSet as FAFieldSet, Grid as FAGrid, Field, types
from formalchemy import config
from formalchemy import templates
from formalchemy.fields import FieldRenderer

from blog.models import Session
from blog import globals as g

config.from_config({'formalchemy.encoding':'utf-8'})
config.engine = templates.MakoEngine(
    directories=[os.path.dirname(__file__)],
    input_encoding='utf-8',
    output_encoding='utf-8'
)

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
