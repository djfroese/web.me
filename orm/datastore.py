import web, memcache, datetime

db_name = 'dev'
db_app = 'sqlite'
db_user = ''
db_password = ''

#memcache server list
server_list = ['127.0.0.1:11211']




db = web.database(dbn=db_app,db=db_name)

def setDBConnection(app, name, user, password):
    db = web.database(dbn=app,db=name,user=user,pw=password)

#    @classmethod
#    def setCacheConnection(servers,debuglvl=1):
#        self.cache = memcache.Client(servers,debug=debuglvl)
#    
#    @classmethod
#    def get(self, table, key):
#        return self.cache.get(str("%s_%s"%(table,key)))
#    @classmethod
#    def set(self, table, key, value):
#        self.cache.set(str("%s_%s"%(table,key)),value)
def select(table,**k):
    return db.select(table,**k)

def insert(table,**k):
    return db.insert(table,**k)

def delete(table,**k):
    return db.delete(table,**k)

def update(table,where,**k):
    db.update(table,where=where,**k)
    
def createTable(table,columns,types):
    pass
