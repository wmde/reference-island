import requests

from wikidatarefisland.external_identifiers import GenerateWhitelistedExtIds


class MockResponse:
    def __init__(self, url):
        self.text = 'http://schema.org' if 'with_schema' in url else 'wow'
        self.status_code = 200


class MockWdqsReader():
    def get_usecases(self, pid, limit=10):
        return [{'item': {'value': 'Q42'}, 'value': {'value': '1234'}}] * 10

    def get_formatter(self, pid):
        if pid == 'P1':
            return ['https://example_with_schema.org/$1']
        return ['https://example_without_schema.org/$1']

    def get_all_external_identifiers(self):
        return ['P1', 'P2', 'P3']


class MockStorage():
    def __init__(self):
        self.values = {}

    def get(self, key):
        return self.values.get(key, {})

    def store(self, key, value):
        self.values[key] = value


class MockConfig():
    def get(self, key):
        if key == 'blacklisted_properties':
            return ['P3']


def test_run(monkeypatch):
    def mock_get(url, *args, **kwargs):
        return MockResponse(url)

    monkeypatch.setattr(requests, "get", mock_get)
    storage = MockStorage()
    generate_whitelisted_ext_id = GenerateWhitelistedExtIds(MockWdqsReader(), storage, MockConfig())
    whitelist = generate_whitelisted_ext_id.run()
    assert whitelist == ['P1']
    assert storage.get(generate_whitelisted_ext_id.result_file_name) == \
        {'P1': (10, 10, 10), 'P2': (10, 10, 0)}
