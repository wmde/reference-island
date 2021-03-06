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


def test_get_all_external_identifiers(monkeypatch):
    def mock_query(*args, **kwargs):
        return MockResponse([{'externalIdProps': {'value': 'http://www.wikidata.org/entity/P42'}}])

    monkeypatch.setattr(SPARQLWrapper, "query", mock_query)

    res = WdqsReader('Fake UA', 'https://fakewebsite').get_all_external_identifiers()
    assert res == ['P42']
