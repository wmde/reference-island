from wikidatarefisland.services import WdqsSchemaorgPropertyMapper


class MockWdqsReader():
    def get_sparql_data(self, *args, **kwars):
        return [
            {"property": {"value": "http://www.wikidata.org/entity/P2360"},
             "url": {"value": "http://schema.org/audience"}},
            {"property": {"value": "http://www.wikidata.org/entity/P304"},
             "url": {"value": "http://schema.org/pagination"}}
        ]


def test_get_mapping():
    property_mapper = WdqsSchemaorgPropertyMapper(MockWdqsReader())
    assert property_mapper.get_mapping() == [
        {'property': 'P2360', 'url': 'http://schema.org/audience'},
        {'property': 'P304', 'url': 'http://schema.org/pagination'}
    ]
