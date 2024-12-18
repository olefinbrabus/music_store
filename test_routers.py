from time import time
import pytest
from app import app

client = app.test_client()


def test_filter_instruments():
    ts = time()
    response = client.get('/instruments?operation=filter&price_min=500&price_max=1500&category_ids=1,2&search=guitar')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    print(f"\n{time() - ts}")


def test_sort_instruments():
    ts = time()
    response = client.get('/instruments?operation=sort&sort_by=price&order=desc&limit=5&offset=0')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    print(f"\n{time() - ts}")


def test_instruments_count_by_category():
    ts = time()
    response = client.get('/instruments?operation=count_by_category')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    print(f"\n{time() - ts}")


def test_recent_instruments():
    ts = time()
    response = client.get('/instruments?operation=recent&days=7')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    print(f"\n{time() - ts}")


def test_instruments_with_categories():
    ts = time()
    response = client.get('/instruments?operation=with_categories')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    print(f"\n{time() - ts}")