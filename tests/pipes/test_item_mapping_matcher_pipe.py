import pytest

from wikidatarefisland.pipes import ItemMappingMatcherPipe
from .test_data import mock_data as test_data

given = {
    "item": {
        "not_item_value_type": {
            **test_data.REFERENCE_LINE,
            'statement': {
                "pid": test_data.NON_SKIPPED_PROPERTY,
                "datatype": 'string',
                "value": 'wow'
            }
        },
        "one_item": test_data.EXAMPLE_LINE,
    },
    "mapping": {
        "no_mapping": {},
        "simple_mapping": {
            test_data.ALLOWED_EXT_ID: {test_data.NON_SKIPPED_PROPERTY: {'foo': 191789}}
        },
        "non_matching_mapping_value": {
            test_data.ALLOWED_EXT_ID: {test_data.NON_SKIPPED_PROPERTY: {'baz': 191789}}
        },
        "non_matching_mapping_item": {
            test_data.ALLOWED_EXT_ID: {test_data.NON_SKIPPED_PROPERTY: {'foo': 191788}}
        },
    }
}


class TestItemMappingMatcherPipe:
    @pytest.mark.parametrize("mapping,given,expected", [
        [given["mapping"]["simple_mapping"], given["item"]["not_item_value_type"], []],
        [given["mapping"]["simple_mapping"], given["item"]["one_item"],
         [given["item"]["one_item"]]],
        [given["mapping"]["non_matching_mapping_value"], given["item"]["one_item"], []],
        [given["mapping"]["non_matching_mapping_item"], given["item"]["one_item"], []],
    ])
    def test_flow(self, mapping, given, expected):
        pipe = ItemMappingMatcherPipe(mapping, [test_data.ALLOWED_EXT_ID])

        assert pipe.flow(given) == expected
