import web, datetime
import utils, config, views
from views import *

class projects(utils.WebRequestHandler):
    def GET(self):
        return views.render.base(views.Projects.list(),user=self.user)
