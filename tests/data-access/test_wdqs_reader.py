import pytest
from SPARQLWrapper import SPARQLWrapper

from wikidatarefisland.data_access import WdqsReader


class MockResponse:
    def __init__(self, res=[{'a': {'value': 'b'}}]):
        self.res = res

    def convert(self):
        return {"results": {"bindings": self.res}}


@pytest.fixture
def mock_response(monkeypatch):
    def mock_query(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(SPARQLWrapper, "query", mock_query)


def test_get_sparql_data(mock_response):
    result = WdqsReader('Fake UA', 'https://fakewebsite').get_sparql_data('SELECT ?a ?b ?c')
    assert result == [{'a': {'value': 'b'}}]


def test_get_usages(monkeypatch):
    # TODO: Improve the test
    def mock_query(sparql):
        assert sparql.queryString == """SELECT ?item ?value
WHERE {
?item wdt:P1 ?value
}
LIMIT 42"""
        return MockResponse()

    monkeypatch.setattr(SPARQLWrapper, "query", mock_query)

    WdqsReader('Fake UA', 'https://fakewebsite').get_usecases('P1', 42)


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


def test_get_formatter(monkeypatch):
    def mock_query(*args, **kwargs):
        return MockResponse([{'property': {'value': 'http://www.wikidata.org/entity/P1'},
                              'formatter': {'value': 'https://example.com/$1'}}])

    monkeypatch.setattr(SPARQLWrapper, "query", mock_query)

    res = WdqsReader('Fake UA', 'https://fakewebsite').get_formatter('P1')
    assert res == ['https://example.com/$1']


def test_get_all_external_identifiers(monkeypatch):
    def mock_query(*args, **kwargs):
        return MockResponse([{'externalIdProps': {'value': 'http://www.wikidata.org/entity/P42'}}])

    monkeypatch.setattr(SPARQLWrapper, "query", mock_query)

    res = WdqsReader('Fake UA', 'https://fakewebsite').get_all_external_identifiers()
    assert res == ['P42']
