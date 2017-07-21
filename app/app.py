from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from app.search import search_blueprint

def create_flask_app(search_blueprint_prefix='/search'):
	app = Flask(__name__)
	app.register_blueprint(search_blueprint, url_prefix=search_blueprint_prefix)
	return app

if (__name__ == "__main__"): # pragma: no cover
	app = create_flask_app()
	app.run(debug=True)
