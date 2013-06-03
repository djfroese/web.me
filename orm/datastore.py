import web, memcache, datetime

db_name = 'dev'
db_app = 'sqlite'
db_user = ''
db_password = ''

#memcache server list
server_list = ['127.0.0.1:11211']



class ds():
    db = web.database(dbn=db_app,db=db_name)
    cache = memcache.Client(server_list,debug=1)
    
    @classmethod
    def setDBConnection(self, app, name, user, password):
        self.db = web.database(dbn=app,db=name,user=user,pw=password)
    
    @classmethod
    def setCacheConnection(servers,debuglvl=1):
        self.cache = memcache.Client(servers,debug=debuglvl)
    
    @classmethod
    def get(self, table, key):
        return self.cache.get(str("%s_%s"%(table,key)))
    @classmethod
    def set(self, table, key, value):
        self.cache.set(str("%s_%s"%(table,key)),value)
    @classmethod
    def select(self,table,**k):
        return self.db.select(table,**k)
    @classmethod
    def insert(self,table,**k):
        return self.db.insert(table,**k)
    @classmethod
    def delete(self,table,**k):
        return self.db.delete(table,**k)
    @classmethod
    def update(self,table,where,**k):
        self.db.update(table,where=where,**k)
        
    @classmethod
    def createTable(self,table,columns,types):
        pass
