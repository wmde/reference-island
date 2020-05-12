import pytest

from wikidatarefisland.pipes import ItemExtractorPipe
from .test_data import mock_data as test_data

given = {
    "item": {
        "without_unreferenced_claims": {
            **test_data.ITEM,
            "claims": {
                test_data.NON_BLACKLISTED_PROPERTY: [
                    test_data.mock["claim"]["with_references"]
                ]
            }
        },
        "without_non_blacklisted_properties": {
            **test_data.ITEM,
            "claims": {
                test_data.BLACKLISTED_PROPERTY: [
                    test_data.mock["claim"]["with_blacklisted_property"]
                ]
            }
        },
        "without_whitelisted_external_ids": {
            **test_data.ITEM,
            "claims": {
                test_data.NON_BLACKLISTED_PROPERTY: [
                    test_data.mock["claim"]["with_any_unreferenced_property"]
                ],
                test_data.NON_WHITELISTED_EXT_ID: [
                    test_data.mock["claim"]["with_any_external_id"]
                ]
            }
        },
        "with_all": {
            **test_data.ITEM,
            "claims": {
                test_data.NON_BLACKLISTED_PROPERTY: [
                    test_data.mock["claim"]["with_any_unreferenced_property"]
                ],
                test_data.WHITELISTED_EXT_ID: [
                    test_data.mock["claim"]["with_whitelisted_external_id"]
                ]
            }
        }
    }
}

expected = {
    "line": {
        "with_all": {
            **test_data.LINE,
            "statements": [test_data.STATEMENT_BLOB],
            "resourceUrls": [test_data.RESOURCE_BLOB]
        }
    }
}


class MockExternalIdFormatter:
    def format(self, *args):
        return test_data.RESOURCE_BLOB


class TestItemExtractorPipe:
    @pytest.mark.parametrize("given,expected", [
        (given["item"]["without_unreferenced_claims"], []),
        (given["item"]["without_non_blacklisted_properties"], []),
        (given["item"]["without_whitelisted_external_ids"], []),
        (given["item"]["with_all"], [expected["line"]["with_all"]])
    ])
    def test_flow(self, given, expected):
        external_id_formatter = MockExternalIdFormatter()
        blacklisted_properties = [test_data.BLACKLISTED_PROPERTY]
        whitelisted_ext_ids = [test_data.WHITELISTED_EXT_ID]
        pipe = ItemExtractorPipe(external_id_formatter, blacklisted_properties, whitelisted_ext_ids)

        assert pipe.flow(given) == expected
