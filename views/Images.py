import web
import views
import models

def thumbnails(albumid):
    images = models.Images.urlsForAlbumId(albumid)
    return views.render.images.thumbnail(images)

def upload():
    return views.render.images.upload()