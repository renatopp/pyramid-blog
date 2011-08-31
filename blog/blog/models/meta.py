#-*- coding:utf-8 -*-

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class BaseModel(object):
    @classmethod
    def _configure_form(cls, form):
        pass
    
    @classmethod
    def _configure_grid(cls, grid):
        grid.configure(readonly=True)

    @classmethod
    def _before_add(cls, form):
        pass

Session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()