import utils

class Users:
    @classmethod
    def userById(self,uid):
        user = utils.data.select('Users',where='id=%s'%uid,limit=1)[0]
        return user
    
    @classmethod
    def userByName(self,name):
        users = utils.data.select('Users',where='username="%s"'%name,limit=1)
        if users:
            return [x for x in users][0]
            #return user[0]
        else:
            return None
    
    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = utils.make_pw_hash(name,pw)
        if email:
            uid = utils.data.insert('Users',username=name, password=pw_hash)
        else:
            uid = utils.data.insert('Users',username=name, password=pw_hash,email=email)
        
        return self.userById(uid)
    
    @classmethod
    def login(cls, name, pw):
        user = cls.userByName(name)
        if user and utils.valid_pw(name, pw, user.password):
            return user
        else:
            return None
