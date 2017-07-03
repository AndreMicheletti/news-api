class cache_return(object):
	def __init__(self, func):
		self.func = func
		self.cache = {}
	def __call__(self, *args):
		if not isinstance(args, collections.Hashable):
			return self.func(*args)
		if (args in self.cache):
			return self.cache[args]
		else:
			value = self.func(args)
			self.cache[args] = value
			return value

			
