#-*- coding:utf-8 -*-
import datetime
from blog.models.meta import Base, BaseModel
from sqlalchemy import Integer, Unicode, UnicodeText, DateTime, ForeignKey
from formalchemy import Column

class Comment(Base, BaseModel):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, unique=True, label=u'Nome')
    email = Column(Unicode, nullable=False, unique=True, label=u'Email')
    url = Column(Unicode, nullable=False, label=u'Url')
    content = Column(UnicodeText, nullable=False, label=u'Comentário')
    date = Column(DateTime, nullable=False, label=u'Data de Criação')
    
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    
    def __init__(self):
        self.date = datetime.datetime.now()

    def __unicode__(self):
        return self.name

    @classmethod
    def _configure_grid(cls, grid):
        grid.configure(
            readonly=True,
            exclude=[
                grid.content,
            ],
        )
        grid.add_operations('comment')

    @classmethod
    def _configure_form(cls, form):
        form.configure(
            exclude=[
                form.date,
            ], 
            options=[
                form.content.textarea()
            ]
        )