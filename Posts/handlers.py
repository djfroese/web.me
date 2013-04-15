import web, datetime
import utils, config, view
from view import *

class post(utils.WebRequestHandler):
    def GET(self,pid):
        return render.base(view.post(where='id=%s'%pid,limit=1),user=self.user)

class edit(utils.WebRequestHandler):
    def GET(self,pid):
        if self.user:
            return render.base(view.edit(where='id=%s'%pid,limit=1),user=self.user)
        else:
            raise web.seeother('/')
    
    def POST(self,pid):
        data = web.input()
        config.DB.update('Posts', where='id=%s'%pid, title=data.title, body=data.body,modified=datetime.datetime.now())
        config.MC.delete(str('post_id=%s'%pid))
        config.MC.delete('posts_all')
        raise web.seeother('/post/%s'%pid)

class new(utils.WebRequestHandler):
    def GET(self):
        if self.user:
            return render.base(view.new(),user=self.user)
        else:
            raise web.seeother('/')
        
    def POST(self):
        if self.user:
            data = web.input()
            t = datetime.datetime.now()
            pid = config.DB.insert('Posts', title=data.title, body=data.body, created=t, modified=t)
            config.MC.delete('posts_all')
            raise web.seeother('/post/%s'%pid)
        else:
            raise web.seeother('/')

class detail(utils.WebRequestHandler):
    def GET(self):
        if self.user:
            return render.base(view.detail(),user=self.user)
        else:
            raise web.seeother('/')

class delete(utils.WebRequestHandler):
    def GET(self,pid):
        if self.user:
            config.DB.delete('Posts',where='id=%s'%pid)
            config.MC.delete(str('post_id=%s'%pid))
            config.MC.delete('posts_all')
            raise web.seeother('/posts')
        else:
            raise web.seeother('/')
