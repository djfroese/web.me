#!/usr/bin/env python

import web
import datetime
import views, config, utils
from views import *
from controllers import *
import datastore


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
    '/_logout','logout',
    '/_reg','register',
    '/projects','projects',
    '/_upload','upload',
    '/_thumbnail','thumbnail'
    )

class index(utils.WebRequestHandler):
    def GET(self):
        return views.render.base(views.Posts.posts(),title="Home",user=self.user)
        

class flush(utils.WebRequestHandler):
    def GET(self):
        if self.user:
            config.MC.flush_all()
        raise web.seeother('/')

if __name__ == "__main__":
    app = web.application(urls,globals())
    if config.debugmode:
        app.internalerror = web.debugerror
    app.run()
