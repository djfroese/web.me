import web, datetime
import utils, config, views
from views import *
import models

class upload(utils.WebRequestHandler):
    def GET(self):
        return views.render.base(views.Images.upload(),user=self.user)
    
    def POST(self):
        #if not self.user:
        #    raise web.seeother('/_upload')
        
        x = web.input(image={})
        web.debug(x['image'].filename) # This is the filename
        #web.debug(x['image'].value) # This is the file contents
        #web.debug(x['image'].file.read()) # Or use a file(-like) object
        if 'image' in x:
            if 'alt' in x:
                alt_text = x.alt
            else:
                alt_text = ''
            
            models.Images.addImage(file=x.image, alt_text=alt_text)
        
        raise web.seeother('/_upload')

class thumbnail(utils.WebRequestHandler):
    def GET(self,albumid):
        return views.render.base(views.Images.thumbnail(albumid),user=self.user)

