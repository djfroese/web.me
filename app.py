#!/usr/bin/python

import web
import datetime
import view, config, utils
from users import Users
from view import render
from Posts.handlers import *
from Users.handlers import *
import Posts

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
        return render.base(Posts.view.posts(),title="Home",user=self.user)
        

class flush:
    def GET(self):
        if self.user:
            config.MC.flush_all()
            raise web.seeother('/')
        else:
            raise web.seeother('/')


    
if __name__ == "__main__":
    app = web.application(urls,globals())
    if config.debugmode:
        app.internalerror = web.debugerror
    app.run()
