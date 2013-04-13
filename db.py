import config

def posts(**k):
	return config.DB.select('Posts',**k)
