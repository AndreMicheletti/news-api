from flask import Blueprint
from flask_restful import Api, Resource, abort

feed_blueprint = Blueprint('feed', __name__)
api = Api(feed_blueprint)

feed_emails = {
	'andreluizmtmicheletti@gmail.com' : {
		 'sites' : []
		,'words' : ['Lula']
	}
}

class FeedManager(Resource):

	def get(self):
		return feed_emails

	def put(self):