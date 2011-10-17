#-*- coding:utf-8 -*-

import datetime
from blog.models.meta import Base, BaseModel
from sqlalchemy import Integer, Unicode, UnicodeText, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, relation
from formalchemy import Column

class Snippet(Base, BaseModel):
    __tablename__ = 'snippet'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False, label=u'Título')
    alias = Column(Unicode, nullable=False, unique=True, label=u'Alias')
    summary = Column(UnicodeText, label=u'Descrição')
    content = Column(UnicodeText, nullable=False, label=u'Cóigo')
    language = Column(Unicode, nullable=False, label=u'Linguagem')
    date = Column(DateTime, nullable=False, label=u'Data de Criação')
    modified = Column(DateTime, label=u'Data de Modificação')
    allow_comment = Column(Boolean, nullable=False, label=u'Permitir Comentários')
    
    categorys = relationship('Tag', secondary='association_snippet_category', backref='snippets')

    def __init__(self):
        self.date = datetime.datetime.now()
        self.allow_comment = True

    def __unicode__(self):
        return self.title

    @classmethod
    def __languages(self):
        import pygments
        listagem = [(x[0], x[1][0]) for x in pygments.lexers.get_all_lexers()]
        listagem.sort(cmp=lambda a,b:cmp(a[0].title(), b[0].title()))
        
        return listagem

    @classmethod
    def _configure_grid(cls, grid):
        grid.configure(
            readonly=True,
            exclude=[
                grid.alias,
                grid.summary,
                grid.content,
                grid.date,
                grid.modified,
                grid.allow_comment,
            ],
        )
        grid.add_operations('snippet')

    @classmethod
    def _configure_form(cls, form):
        form.configure(
            exclude=[
                form.date, 
                form.modified,
            ], 
            options=[
                form.title.with_html(class_='span12'),
                form.alias.with_html(class_='span12'),
                form.summary.textarea().with_html(class_='span12'),
                form.content.textarea().with_html(class_='span12 markitup'),
                form.categorys.with_html(class_='span12'),
                form.language.dropdown(Snippet.__languages(), size=10),
            ]
        )
