import web
import db
import config
import markdown
import views


#t_globals = dict(
#    datestr=web.datestr,
#    markdown=markdown.markdown,
#    )

#render = web.template.render('templates/', cache=config.cache, globals=t_globals)
#render._keywords['globals']['render'] = render

def login():
    return views.render.users.login()
    
def register(errors=None):
    return views.render.users.register(errors=errors)
