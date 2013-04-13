import web
import datetime
import view, config, utils
from view import render

PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'

urls = (
    '/','index',
    '/post/'+PAGE_RE,'post',
    '/_edit/'+PAGE_RE,'edit',
    '/_new','new',
    '/posts','detail',
    '/_delete/'+PAGE_RE,'delete',
    '/_flush','flush'
    )

class index(utils.WebRequestHandler):
    def GET(self):
        self.setSecureCookie('test','Hello World')
        return render.base(view.posts(),title="Home")
        
class post(utils.WebRequestHandler):
    def GET(self,pid):
        return render.base(view.post(where='id=%s'%pid,limit=1))

class edit(utils.WebRequestHandler):
    def GET(self,pid):
        return render.base(view.edit(where='id=%s'%pid,limit=1))
    
    def POST(self,pid):
        data = web.input()
        config.DB.update('Posts', where='id=%s'%pid, title=data.title, body=data.body,modified=datetime.datetime.now())
        config.MC.delete(str('post_id=%s'%pid))
        config.MC.delete('posts_all')
        raise web.seeother('/post/%s'%pid)

class new(utils.WebRequestHandler):
    def GET(self):
        return render.base(view.new())
        
    def POST(self):
        data = web.input()
        t = datetime.datetime.now()
        pid = config.DB.insert('Posts', title=data.title, body=data.body, created=t, modified=t)
        config.MC.delete('posts_all')
        raise web.seeother('/post/%s'%pid)

class detail(utils.WebRequestHandler):
    def GET(self):
        return render.base(view.detail())

class delete(utils.WebRequestHandler):
    def GET(self,pid):
        config.DB.delete('Posts',where='id=%s'%pid)
        config.MC.delete(str('post_id=%s'%pid))
        config.MC.delete('posts_all')
        raise web.seeother('/posts')

class flush:
    def GET(self):
        config.MC.flush_all()
        raise web.seeother('/')     

if __name__ == "__main__":
    app = web.application(urls,globals())
    if config.debugmode:
        app.internalerror = web.debugerror
    app.run()
