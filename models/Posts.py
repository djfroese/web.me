from datastore import data, cache

class Posts:
    @classmethod
    def posts(self,**k):
        value = cache.get('Posts','all')
        if value is None:
            value = [x for x in data.select('Posts',order='created DESC',**k)]
            cache.set('Posts','all',value)
        
        return value
    
    @classmethod
    def postById(self,pid):
        value = cache.get('Posts',pid)
        if value is None:
            value = [x for x in data.select('Posts',where='id=%s'%pid)][0]
            cache.set('Posts',pid,value)
        
        return value
    
    @classmethod
    def createPost(self,**k):
        seqid = data.insert('Posts',**k)
        if seqid > -1:
            value = [x for x in data.select('Posts',where='id=%s'%seqid)][0]
            cache.set('Posts',value.id,value)
            cache.delete('Posts','all')
            return seqid
        else:
            return False
    
    @classmethod
    def deletePost(self,pid):
        cache.delete('Posts',pid)
        cache.delete('Posts','all')
        data.delete('Posts',where='id=%s'%pid)
    
    @classmethod
    def updatePost(self,pid,**k):
        data.update('Posts',**k)
        cache.delete('Posts','all')
        cache.delete('Posts',pid)