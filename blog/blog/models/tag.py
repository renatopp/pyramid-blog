#-*- coding:utf-8 -*-
import datetime
from blog.models.meta import Base, BaseModel
from sqlalchemy import Integer, Unicode, UnicodeText, DateTime, ForeignKey
from formalchemy import Column

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, unique=True, label=u'Descrição')

    def __init__(self, name=None):
        self.name = name

    def __unicode__(self):
        return self.name
