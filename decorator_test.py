
class cached(object):

	def __init__(self, func):
		self.func = func
		self.cache = {}
		self.__name__ = func.__name__
		
	def __call__(self, *args):
		import collections
		if not isinstance(args, collections.Hashable):
			return self.func(*args)
		if (args in self.cache):
			return self.cache[args]
		else:
			value = self.func(*args)
			self.cache[args] = value
			return value

			
import os
import json

#DECORATOR CLASS for maintaining profile history
class profile_and_save(object):
	
	def __init__(self, func):
		self.func = func
		self.__name__ = func.__name__
		self.filename = 'profiler.json'
		if (os.path.isfile(self.filename)):
			with open(self.filename, 'r') as file:
				self.data = json.load(file)
		else:
			self.data = {}
			with open(self.filename, 'w') as file:
				json.dump(self.data, file)
				
	def __call__(self, *args):
		import time
		import datetime
		t1 = time.process_time()
		result = self.func(*args)
		elapsed = time.process_time() - t1
		if not (self.__name__ in self.data.keys()):
			self.data[self.__name__] = {}
		self.data[self.__name__][str(datetime.datetime.now())] = str(elapsed)
		with open(self.filename, 'w') as f:
			json.dump(self.data, f)
		return result


@profile_and_save
@cached
def fib(n):
	a,b = 1,1
	for i in range(n-1):
		a,b = b,a+b
	return a

if (__name__ == '__main__'):
	fib(13000)
	fib(13000)

"""			
https://www.turnkeylinux.org/blog/python-optimization
"""