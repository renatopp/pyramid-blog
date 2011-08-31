#-*- coding:utf-8 -*-
import datetime
from blog.models.meta import Base, BaseModel
from sqlalchemy import Integer, Unicode, UnicodeText, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from formalchemy import Column

class Post(Base, BaseModel):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False, unique=True, label=u'Título')
    alias = Column(Unicode, nullable=False, unique=True, label=u'Alias')
    content = Column(Unicode, nullable=False, label=u'')
    date = Column(DateTime, nullable=False, label=u'Data de Criação')
    modified = Column(DateTime, label=u'Data de Modificação')
    status = Column(Unicode, nullable=False, label=u'Status')
    type = Column(Unicode, nullable=False, label=u'Tipo')
    order = Column(Integer, label=u'Ordem')
    allow_comment = Column(Boolean, nullable=False, label=u'Permitir Comentários')
    
    #  parent
    #  tags
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comments = relationship('Comment', backref='post')

    def __init__(self):
        self.date = datetime.datetime.now()
        self.status = 'Published'
        self.type = 'Post'
        self.allow_comment = True

    def __unicode__(self):
        return self.title

    @classmethod
    def _configure_grid(cls, grid):
        grid.configure(
            readonly=True,
            exclude=[
                grid.alias,
                grid.content,
                grid.type,
                grid.order,
                grid.comments,
            ],
        )
        grid.add_operations('post')

    @classmethod
    def _configure_form(cls, form):
        form.configure(
            exclude=[
                form.date, 
                form.modified,
                form.status,
                form.type,
                form.comments,
            ], 
            options=[
                form.content.textarea().with_html(class_='markitup')
            ]
        )