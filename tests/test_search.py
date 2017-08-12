from app import create_flask_app
from unittest import mock
from mock import patch
from flask import Flask, Response
from app.search import SearchEngine, search_blueprint
import pytest
import json

""" MOCKING """
def mocked_seach_news(site, limit=5):
	from itertools import cycle
	mock_news_data = cycle([
		 "Combustível com alta de imposto já chegou a postos, diz sindicato"
		,"Motorista vai gastar R$ 18 a mais para encher o tanque com reajuste"
		,"Governo aumentou tributo a limite máximo previsto em lei, diz Fisco"
		,"Governo diminuiu tributo a limite minimo previsto em lei"
		,"Galo anuncia Rogério Micale, técnico do ouro olímpico no Rio"
		,"Helicóptero faz pouso forçado em praia do Rio"
		,"Meirelles dorme enquanto Temer fala na Argentina"
		,"PF nega ter recebido verba para passaporte"
		,"Justiça condena Agnelo Queiroz e advogado no DF"
		,"Bilhete de filho do cantor do Linkin Park comove: 'Ame a vida'"
	])
	search_news_result = []
	for i in range(limit):
		search_news_result.append(next(mock_news_data))
	return search_news_result


SEARCH_BLUEPRINT_PREFIX = "/search"

@pytest.fixture()
def test_app():
	class ClientTest(object):
		flask_app = create_flask_app(search_blueprint_prefix=SEARCH_BLUEPRINT_PREFIX)
		flask_app.testing = True
		client = flask_app.test_client()
		def get(self, url):
			return ClientTest.client.get(SEARCH_BLUEPRINT_PREFIX + url)
		def put(self, url):
			return ClientTest.client.put(SEARCH_BLUEPRINT_PREFIX + url)
	client_test = ClientTest()
	return client_test

"""
GIVEN: the News app
WHEN: GET request on listing endpoints
THEN: response code should be 200 OK
"""

@pytest.fixture(params=["/","/sites","/list"])
def listing_endpoints(request):
	return request.param

def test_200_ok(test_app, listing_endpoints):
	response = test_app.get(listing_endpoints)
	assert response.status_code == 200


"""
GIVEN: the News app
WHEN: GET request on Search by Site
THEN: response code should be 200 OK if arguments valid and 404 otherwise
"""

@pytest.fixture(params=[
	# Tuple with: (input, expected output=[status_code, total_items_found])
	  ("/site/", [404, 0])
	 ,("/site/?limit=5", [404, 0])
	 ,("/site/?nonsense_arg", [404, 0])
	 ,("/site/?limit=", [404, 0])
	 ,("/site/notexist", [404, 0])
	 ,("/site/globo.com", [200, 5])
	 ,("/site/globo.com?limit=5", [200, 5])
	 ,("/site/globo.com?limit=25", [200, 25])
	 ,("/site/globo.com?limit=100", [200, 100])
	 ,("/site/globo.com?limit=", [200, 5])
])
def site_searching(request):
	return request.param

@patch.object(SearchEngine, 'search_news', mocked_seach_news)
def test_site_searching(test_app, site_searching):
	from typing import List
	( the_input, expected_output ) = site_searching
	response = test_app.get(the_input)
	assert response.status_code == expected_output[0]
	str_response = response.data.decode('utf-8')
	if (response.status_code == 200):
		json_data = json.loads(str_response)
		assert len(json_data) <= expected_output[1]


"""
GIVEN: the News app
WHEN: GET request on Search by Site
THEN: response code should be 200 OK if arguments valid and 404 otherwise
"""

@pytest.fixture(params=[
	# Tuple with: (input, expected output=[status_code, total_items_found])
	("/Governo", [200, 5])
	,("/Governo?limit=25", [200, 25])
	,("/Governo?limit=", [200, 5])
])
def string_searching_data(request):
	return request.param

@patch.object(SearchEngine, 'search_news', mocked_seach_news)
def test_string_searching(test_app, string_searching_data):
	( the_input, expected_output ) = string_searching_data
	response = test_app.get(the_input)
	assert response.status_code == expected_output[0]
	str_response = response.data.decode('utf-8')
	if (response.status_code == 200):
		json_data = json.loads(str_response)
		for url_key in list(json_data["found"]):
			assert len(json_data["found"][url_key]) <= expected_output[1]


"""
GIVEN: the News app
WHEN: PUT request on listing endpoints
THEN: response code should be 200 OK if arguments valid and 404 otherwise
"""

@pytest.fixture(params=[
	("/", [404, "Please provide"])
	,("/?website=", [404, "Please provide"])
	,("/?tag=&?class=", [404, "Please provide"])
	,("/?website=glo.bocom&tag=p&class=hui-premium__title", [404, ""])
	,("/?website=forsurethisurldoesnotexist.com&tag=p&class=hui-premium__title", [404, ""])
	,("/?website=globo.com&tag=p&class=hui-premium__title", [201, ""])
])
def site_put(request):
	return request.param

@patch.object(SearchEngine, 'search_news', mocked_seach_news)
def test_site_put(test_app, site_put):
	( the_input, expected_output ) = site_put
	response = test_app.put(the_input)
	assert response.status_code == expected_output[0]
	assert expected_output[1] in response.data.decode('utf8')
