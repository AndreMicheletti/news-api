from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from search.search import search_blueprint

app = Flask(__name__)
app.register_blueprint(search_blueprint, url_prefix='/search')


if (__name__ == "__main__"):
	app.run(debug=True)