#-*- coding:utf-8 -*-
import transaction
import hashlib
from sqlalchemy.exc import IntegrityError
from blog.models.meta import Session, Base
# from weblog.models.user import User
# from weblog.models.post import Post
# from weblog.models.comment import Comment

def populate():
    session = Session()
    # user = User(u'renato.ppontes@gmail.com')
    # user.password = hashlib.md5(u'123456'+config.salt).hexdigest()
    # user.nickname = u'Renatopp'
    # user.realname = u'Renato Pereira'
    # session.add(user)
    # transaction.commit()
    
def initialize_sql(engine):
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        Session.rollback()