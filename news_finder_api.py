"""
DECORATOR functions
"""
def require_arguments(required):
	def wrap(f):
		def new_f(_self):
			args = parser.parse_args()
			for arg in required:
				if (args[arg] == None or args[arg] == ''):
					abort(403, message="Please provide the argument {}".format(arg))
			return f(_self)
		return new_f
	return wrap
# END

import string
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

# Dictionary of know sites
sites = {
	'globo.com': {
		'tag':'p',
		'class':'hui-premium__title'
	},
	'nytimes.com': {
		'tag':'',
		'class':'story-heading'
	},
	'veja.abril.com.br': {
		'tag':'a',
		'class':'widget-home-box-list-item-title-a'
	}
}

parser = reqparse.RequestParser()
parser.add_argument('limit')
parser.add_argument('website')
parser.add_argument('tag')
parser.add_argument('class')

# Core search function - it uses the dictionary to search news on the websites
def search_news(site, limit=5):
	url = 'http://' + site
	tag = sites[site]['tag']
	class_ = sites[site]['class']
	html = requests.get(url).content.decode('utf-8')
	soup = BeautifulSoup(html, 'html.parser')
	result = []
	i = 0
	for tag in soup.find_all(tag, class_):
		if (i == limit): break
		if (tag.string != None):
			result.append(tag.string.strip())
			i += 1
	return result


# A Resource to list the available sites or include new ones
class NewsSites(Resource):

	def get(self):
		array = [key for key in sites.keys()]
		return {'sites' : array } 
	
	@require_arguments(['website','tag','class'])
	def put(self):
		args = parser.parse_args()
		website = args['website'].replace('http','').replace(':','').replace('//','')
		test = requests.get('http://' + website)
		if (test.status_code == 200):
			sites[website] = { 'tag' : args['tag'], 'class' : args['class'] }
			return sites[website], 201
		else:
			abort(403, message="{} is not a valid website".format(website))
		

# This Resource will list the news specified website
class NewsList(Resource):

	def get(self, site):
		if (site == None):
			return 'Usage: put the news site name after / (example: /globo.com)'
		site = site.lower().replace(' ','')
		if not(site in sites.keys()):
			abort(403, message="The website '{}' is not valid. Try /list to see the list".format(site))
		args = parser.parse_args()
		limit = 5
		if ((args['limit'] != None) and (args['limit']) != ''):
			limit = int(args['limit'])
		return search_news(site, limit)

		
# This Resource can seach on all available websites for news that match a keyword
class NewsFinder(Resource):

	def get(self, query):
		result = { 'found' : {} }
		limit = 5
		args = parser.parse_args()
		if ((args['limit'] != None) and (args['limit']) != ''):
			limit = int(args['limit'])
		for key in sites.keys():
			array = []
			for news in search_news(key, limit):
				if (query in news):
					array.append(news)
				
			result['found'][key] = array
		return result
	
	
api.add_resource(NewsSites, '/', '/sites', '/list')
api.add_resource(NewsList, "/<string:site>")
api.add_resource(NewsFinder, "/search/<string:query>")
		
if (__name__ == "__main__"):
	app.run(debug=True)