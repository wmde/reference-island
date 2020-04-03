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


def test_get_usages(monkeypatch):
    # TODO: Improve the test
    def mock_query(sparql):
        assert sparql.queryString == """SELECT ?item ?value
WHERE {
?item wdt:P1 ?value
}
LIMIT 10"""
        return MockResponse()

    monkeypatch.setattr(SPARQLWrapper, "query", mock_query)

    WdqsReader('Fake UA', 'https://fakewebsite').get_usecases('P1')


def test_get_schemaorg_mapping(monkeypatch):
    # TODO: Improve the test
    def mock_query(sparql):
        assert sparql.queryString == """SELECT ?property ?url
WHERE {
  ?property wdt:P1628 ?url.
  FILTER(STRSTARTS(str(?url), "http://schema.org")).
}"""
        return MockResponse()

    monkeypatch.setattr(SPARQLWrapper, "query", mock_query)

    WdqsReader('Fake UA', 'https://fakewebsite').get_schemaorg_mapping()
