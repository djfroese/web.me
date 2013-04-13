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

def edit(**k):
	item = db.posts(**k)	
	return render.posts.edit(item[0])

def new():
    return render.posts.new()