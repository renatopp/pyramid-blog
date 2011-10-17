from blog.models.meta import Base
from sqlalchemy import Integer, Unicode, UnicodeText, Boolean, DateTime
from sqlalchemy import ForeignKey, Table
from formalchemy import Column

association_post_category = Table('association_post_category', Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('category_id', Integer, ForeignKey('tag.id'))
)

association_snippet_category = Table('association_snippet_category', Base.metadata,
    Column('snippet_id', Integer, ForeignKey('snippet.id')),
    Column('category_id', Integer, ForeignKey('tag.id'))
)
