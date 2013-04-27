import views
import models

def list():
    items = models.Projects.getProjects()
    return views.render.projects.list(items)
