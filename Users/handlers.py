import web
import utils, config, view
from view import *
from users import Users

class login(utils.WebRequestHandler):
    def GET(self):
        return render.base(view.login(),user=self.user)

    def POST(self):
        data = web.input()
        user = [x for x in Users.userByName(data.username)][0]
        if user:
            result = utils.valid_pw(data.username, data.password, user.pw)
            if result:
                self.login(user)
                self.user = user
                raise web.seeother('/')
            else:
                return render.base(view.login(),user=self.user)
        else:
            return render.base(view.login(),user=self.user)
        
        return render.base(view.login(),user=self.user)


class logout(utils.WebRequestHandler):
    def GET(self):
        self.logout()
        raise web.seeother('/')
