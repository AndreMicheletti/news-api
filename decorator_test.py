
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


def benchmark(func):
	def time(*args, **kw):
		import time
		t = time.process_time()
		result = func(*args, **kw)
		print('function {0} with args {1} runs in {2:f} seconds'.format(func.__name__, args ,time.process_time() - t))
		return result
	return time

@benchmark
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