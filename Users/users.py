import config, utils, view

class Users:
    
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

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = utils.make_pw_hash(name,pw)
        if email:
            uid = data.insert('Users',username=name, password=pw_hash)
        else:
            uid = data.insert('Users',username=name, password=pw_hash,email=email)
        
        return self.userById(uid)[0]