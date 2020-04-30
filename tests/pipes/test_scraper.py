import requests
import os

from wikidatarefisland import Config
from wikidatarefisland.pipes import ScraperPipe
from wikidatarefisland.services import SchemaorgPropertyMapper


class MockResponse:
    def __init__(self, url):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, '../data/test_response.html'), 'r') as f:
            self.text = f.read()
        self.status_code = 200
        self.url = url


class MockSchemaorgPropertyMapper(SchemaorgPropertyMapper):
    def get_mapping(self):
        return [
            {'property': 'P321', 'url': 'http://schema.org/director'},
            {'property': 'P123', 'url': 'http://schema.org/name'},
        ]


class MockConfig(Config):
    def __init__(self):
        pass

    def get(self, key):
        if key == 'user_agent':
            return 'Test'
        if key == 'parallel_workers':
            return 20


class MockSchemaorgNormalizer():
    @staticmethod
    def normalize_from_extruct(data):
        return {
            "http://schema.org/director": [
                data['microdata'][0]['director']['name']
            ],
            "http://schema.org/genre": [
                data['microdata'][0]['genre']
            ]
        }


def test_run(monkeypatch):
    def mock_get(url, *args, **kwargs):
        return MockResponse(url)

    monkeypatch.setattr(requests, "get", mock_get)
    item = {
        'itemId': 'Q42',
        'resourceUrls': [{
            'url': 'https://example_with_schema.org/wow',
            'referenceMetadata': {'a': 'b'}
        }],
        'statements': [{
            "pid": "P321",
            "datatype": "wikibase-item",
            "value": {
                "numeric-id": 214917,
                "id": "Q214917"
            }
        }]
    }
    scraper = ScraperPipe(MockConfig(), MockSchemaorgNormalizer, MockSchemaorgPropertyMapper())
    result = scraper.flow(item)
    assert 'dateRetrieved' in result[0]['reference']['referenceMetadata']
    assert len(result) == 1
    del result[0]['reference']['referenceMetadata']['dateRetrieved']
    assert result[0] == {
        'statement': {
            'pid': 'P321',
            'datatype': 'wikibase-item',
            'value': {'numeric-id': 214917, 'id': 'Q214917'}},
        'itemId': 'Q42',
        'reference': {'referenceMetadata': {'a': 'b'},
                      'extractedData': ['James Cameron']}}
