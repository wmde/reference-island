import os
import json
import shutil

import pytest
import requests

from wikidatarefisland import run_main
from wikidatarefisland.data_access import WdqsReader
from wikidatarefisland.services import WdqsExternalIdentifierFormatter


@pytest.fixture()
def test_directory(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('directory')
    conf_dir = tmpdir.mkdir('config')
    tmpdir.mkdir('scripts')
    tmpdir.mkdir('data')
    config_file = conf_dir.join('default.yml')
    override_file = conf_dir.join('override.yml')
    override_file.write('')
    yaml_path = os.path.join(os.path.dirname(__file__), '../config/default.yml')
    shutil.copy(yaml_path, config_file.strpath)
    return tmpdir


def test_main_ss1(monkeypatch, test_directory):
    def mock_external_ids(_):
        return ['P1234']

    def mock_usecases(*args):
        return [{'value': {'value': 'cat1234'}}] * 6

    def mock_formatter(*args):
        return {
            'url': 'http://example.com/cat1234',
            'referenceMetadata': {}  # not needed here; leaked in from SS4
        }

    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.text = 'http://schema.org'
                self.status_code = 200

        return MockResponse()

    monkeypatch.setattr(WdqsReader, "get_all_external_identifiers", mock_external_ids)
    monkeypatch.setattr(WdqsReader, "get_usecases", mock_usecases)
    monkeypatch.setattr(WdqsExternalIdentifierFormatter, "format", mock_formatter)
    monkeypatch.setattr(requests, "get", mock_get)

    test_filename = "test_result_ss1.json"
    mock_args = f"this_is_ignored.py --step ss1 --output {test_filename}"
    mock_file_path = test_directory.join('scripts', 'this_is_ignored.py')
    result_file = test_directory.join('data', test_filename)

    run_main(mock_args.split(), mock_file_path)

    assert json.loads(result_file.read()) == ['P1234']
