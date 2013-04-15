import config, memcache

def posts(**k):
    #result = config.DB.select('Posts',order='id desc',**k)
    
    if 'where' in k:
        post = config.MC.get('post_%s'%str(k['where']))
        if post:
            return post
        else:
            post = config.DB.select('Posts',order='id desc',**k)
            if post:
                val = [x for x in post]
                config.MC.set('post_%s'%str(k['where']),val[0])
                return val[0]
            else:
                return None
    else:
        posts = config.MC.get('posts_all')
        if posts:
            return posts
        else:
            posts = config.DB.select('Posts',order='id desc',**k)
            if posts:
                vals = [p for p in posts]
                config.MC.set('posts_all',vals)
                return vals
            else:
                return None
