import web
import db
import config
import markdown

t_globals = dict(
    datestr=web.datestr,
    markdown=markdown.markdown,
    )

render = web.template.render('templates/', cache=config.cache, globals=t_globals)
render._keywords['globals']['render'] = render

def posts(**k):
	l = db.posts(**k)
	return render.posts.list(l)

def post(**k):
    item = db.posts(**k)
    if item:
        return render.posts.item(item)
    else:
        raise web.seeother('/')

def edit(**k):
	item = db.posts(**k)
	if item:
		return render.posts.edit(item)
	else:
	    raise web.seeother('/')

def new():
    return render.posts.new()

def detail(**k):
    l = db.posts(**k)
    return render.posts.detail(l)