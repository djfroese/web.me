import web, memcache

db_name = 'dev'
db_app = 'sqlite'

# whether to cache the rendered templates
cache = False
debugmode = True

#memcache server list
server_list = ['192.168.1.26:11211']

DB = web.database(dbn=db_app,db=db_name)
MC = memcache.Client(server_list,debug=1)
