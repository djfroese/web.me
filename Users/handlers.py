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

class register(utils.WebRequestHandler):
    def GET(self):
        return render.base(view.register())
    
    def POST(self):
        data = web.input()
        user = Users.userByName(data.username)
        
        errors = {}
        
        if user:
            # need to send render register page with error message
            errors['exists'] = True
        
        if validate_pw(data.password, data.confirm):
            errors['nomatch'] = True
        
        #print errors
        
        if errors == {}:
            user = Users.register(data.name, data.passwrod)
            self.login(user)
            raise web.seeother('/')
        else:
            return render.base(view.register(errors))
            
def validate_pw(pw,confirm):
    if pw == confirm:
        return False
    else:
        return True

