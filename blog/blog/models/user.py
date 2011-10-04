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
    nickname = Column(Unicode, nullable=False, label=u'Nick')
    realname = Column(Unicode, nullable=False, label=u'Nome Real')
    email = Column(Unicode, nullable=False, unique=True, label=u'Email')
    password = Column(Unicode, nullable=False, label=u'Senha')
    url = Column(Unicode, label=u'Website')

    posts = relationship('Post', backref='user')
    
    def __init__(self, nickname=None, email=None, password=None):
        self.nickname = nickname
        self.email = email
        self.password = password

    def __str__(self):
        return '%s (%s)'%(self.nickname or self.realname, self.email)

    @classmethod
    def get_pass_hash(cls, password):
        passsalt = password+g.SALT
        return hashlib.md5(passsalt).hexdigest()

    @classmethod
    def _before_create(cls, form, params=None):
        form.model.password = cls.get_pass_hash(form.model.password)

    @classmethod
    def _before_update(cls, obj, form, params=None):
        pass

    @classmethod
    def _configure_form(cls, form):
        form.configure(
            options=[
                form.password.password()
            ],
            exclude=[
                form.posts
            ]
        )

    @classmethod
    def _configure_grid(cls, grid):
        grid.configure(
            readonly=True,
            exclude=[
                grid.posts,
                grid.password
            ]
        )
        grid.add_operations('user')