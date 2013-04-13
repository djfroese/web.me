import web
import datetime
import view, config
from view import render

PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'

urls = (
	'/','index',
	'/post/'+PAGE_RE,'post',
	'/_edit/'+PAGE_RE,'edit'
	)

class index:
	def GET(self):
		return render.base(view.posts(),title="Home")
		
class post:
	def GET(self,pid):
		return "url handling works for pid: %s"%pid

class edit:
	def GET(self,pid):
		return render.base(view.edit(where='id=%s'%pid))
	
	def POST(self,pid):
		data = web.input()
		config.DB.update('Posts', where='id=%s'%pid, title=data.title, body=data.body,modified=datetime.datetime.now())
		web.seeother('/')		

if __name__ == "__main__":
	app = web.application(urls,globals())
	if config.debugmode:
		app.internalerror = web.debugerror
	app.run()
