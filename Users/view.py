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

def login():
    return render.users.login()