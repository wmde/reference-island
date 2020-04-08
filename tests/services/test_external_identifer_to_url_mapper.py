from wikidatarefisland.services import WdqsExternalIdentifierToUrlMapper


class MockWdqsReader():
    def get_sparql_data(self, *args, **kwars):
        return [{'property': {'value': 'http://www.wikidata.org/entity/P1'},
                 'formatter': {'value': 'https://example.com/$1'}}]


def test_get_formatter(monkeypatch):
    external_identifier_to_url_mapper = WdqsExternalIdentifierToUrlMapper(MockWdqsReader())
    res = external_identifier_to_url_mapper .get_formatter('P1')
    assert res == ['https://example.com/$1']
