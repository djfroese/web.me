import os, utils, config
from datastore import data, cache

class Images:
        
    @classmethod
    def url(self, imgid):
        image = cache.get('Images',imgid)
        if not image:
            image = data.select('Images',where='id="%s"'%imgid)
            if not image:
                return None
            else:
                cache.set('Images',imgid,image)
        
        return image.url
    
    @classmethod
    def urlsForAlbum(self, albumid):
        album = cache.get('Images',albumid)
        if not album:
            album = data.select('Images',where='album_id="%s"'%albumid)
            if not album:
                return None
            else:
                cache.set('Images',albumid,album)
        
        return [image.url for image in album]


    @classmethod
    def storeImage(self, imageFile):
        #filepath=imageFile.filename.replace('\\','/')
        filestr = imageFile.file.read()
        filename=utils.createHashID(filestr)
        path = config.staticImagePath + '/' + filename + '.jpg'
        print path
        fout = open(path,'w')
        fout.write(filestr)
        fout.close()
        return filename
    
    @classmethod
    def addImage(self, file, alt_text=''):
        # take file and store in static files images.
        filename = self.storeImage(file)
        url = '../static/'+filename+'.jpg'
        # insert into db
        print alt_text
        data.insert('Images', url=url, id=filename, alt=alt_text)
    
    ############################################################################
    # 
    # METHODS NOT CURRENTLY IN USE. HERE FOR POSSIBLE FUTURE USE.
    #
    ############################################################################
    @classmethod
    def imageExists(self,imgid):
        path = "%s/%s.jpeg"%(config.staticImagePath,imgid)
        if os.path.isfile(path):
            try:
                with open(path): pass
                return True
            except IOError:
                return False
        else:
            return False
    
    