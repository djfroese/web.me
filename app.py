import web
import datetime
import view, config
from view import render

PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'

urls = (
	'/','index',
	'/post/'+PAGE_RE,'post',
	'/_edit/'+PAGE_RE,'edit',
	'/_new','new'
	)

class index:
	def GET(self):
		return render.base(view.posts(),title="Home")
		
class post:
	def GET(self,pid):
		return "url handling works for pid: %s"%pid

class edit:
	def GET(self,pid):
		return render.base(view.edit(where='id=%s'%pid,limit=1))
	
	def POST(self,pid):
		data = web.input()
		config.DB.update('Posts', where='id=%s'%pid, title=data.title, body=data.body,modified=datetime.datetime.now())
		config.MC.delete(str('post_id=%s'%pid))
		config.MC.delete('posts_all')
		raise web.seeother('/')

class new:
    def GET(self):
        return render.base(view.new())
        
    def POST(self):
        data = web.input()
        t = datetime.datetime.now()
        config.DB.insert('Posts', title=data.title, body=data.body, created=t, modified=t)
        config.MC.delete('posts_all')
        raise web.seeother('/')

if __name__ == "__main__":
	app = web.application(urls,globals())
	if config.debugmode:
		app.internalerror = web.debugerror
	app.run()
