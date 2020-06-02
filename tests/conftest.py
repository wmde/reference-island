import os

import pytest
import requests

from wikidatarefisland.services import WdqsSchemaorgPropertyMapper


class MockResponse:
    def __init__(self, url):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, 'data/test_response.html'), 'r') as f:
            self.text = f.read()
        self.status_code = 200
        self.url = url


class MockSession():
    def __init__(self):
        self.headers = {}

    def get(self, url, *args, **kwargs):
        return MockResponse(url)


@pytest.fixture
def mock_wdqs_schemaorg_property_mapper(monkeypatch):
    def get_mapping(_):
        return [
            {'property': 'P321', 'url': 'http://schema.org/director'},
            {'property': 'P123', 'url': 'http://schema.org/name'},
        ]

    monkeypatch.setattr(WdqsSchemaorgPropertyMapper, "get_mapping", get_mapping)


@pytest.fixture
def mock_response(monkeypatch):
    def mock_get(url, *args, **kwargs):
        return MockResponse(url)

    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr(requests, "Session", MockSession)
