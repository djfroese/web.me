import utils

class Posts:
    @classmethod
    def posts(self):
        value = utils.cache.get('Posts','all')
        if value is None:
            value = utils.data.select('Posts',order='asc created')
            utils.cache.set('Posts','all',value)
        
        return value
    
    @classmethod
    def postById(self,pid):
        value = utils.cache.get('Posts',pid)
        if value is None:
            value = utils.data.select('Posts',where='id=%s'%pid)
            utils.cache.set('Posts',pid,value)
        
        return value
    
    @classmethod
    def createPost(self,**k):
        seqid = data.insert('Posts',**k)
        if seqid > -1:
            value = utils.data.select('Posts',where='id=%s'%seqid)
            utils.cache.set('Posts',value.id,value)
            return True
        else:
            return False
    
    @classmethod
    def deletePost(self,pid):
        utils.cache.delete('Posts',pid)
        utils.data.delete('Posts',where='id=%s'%pid)
    
    @classmethod
    def updatePost(self,**k):
        utils.data.update('Posts',**k)
        utils.cache.delete('Posts',pid)