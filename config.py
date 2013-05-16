import web, memcache

db_name = 'dev'
db_app = 'sqlite'

# Storing images folder location
staticImagePath = '/Users/david/Documents/Projects/web.me/static/uploads'

# whether to cache the rendered templates
cache = False
debugmode = True

#memcache server list
server_list = ['127.0.0.1:11211']

DB = web.database(dbn=db_app,db=db_name)
MC = memcache.Client(server_list,debug=1)
