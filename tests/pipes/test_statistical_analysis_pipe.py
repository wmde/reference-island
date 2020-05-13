import pytest

from wikidatarefisland.pipes import ItemStatisticalAnalysisPipe
from .test_data import mock_data as test_data


given = {
    "item": {
        "not_item_value_type": [{
            **test_data.REFERENCE_LINE,
            'statement': {
                "pid": test_data.NON_BLACKLISTED_PROPERTY,
                "datatype": 'string',
                "value": 'wow'
            }
        }],
        "one_item": [test_data.EXAMPLE_LINE],
        "three_items_with_noise": [
            test_data.EXAMPLE_LINE,
            test_data.EXAMPLE_LINE,
            {
                **test_data.REFERENCE_LINE,
                'statement': {
                    "pid": test_data.NON_BLACKLISTED_PROPERTY,
                    "datatype": test_data.DATATYPE,
                    "value": {
                        "entity-type": "item",
                        "numeric-id": 191788,
                        "id": "Q191788"
                    }
                },
                'reference': test_data.EXAMPLE_LINE['reference']
            }
        ],
    },
}
expected = {
    "mapping": {
        "no_mapping": {},
        "empty_mapping": {test_data.WHITELISTED_EXT_ID: {test_data.NON_BLACKLISTED_PROPERTY: {}}},
        "simple_mapping": {test_data.WHITELISTED_EXT_ID: {
            test_data.NON_BLACKLISTED_PROPERTY: {'bar': 191789, 'foo': 191789}
        }}
    },
    "repetitions": {
        "one_item": 0,
        "at_least_two": 1
    },
    "noise": {
        "unacceptable_noise": 0,
        "lots_of_noise": 0.4
    }
}


class TestItemExtractorPipe:
    @pytest.mark.parametrize("given,expected,repetitions,noise", [
        (
                given["item"]["not_item_value_type"],
                expected["mapping"]["no_mapping"],
                expected["repetitions"]["one_item"],
                expected["noise"]["unacceptable_noise"],
        ),
        (
                given["item"]["one_item"],
                expected["mapping"]["simple_mapping"],
                expected["repetitions"]["one_item"],
                expected["noise"]["unacceptable_noise"],
        ),
        (
                given["item"]["one_item"],
                expected["mapping"]["empty_mapping"],
                expected["repetitions"]["at_least_two"],
                expected["noise"]["unacceptable_noise"],
        ),
        (
                given["item"]["three_items_with_noise"],
                expected["mapping"]["empty_mapping"],
                expected["repetitions"]["one_item"],
                expected["noise"]["unacceptable_noise"],
        ),
        (
                given["item"]["three_items_with_noise"],
                expected["mapping"]["simple_mapping"],
                expected["repetitions"]["at_least_two"],
                expected["noise"]["lots_of_noise"],
        ),
    ])
    def test_flow(self, given, expected, repetitions, noise):
        whitelisted_ext_ids = [test_data.WHITELISTED_EXT_ID]
        pipe = ItemStatisticalAnalysisPipe(whitelisted_ext_ids, repetitions, noise)
        for case in given:
            pipe.flow(case)

        assert dict(pipe.get_mapping()) == expected
