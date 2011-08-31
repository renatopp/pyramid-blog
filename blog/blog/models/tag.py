#-*- coding:utf-8 -*-
import datetime
from blog.models.meta import Base, BaseModel
from sqlalchemy import Integer, Unicode, UnicodeText, DateTime, ForeignKey
from formalchemy import Column

class Tag(Base, BaseModel):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, unique=True, label=u'Descrição')

    def __init__(self, name=None):
        self.name = name

    def __unicode__(self):
        return self.name

    @classmethod
    def _configure_grid(cls, grid):
        grid.configure(
            readonly=True,
            exclude=[
                grid.posts,
            ],
        )
        grid.add_operations('tag')

    @classmethod
    def _configure_form(cls, form):
        form.configure(
            exclude=[
                form.posts, 
            ], 
        )