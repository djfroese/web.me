#!/usr/bin/python

import web
import datetime
import view, config, utils
from users import Users
from view import render

PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'

urls = (
    '/','index',
    '/post/'+PAGE_RE,'post',
    '/_edit/'+PAGE_RE,'edit',
    '/_new','new',
    '/posts','detail',
    '/_delete/'+PAGE_RE,'delete',
    '/_flush','flush',
    '/_login','login',
    '/_logout','logout'
    )

class index(utils.WebRequestHandler):
    def GET(self):
        return render.base(view.posts(),title="Home",user=self.user)
        
class post(utils.WebRequestHandler):
    def GET(self,pid):
        return render.base(view.post(where='id=%s'%pid,limit=1))

class edit(utils.WebRequestHandler):
    def GET(self,pid):
        if self.user:
            return render.base(view.edit(where='id=%s'%pid,limit=1))
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
            return render.base(view.new())
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

class flush:
    def GET(self):
        if self.user:
            config.MC.flush_all()
            raise web.seeother('/')
        else:
            raise web.seeother('/')

class login(utils.WebRequestHandler):
    def GET(self):
        return render.base(view.login(),user=self.user)

    def POST(self):
        data = web.input()
        user = [x for x in Users.userByName(data.username)][0]
        if user:
            result = utils.valid_pw(data.username, data.password, user.pw)
            if result:
                self.login(user)
                self.user = user
                raise web.seeother('/')
            else:
                return render.base(view.login(),user=self.user)
        else:
            return render.base(view.login(),user=self.user)
        
        return render.base(view.login(),user=self.user)

class logout(utils.WebRequestHandler):
    def GET(self):
        self.logout()
        raise web.seeother('/')

    
if __name__ == "__main__":
    app = web.application(urls,globals())
    if config.debugmode:
        app.internalerror = web.debugerror
    app.run()
