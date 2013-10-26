from datastore import cache, data

class Projects:
    
    @classmethod
    def getProjectById(self,prid):
        value = cache.get('Projects',prid)
        if value is None:
            value = data.select('Projects',where='id=%s'%prid)
            cache.set('Posts',prid,value)
        
        return value
    
    @classmethod
    def getProjects(self):
        value = cache.get('Projects','all')
        if value is None:
            value = [x for x in data.select('Projects')]
            cache.set('Projects','all',value)
        
        return value
    
    @classmethod
    def createProject(self, **k):        
        seqid = data.insert('Projects',**k)
        if seqid > -1:
            value = data.select('Projects',where='id=%s'%seqid)
            cache.set('Projects',value.id,value)
            return True
        else:
            return False
