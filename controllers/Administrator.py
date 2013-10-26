import web, datetime
import utils, config, views
from datastore import cache
from views import *
import models


class admin(utils.WebRequestHandler):
    def GET(self):
        if self.user is None:
            raise web.seeother('/')
            return
        
        return views.render.base(views.render.admin.dashboard(),user=self.user)      
        
class manageusers(utils.WebRequestHandler):
    def GET(self):
        if self.user is None:
            raise web.seeother('/')
            return
        
        allusers = models.Users.all()
        allusers.order('id')
        result = allusers.execute()
        return views.render.base(views.render.admin.manageusers(result),user=self.user)
    
    def POST(self):
        pass
    
class edituser(utils.WebRequestHandler):
    def GET(self,uid):
        if (not self.user):
            raise web.seeother('/')
        
        u = models.Users.userById(uid)
        if u:
            return views.render.base(views.render.users.edit(u),user=self.user)
        else:
            web.redirect('/admin/users')
    
    def POST(self,uid):
        if self.user is None:
            raise web.seeother('/')
            return
        
        ins = web.input()
        
        u = models.Users.userById(uid)
        u.firstname = ins.fname
        u.lastname = ins.lname
        u.email = ins.email
        u.put()
        cache.set('Users', uid, u.dump())
        
        raise web.seeother('/admin/users')        


class deleteuser(utils.WebRequestHandler):
    def POST(self,uid):
        if not self.user:
            raise web.seeother('/')
            return
        
        u = models.Users.userById(uid)
        if u:
            u.remove()
        
        raise web.seeother('/admin/users')

class adduser(utils.WebRequestHandler):
    def GET(self):
        if not self.user:
            raise web.seeother('/')
            return
        
        return views.render.base(views.render.users.add(),user=self.user)
    
    def POST(self):
        if not self.user:
            raise web.seeother('/')
            return
        
        ins = web.input()
        u = models.Users.userByName(ins.uname)
         
        errors = {}
        
        if u:
            # need to send render register page with error message
            errors['exists'] = True
        
        if utils.validate_pw(ins.pw, ins.confirmpw):
            errors['nomatch'] = True
             
        if errors == {}:
            u = models.Users.register(ins.uname, ins.pw)
            u.firstname = ins.fname
            u.lastname = ins.lname
            u.email = ins.email
            u.put()
            cache.set('Users', u.id, u.dump())
            self.login(u)
            
        else:
            return views.render.base(views.render.users.add(errors),user=self.user)
        
         
        raise web.seeother('/admin')

class privileges(utils.WebRequestHandler):
    def GET(self):
        pass
    
    def POST(self):
        pass

