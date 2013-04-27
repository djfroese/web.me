from datastore import cache, data
import utils

class Users:
    
    @classmethod
    def userById(self,uid):
        user = data.select('Users',where='id=%s'%uid,limit=1)[0]
        return user
    
    @classmethod
    def userByName(self,name):
        users = data.select('Users',where='username="%s"'%name,limit=1)
        if users:
            return [x for x in users][0]
            #return user[0]
        else:
            return None
    
    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = utils.make_pw_hash(name,pw)
        if email:
            uid = data.insert('Users',username=name, pw=pw_hash)
        else:
            uid = data.insert('Users',username=name, pw=pw_hash,email=email)
        
        return cls.userById(uid)
    
    @classmethod
    def login(cls, name, pw):
        user = cls.userByName(name)
        if user and utils.valid_pw(name, pw, user.password):
            return user
        else:
            return None
