import web
import db
import config

t_globals = dict(datestr=web.datestr,)

render = web.template.render('templates/', cache=config.cache, globals=t_globals)
render._keywords['globals']['render'] = render

def posts(**k):
	l = db.posts(**k)
	return render.posts(l)