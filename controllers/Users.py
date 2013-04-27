import web
import utils, config
import views
from views import *
import models
from models import Users

class login(utils.WebRequestHandler):
    def GET(self):
        return views.render.base(views.Users.login(),user=self.user)

    def POST(self):
        data_in = web.input()
        user = Users.userByName(data_in.username)
        if user:
            result = utils.valid_pw(data_in.username, data_in.password, user.pw)
            if result:
                self.login(user)
                self.user = user
                raise web.seeother('/')
            else:
                return views.render.base(views.Users.login(),user=self.user)
        else:
            return views.render.base(views.Users.login(),user=self.user)
        
        return views.render.base(views.Users.login(),user=self.user)


class logout(utils.WebRequestHandler):
    def GET(self):
        self.logout()
        raise web.seeother('/')

class register(utils.WebRequestHandler):
    def GET(self):
        if self.user:
            return views.render.base(views.Users.register())
        else:
            raise web.seeother('/')
    
    def POST(self):
        if not self.user:
            raise web.seeother('/')
    
        data_in = web.input()
        user = Users.userByName(data_in.username)
        
        errors = {}
        
        if user:
            # need to send render register page with error message
            errors['exists'] = True
        
        if validate_pw(data_in.password, data_in.confirm):
            errors['nomatch'] = True
                
        if errors == {}:
            user = Users.register(data_in.username, data_in.password)
            self.login(user)
            raise web.seeother('/')
        else:
            return views.render.base(views.Users.register(errors))
            
def validate_pw(pw,confirm):
    if pw == confirm:
        return False
    else:
        return True

