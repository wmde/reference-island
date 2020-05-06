import json
import pytest
from wikidatarefisland.pipes import ItemExtractorPipe
import importlib.resources as pkg_resources
from . import test_data


@pytest.fixture
def input_data():
    return json.loads(pkg_resources.read_text(
        test_data,
        'item_extractor_pipe_input_test_data.json'
    ))


def test_pipe1_integration(input_data, tmp_path):
    #  TODO: add test cases covering blacklisted properties and the whitelisted external ids
    pipe = ItemExtractorPipe((lambda pid, value: {}), ['P26'])
    result = pipe.flow(input_data)
    expected_data = json.loads(
        pkg_resources.read_text(
            test_data, 'item_extractor_pipe_expected_data.jsonl'
        )
    )
    assert result[0] == expected_data
