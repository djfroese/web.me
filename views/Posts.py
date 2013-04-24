import web
import db
import config
import markdown
import views

def posts(**k):
	l = db.posts(**k)
	return views.render.posts.list(l)

def post(**k):
    item = db.posts(**k)
    if item:
        return views.render.posts.item(item)
    else:
        raise web.seeother('/')

def edit(**k):
	item = db.posts(**k)
	if item:
		return views.render.posts.edit(item)
	else:
	    raise web.seeother('/')

def new():
    return views.render.posts.new()

def detail(**k):
    l = db.posts(**k)
    return views.render.posts.detail(l)
