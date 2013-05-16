import web, random, string, hashlib, hmac, config
import models

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
    
def createHashID(input,length=6):
    h = hashlib.sha256(input).hexdigest()[:length]
    return h


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
    	self.user = uid and models.Users.userById(uid)    

