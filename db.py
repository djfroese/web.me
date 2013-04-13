import config

def posts(**k):
	return config.DB.select('Posts',order='id desc',**k)
