import web, datetime
import utils, config, views
from datastore import cache
from views import *
import models

class post(utils.WebRequestHandler):
    def GET(self,pid):
        result = cache.get('views.post',pid)
        if not result:
            result = views.render.base(views.Posts.post(pid),user=self.user)
            cache.set('views.post',pid,result['__body__'])
               
        return result
        #return views.render.base(views.Posts.post(pid),user=self.user)

class edit(utils.WebRequestHandler):
    def GET(self,pid):
        if self.user:
            return views.render.base(views.Posts.edit(pid),user=self.user)
        else:
            raise web.seeother('/')
    
    def POST(self,pid):
        if self.user:
            ins = web.input()
            item = models.Posts.bykey(pid)
            item.title = ins.title
            item.body = ins.body
            item.modified = datetime.datetime.now()
            item.put()
        
        #models.Posts.updatePost(pid=pid,where='id=%s'%pid,title=ins.title, body=ins.body,modified=datetime.datetime.now())
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
            post = models.Posts()
            #print type(post)
            post.title = ins.title
            post.body = ins.body
            t = datetime.datetime.now()
            post.created = t
            post.modified = t
            pid = post.put()
            
            #pid = models.Posts.createPost(title=ins.title, body=ins.body, created=t, modified=t)
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
            post = models.Posts.bykey(pid)
            post.remove()
            #models.Posts.deletePost(pid)
            raise web.seeother('/posts')
        else:
            raise web.seeother('/')
