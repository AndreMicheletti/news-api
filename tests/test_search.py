
from news.app import create_app
import unittest
from flask import Flask, Response
import pytest


prefix = "/search"

app = create_app()
app.testing = True

client = app.test_client()

"""
GIVEN: the News app
WHEN: GET request on listing endpoints
THEN: response code should be 200 OK
"""

@pytest.fixture(params=["/","/sites","/list"])
def listing_endpoints(request):
	return request.param

def test_200_ok(listing_endpoints):
	response = client.get(prefix + listing_endpoints)
	assert response.status_code == 200


"""
GIVEN: the News app
WHEN: GET request on Search by Site
THEN: response code should be 200 OK if arguments valid and 404 otherwise
"""

@pytest.fixture(params=[
	# Tuple with: (input, expected output=[status_code, message])
	 ("/site/", [404, ""])
	 ,("/site/?limit=5", [404, ""])
	 ,("/site/?nonsense_arg", [404, ""])
	 ,("/site/?limit=", [404, ""])
	 ,("/site/notexist", [404, "is not valid"])
	 ,("/site/globo.com", [200, "["])
	 ,("/site/globo.com?limit=5", [200, "["])
	 ,("/site/globo.com?limit=", [200, "["])
])
def site_searching(request):
	return request.param

def test_site_searching(site_searching):
	( the_input, expected_output ) = site_searching
	response = client.get(prefix + the_input)
	assert response.status_code == expected_output[0]
	assert expected_output[1] in response.data 


"""
GIVEN: the News app
WHEN: GET request on Search by Site
THEN: response code should be 200 OK if arguments valid and 404 otherwise
"""

@pytest.fixture(params=[
	("/Lula", [200, ""])
	,("/Lula?limit=5", [200, ""])
	,("/Lula?limit=", [200, ""])
])
def string_searching(request):
	return request.param

def test_string_searching(string_searching):
	( the_input, expected_output ) = string_searching
	response = client.get(prefix + the_input)
	assert response.status_code == expected_output[0]
	assert expected_output[1] in response.data 


"""
GIVEN: the News app
WHEN: GET request on Search by Site
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

def test_site_put(site_put):
	( the_input, expected_output ) = site_put
	response = client.put(prefix + the_input, data=[])
	assert response.status_code == expected_output[0]
	assert expected_output[1] in response.data 
