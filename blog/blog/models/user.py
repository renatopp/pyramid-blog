#-*- coding:utf-8 -*-
import hashlib
from blog import globals as g
from blog.models.meta import Base, BaseModel
from sqlalchemy import Integer, Unicode
from sqlalchemy.orm import relationship
from formalchemy import Column

class User(Base, BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(Unicode, nullable=False, unique=True, label=u'Email')
    password = Column(Unicode, nullable=False, label=u'Senha')
    nickname = Column(Unicode, nullable=False, label=u'Nick')
    realname = Column(Unicode, nullable=False, label=u'Nome Real')
    url = Column(Unicode, label=u'Website')

    posts = relationship('Post', backref='user')
    comments = relationship('Comment', backref='user')
    
    def __init__(self, nickname=None, email=None, password=None):
        self.nickname = nickname
        self.email = email
        self.password = password

    def __str__(self):
        return '%s (%s)'%(self.nickname or self.realname, self.email)

    @classmethod
    def _before_add(cls, form):
        passsalt = form.model.password+g.SALT
        form.model.password = hashlib.md5(passsalt).hexdigest()

    @classmethod
    def _configure_grid(cls, grid):
        grid.configure(readonly=True)
        grid.add_operations('user')