import web
import view, config
from view import render

urls = (
	'/','index'
	)

class index:
	def GET(self):
		return render.base(view.posts(),title="Home")

if __name__ == "__main__":
	app = web.application(urls,globals())
	if config.debugmode:
		app.internalerror = web.debugerror
	app.run()