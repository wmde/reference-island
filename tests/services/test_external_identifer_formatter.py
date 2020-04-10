from wikidatarefisland.services import WdqsExternalIdentifierFormatter


class MockWdqsReader():
    def get_sparql_data(self, query, *args, **kwars):
        if '?formatter' in query:
            return [{'property': {'value': 'http://www.wikidata.org/entity/P1'},
                     'formatter': {'value': 'https://example.com/$1'}}]
        if 'P1629' in query:
            return [{"property": {'value': 'http://www.wikidata.org/entity/P1'},
                     "var2": {'value': 1},
                     "item": {'value': 'http://www.wikidata.org/entity/Q42'}}]


def test_get_formatter():
    external_identifier_formatter = WdqsExternalIdentifierFormatter(MockWdqsReader())
    res = external_identifier_formatter.format('P1', 'valuee')
    assert res == {
        'url': 'https://example.com/valuee',
        'referenceMetadata': {
            'P1': 'valuee',
            'P248': 'Q42'
        }
    }
