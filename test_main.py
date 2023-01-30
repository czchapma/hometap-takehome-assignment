from api import create_app
import json
import pytest
import pprint
from flask import current_app

# "sewer": "septic"
def test_has_septic(client):
    response = client.get('/has-septic-system?address=101 Main St&zipcode=02142&testData=success-sewer-septic')
    assert 200 == response.status_code
    assert b'has_septic\":true' in response.data

# "sewer": "municipal"
def test_has_municipal(client):
    response = client.get('/has-septic-system?address=101 Main St&zipcode=02142&testData=success-sewer-municipal')
    assert 200 == response.status_code
    assert b'has_septic\":false' in response.data

# "sewer": "yes"
def test_has_sewer_yes(client):
    response = client.get('/has-septic-system?address=101 Main St&zipcode=02142&testData=success-sewer-yes')
    assert 200 == response.status_code
    assert b'has_septic\":false' in response.data

# "sewer": "none"
def test_has_sewer_none(client):
    response = client.get('/has-septic-system?address=101 Main St&zipcode=02142&testData=success-sewer-none')
    assert 200 == response.status_code
    assert b'has_septic\":false' in response.data

def test_204_error(client):
    response = client.get('/has-septic-system?address=101 Main St&zipcode=02142&testData=failure-204')
    assert 204 == response.status_code
    assert b'Septic status unknown for this address' in response.data

def test_400_error(client):
    response = client.get('/has-septic-system?address=101 Main St&zipcode=02142&testData=failure-400')
    assert 400 == response.status_code
    assert b'"address":"Missing required parameter in the query string"' in response.data

def test_401_error(client):
    response = client.get('/has-septic-system?address=101 Main St&zipcode=02142&testData=failure-401')
    assert 401 == response.status_code
    assert b'Authentication Failed with Home Canary API' in response.data
def test_429_error(client):
    response = client.get('/has-septic-system?address=101 Main St&zipcode=02142&testData=failure-429')
    assert 429 == response.status_code
    assert b'Rate limit reached for Home Canary API. Try again later.' in response.data
