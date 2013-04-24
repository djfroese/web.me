import web
import db
import config
import markdown
import views


def login():
    return views.render.users.login()
    
def register(errors=None):
    return views.render.users.register(errors=errors)
