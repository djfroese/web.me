import web
import views
import models

def thumbnails():
    #images = models.Images.urlsForAlbumId(albumid)
    images = models.Images.all()
    return views.render.images.thumbnail(images)

def upload():
    return views.render.images.upload()