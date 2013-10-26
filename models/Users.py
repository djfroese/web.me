from datastore import cache, data
import utils, orm

class Users(orm.Model):
    username = orm.StringProperty()
    pw = orm.StringProperty()
    email = orm.StringProperty()
    firstname = orm.StringProperty()
    lastname = orm.StringProperty()
    created = orm.DateTimeProperty()
    #modified = orm.DateTimeProperty()
    id = orm.IntegerProperty(PrimaryKey=True)
    
    @classmethod
    def userById(self,uid):
        user = self.load(cache.get('Users',uid))
        if not user:
            user = Users.key(uid)
            if user:
                cache.set('Users', uid, user.dump())
        
        #user = data.select('Users',where='id=%s'%uid,limit=1)[0]
        return user
    
    @classmethod
    def userByName(self,name):
        #users = data.select('Users',where='username="%s"'%name,limit=1)
        users = Users.all().filter('username =',name).execute()
        print users
        if users:
            return [x for x in users][0]
            #return user[0]
        else:
            return None
    
    @classmethod
    def register(cls, name, pw):
        pw_hash = utils.make_pw_hash(name,pw)
        
        user = Users()
        user.name = name
        user.pw = pw_hash
        user.put()
        
        return user
    
    @classmethod
    def login(cls, name, pw):
        user = cls.userByName(name)
        if user and utils.valid_pw(name, pw, user.password):
            return user
        else:
            return None
