import web, datetime
import utils, config, views
from views import *
import models

class post(utils.WebRequestHandler):
    def GET(self,pid):
        return views.render.base(views.Posts.post(pid),user=self.user)

class edit(utils.WebRequestHandler):
    def GET(self,pid):
        if self.user:
            return views.render.base(views.Posts.edit(pid),user=self.user)
        else:
            raise web.seeother('/')
    
    def POST(self,pid):
        ins = web.input()
        models.Posts.updatePost(pid=pid,where='id=%s'%pid,title=ins.title, body=ins.body,modified=datetime.datetime.now())
        raise web.seeother('/post/%s'%pid)

class new(utils.WebRequestHandler):
    def GET(self):
        if self.user:
            return views.render.base(views.Posts.new(),user=self.user)
        else:
            raise web.seeother('/')
        
    def POST(self):
        if self.user:
            ins = web.input()
            t = datetime.datetime.now()
            pid = models.Posts.createPost(title=ins.title, body=ins.body, created=t, modified=t)
            raise web.seeother('/post/%s'%pid)
        else:
            raise web.seeother('/')

class detail(utils.WebRequestHandler):
    def GET(self):
        if self.user:
            return views.render.base(views.Posts.detail(),user=self.user)
        else:
            raise web.seeother('/')

class delete(utils.WebRequestHandler):
    def GET(self,pid):
        if self.user:
            models.Posts.deletePost(pid)
            raise web.seeother('/posts')
        else:
            raise web.seeother('/')
