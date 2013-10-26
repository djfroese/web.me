#!/usr/bin/env python

import web
import datetime
import views, config, utils
from views import *
from controllers import *
from datastore import cache

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
    '/_thumbnail','thumbnail',
    '/admin','admin',
    '/admin/users','manageusers',
    '/admin/users/_edit/(.*)','edituser',
    '/admin/users/create','adduser',
    '/admin/users/_del/(.*)','deleteuser',
    '/admin/users/_changepw/(.*)','changepw'
    )

class index(utils.WebRequestHandler):
    def GET(self):
        #result = cache.get('views.posts','all')
        #if not result:
        #    result = views.render.base(views.Posts.posts(),title="Home",user=self.user)
        #    cache.set('views.posts','all',result['__body__'])
        
        #return result
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
