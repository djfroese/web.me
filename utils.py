import web, random, string, hashlib, hmac, config, memcache
#import models
from models import Users
#--------------------------------------------------------------------------
# Hashing functions
#--------------------------------------------------------------------------

secret = "jad9paskmn**@#)2NChas;817cna8anc"

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw,salt=make_salt()):
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    if make_pw_hash(name,pw,salt) == h:
        return True

def make_secure_val(val):
    return "%s|%s" % (val,hmac.new(secret, val).hexdigest())

def check_secure_val(h):
    val = h.split('|')[0]
    if make_secure_val(val) == h:
        return val
    
#--------------------------------------------------------------------------

class WebRequestHandler():
    
    def setSecureCookie(self, name, val):
        cookie_val = make_secure_val(val)        
        result = web.setcookie(name,cookie_val)
    
    def readSecureCookie(self, name):
        cookie_val = web.cookies().get(name)  
        return cookie_val and check_secure_val(cookie_val)
    
    def login(self, user):
        self.setSecureCookie('user_id',str(user.id))
    
    def logout(self):
        self.user = None
        web.setcookie('user_id','',expires=0)
    
    def __init__(self):
    	uid = self.readSecureCookie('user_id')
    	self.user = uid and Users.userById(uid)    

class data:
    @classmethod
    def select(self, table, **k):
        return config.DB.select(table,**k)
    
    @classmethod
    def update(self, table, **k):
        return config.DB.update(table,**k)
    
    @classmethod
    def delete(self, table, **k):
        return config.DB.delete(table,**k)
    
    @classmethod
    def insert(self, table, **k):
        return config.DB.insert(table,**k)

class cache:
    @classmethod
    def get(self, type, key):
        value = memcached.get('%s_%s'%(type,key))
        if value:
            return value
        else:
            return None
    
    @classmethod
    def set(self, type, key, value):
        memcached.set('%s_%s'%(type,key),value)
    
    @classmethod
    def delete(self, type, key):
        memcached.delete('%s_%s'%(type,key))
    
    @classmethod
    def flush(self):
        memcached.flush_all()
