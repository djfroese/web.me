import config, memcache

def posts(**k):
    #result = config.DB.select('Posts',order='id desc',**k)
    
    if 'where' in k:
        print 'where found - should only show if requesting one post'
        post = config.MC.get('post_%s'%str(k['where']))
        if post:
            print 'Cache Value Found'
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
        print 'where NOT found - should only show if requesting all posts'
        posts = config.MC.get('posts_all')
        if posts:
            print 'Cache Value Found'
            return posts
        else:
            posts = config.DB.select('Posts',order='id desc',**k)
            if posts:
                vals = [p for p in posts]
                config.MC.set('posts_all',vals)
                return vals
            else:
                return None
