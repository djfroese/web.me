import config

class Users:
    
    @classmethod
    def login(self, username, password):
        pass
    
    @classmethod
    def logout(self, username, password):
        pass
    
    @classmethod
    def userByName(self, name):
        user = config.DB.select('Users',where='username="%s"'%name, limit=1)
        if user:
            return user
        else:
            return None

    @classmethod
    def userById(self, uid):
        user = config.DB.select('Users',where='id=%s'%uid, limit=1)
        if user:
            return user
        else:
            return None
