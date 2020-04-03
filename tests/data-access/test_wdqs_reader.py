import pytest
from SPARQLWrapper import SPARQLWrapper

from wikidatarefisland.data_access import WdqsReader


class MockResponse:
    @staticmethod
    def convert():
        return {"results": {"bindings": [{'a': 'b'}]}}


@pytest.fixture
def mock_response(monkeypatch):
    def mock_query(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(SPARQLWrapper, "query", mock_query)


def test_get_sparql_data(mock_response):
    result = WdqsReader('Fake UA', 'https://fakewebsite').get_sparql_data('Wrong query')
    assert result == [{'a': 'b'}]
