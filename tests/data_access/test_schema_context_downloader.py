from json import JSONDecodeError
from unittest.mock import MagicMock

import requests

from wikidatarefisland.data_access import SchemaContextDownloader


class MockResponse:
    def __init__(self, valid_json=True, json_response=None):
        if json_response is None:
            json_response = {}
        self.json_response = json_response
        self.valid_json = valid_json

    def json(self):
        if self.valid_json:
            return self.json_response
        else:
            raise JSONDecodeError('Fake', 'Fake2', 123)


def test_uses_schema_org_if_possible(monkeypatch):
    mock_result = {"mock_key": "mock_response"}

    def mock_get(*args, **kwargs):
        return MockResponse(True, mock_result)
    monkeypatch.setattr(requests, "get", mock_get)
    assert SchemaContextDownloader.download('fake_user_agent') == mock_result


def test_falls_back(monkeypatch):
    mock_result = {"mock_key": "mock_response"}

    mock_get = MagicMock()
    mock_get.side_effect = [MockResponse(False), MockResponse(True, mock_result)]

    monkeypatch.setattr(requests, "get", mock_get)
    assert SchemaContextDownloader.download('fake_user_agent') == mock_result
    assert mock_get.call_count == 2
