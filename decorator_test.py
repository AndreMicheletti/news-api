"""

 MY DECORATORS 

Some decorator usages

"""

# Require Login
def require_login(function):
	def wrap(*args, **kw):
		if(check_login()):
			return function(*args, **kw)
		else:
			print("Not logged in")
	return wrap
		

		
# Check if file exists and if not, create
def ensure_file(function):
	def wrap(filename):
		import os
		if not(os.path.isfile(filename)):
			with open(filename, 'w') as file:
				file.write('')
		return function(filename)
	return wrap
	
	
	
# Same as before, but the filename is passed by the decorator (function arguments are free)
def ensure_file2(filename):
	def _decorator(function):
		def wrap(*args, **kw):
			import os
			if not(os.path.isfile(filename)):
				with open(filename, 'w') as file:
					file.write('')
			return function(*args, **kw)
		return wrap
	return _decorator

	

# Ensure that all string arguments are formatted 
def string_format(function):

	# define here how the string should be formatted
	def _format(_str):
		return _str.lower().strip()
		
	def wrap(*args, **kw):
	
		# format all strings in *arguments
		args = [_format(arg) for arg in args if (isinstance(arg, str))]
		
		# format all strins in **keyword arguments
		for key in kw.keys():
			if (isinstance(kw[key], str)):
				kw[key] = _format(kw[key])
				
		# execute the original function
		return function(*args, **kw)
	return wrap
	
	
	
# Cache a function's result
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

			
			
# Time a function
def timer(func):
	def wrapper(*args, **kw):
		import time
		t = time.time()
		result = func(*args, **kw)
		print("call to {0} took {1:f} seconds".format(str(func.__name__), time.time() - t))
		return result
	return wrapper


	
# DECORATOR CLASS for maintaining profile history
import os
import json
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
"""

DECORATOR TESTS

"""
if (__name__ == "__main__"):

	def test_mystuff(benchmark):
		benchmark(process)
	
	@timer
	@cached
	def large_function(n):
		import time
		time.sleep(1.1)
		return n + 2
		
	def process():
		large_function(2)
		large_function(2)
	
	process()
	
	@string_format
	def echo(*args, **kw):
		for str in args:
			print(str)
		for str in kw.values():
			print (str)
		
	echo("a ", "   b ")
	echo(" D ")
	echo(" EF                       ", arg1='           f        ', arg2=' G            ')

"""			
https://www.turnkeylinux.org/blog/python-optimization
"""