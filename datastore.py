import config

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
        value = config.MC.get(str('%s_%s'%(type,key)))
        if value:
            return value
        else:
            return None
    
    @classmethod
    def set(self, type, key, value):
        config.MC.set(str('%s_%s'%(type,key)),value)
    
    @classmethod
    def delete(self, type, key):
        config.MC.delete(str('%s_%s'%(type,key)))
    
    @classmethod
    def flush(self):
        config.MC.flush_all()
