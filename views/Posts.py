import markdown
import views
import models

def posts(**k):
    ps = models.Posts.all()
    ps.order('-created')
    l = ps.execute()
    
    #l = models.Posts.posts(**k)
    return views.render.posts.list(l)

def post(pid):
    item = models.Posts.bykey(pid)
    #item = models.Posts.postById(pid)
    if item:
        return views.render.posts.item(item)
    else:
        raise web.seeother('/')

def edit(pid):
	item = models.Posts.bykey(pid)
	if item:
		return views.render.posts.edit(item)
	else:
	    raise web.seeother('/')

def new():
    return views.render.posts.new()

def detail(**k):
    ps = models.Posts.all()
    ps.order('-created')
    l = ps.execute()
    #l = models.Posts.posts(**k)
    return views.render.posts.detail(l)
