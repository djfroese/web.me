import web

db_name = 'dev'
db_app = 'sqlite'

# whether to cache the rendered templates
cache = False

debugmode = True

DB = web.database(dbn=db_app,db=db_name)
