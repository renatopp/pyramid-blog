from blog.handlers import BaseHandler
from pyramid.response import Response

class TestHandler(BaseHandler):
    def index(self):
        # return Response(u'''
        # <a href="/users">Users</a><br>
        # <a href="/posts">Posts</a><br>
        # <a href="/comments">Comments</a><br>
        # ''')

        return self.render('/bases/layout_blog.jinja2')