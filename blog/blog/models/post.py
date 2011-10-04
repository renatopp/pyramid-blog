#-*- coding:utf-8 -*-
import datetime
from blog.models.meta import Base, BaseModel
from sqlalchemy import Integer, Unicode, UnicodeText, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, relation
from formalchemy import Column

class Post(Base, BaseModel):
    """
    status = {Published, Draft, Trash}
    type = {Post, Article, Page}
    """
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False, unique=True, label=u'Título')
    alias = Column(Unicode, nullable=False, unique=True, label=u'Alias')
    summary = Column(UnicodeText, label=u'Descrição da Postagem')
    content = Column(UnicodeText, nullable=False, label=u'')
    date = Column(DateTime, nullable=False, label=u'Data de Criação')
    modified = Column(DateTime, label=u'Data de Modificação')
    status = Column(Unicode, nullable=False, label=u'Status')
    type = Column(Unicode, nullable=False, label=u'Tipo')
    order = Column(Integer, label=u'Ordem')
    allow_comment = Column(Boolean, nullable=False, label=u'Permitir Comentários')
    
    parent_id = Column(Integer, ForeignKey('post.id'))
    parent = relation('Post', remote_side=[id], backref='children')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    categorys = relationship('Tag', secondary='association_post_category', backref='posts')

    def __init__(self):
        self.date = datetime.datetime.now()
        self.status = 'Published'
        self.type = 'Post'
        self.allow_comment = True

    def __unicode__(self):
        return self.title

    @classmethod
    def _before_add(cls, form, params=None):
        if params:
            if 'Rascunho' in params.get('submit'):
                form.model.status = 'Draft'

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
                grid.type,
                grid.order,
                grid.parent,
                grid.allow_comment,
                grid.user,
                grid.children,
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
            ], 
            options=[
                # form.summary.textarea().with_html(class_='markitup'),
                form.content.textarea().with_html(class_='markitup'),
            ]
        )


        