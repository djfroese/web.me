import web
import db
import config
import markdown

from Posts import *
from Users import *
from Base import *
from Projects import *
from Images import *

t_globals = dict(
    datestr=web.datestr,
    markdown=markdown.markdown,
    )

render = web.template.render('templates/', cache=config.cache, globals=t_globals)
render._keywords['globals']['render'] = render
