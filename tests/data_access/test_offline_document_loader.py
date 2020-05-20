import pytest
from wikidatarefisland.data_access.offline_document_loader import OfflineDocumentLoader

MOCK_CONTEXT = {'fake': 'context'}


@pytest.fixture
def loader():
    return OfflineDocumentLoader(MOCK_CONTEXT)


def test_non_schema_org_url(loader):
    url = 'http://example.com'
    assert loader.get_loader(url) == {
        'contextUrl': None,
        'document': {},
        'documentUrl': url
    }


def test_schema_org_url(loader):
    url = 'http://schema.org'
    assert loader.get_loader(url) == {
        'contextUrl': None,
        'document': MOCK_CONTEXT,
        'documentUrl': url
    }
