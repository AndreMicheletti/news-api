from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from search.search import search_blueprint

def create_app():
	app = Flask(__name__)
	app.register_blueprint(search_blueprint, url_prefix='/search')
	return app

if (__name__ == "__main__"):
	app = create_app()
	app.run(debug=True)