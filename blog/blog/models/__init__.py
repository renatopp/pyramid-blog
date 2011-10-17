#-*- coding:utf-8 -*-
import transaction
import hashlib
from sqlalchemy.exc import IntegrityError
from blog import globals as g
from blog.models.meta import Session, Base
from blog.models.associations import association_post_category
from blog.models.associations import association_snippet_category
from blog.models.user import User
from blog.models.post import Post
from blog.models.tag import Tag
from blog.models.snippet import Snippet

def populate():
    session = Session()
    user = User(u'Renatopp', u'renato.ppontes@gmail.com')
    user.password = hashlib.md5(u'123456'+g.SALT).hexdigest()
    user.realname = u'Renato Pereira'
    session.add(user)
    transaction.commit()
    
def initialize_sql(engine):
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        Session.rollback()