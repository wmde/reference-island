import pytest

from wikidatarefisland.pipes import ItemExtractorPipe

from .test_data import mock_data as test_data

given = {
    "item": {
        "without_non_ignored_references": {
            **test_data.ITEM,
            "claims": {
                test_data.NON_SKIPPED_PROPERTY: [
                    test_data.mock["claim"]["with_ignored_references_only"]
                ],
                test_data.ALLOWED_EXT_ID: [
                    test_data.mock["claim"]["with_allowed_external_id"]
                ]
            }
        },
        "without_unreferenced_claims": {
            **test_data.ITEM,
            "claims": {
                test_data.NON_SKIPPED_PROPERTY: [
                    test_data.mock["claim"]["with_references"]
                ]
            }
        },
        "without_non_skipped_properties": {
            **test_data.ITEM,
            "claims": {
                test_data.SKIPPED_PROPERTY: [
                    test_data.mock["claim"]["with_skipped_property"]
                ]
            }
        },
        "without_allowed_external_ids": {
            **test_data.ITEM,
            "claims": {
                test_data.NON_SKIPPED_PROPERTY: [
                    test_data.mock["claim"]["with_any_unreferenced_property"]
                ],
                test_data.NON_ALLOWED_EXT_ID: [
                    test_data.mock["claim"]["with_any_external_id"]
                ]
            }
        },
        "without_ignored_classes": {
            **test_data.ITEM,
            "claims": {
                test_data.NON_SKIPPED_PROPERTY: [
                    test_data.mock["claim"]["with_any_unreferenced_property"]
                ],
                test_data.ALLOWED_EXT_ID: [
                    test_data.mock["claim"]["with_allowed_external_id"]
                ],
                test_data.INSTANCE_OF_PROPERTY: [
                    test_data.mock["claim"]["with_ignored_class"]
                ]
            }
        },
        "with_all": {
            **test_data.ITEM,
            "claims": {
                test_data.NON_SKIPPED_PROPERTY: [
                    test_data.mock["claim"]["with_any_unreferenced_property"]
                ],
                test_data.ALLOWED_EXT_ID: [
                    test_data.mock["claim"]["with_allowed_external_id"]
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
        (given["item"]["without_non_ignored_references"], [expected["line"]["with_all"]]),
        (given["item"]["without_unreferenced_claims"], []),
        (given["item"]["without_non_skipped_properties"], []),
        (given["item"]["without_ignored_classes"], []),
        (given["item"]["without_allowed_external_ids"], []),
        (given["item"]["with_all"], [expected["line"]["with_all"]])
    ])
    def test_flow(self, given, expected):
        external_id_formatter = MockExternalIdFormatter()
        skipped_properties = [test_data.SKIPPED_PROPERTY]
        allowed_ext_ids = [test_data.ALLOWED_EXT_ID]
        imported_from_properties = [test_data.IGNORED_REFERENCE_PROPERTY]
        ignored_classes = [test_data.IGNORED_CLASS]

        pipe = ItemExtractorPipe(
            external_id_formatter,
            skipped_properties,
            allowed_ext_ids,
            ignored_classes,
            imported_from_properties)

        assert pipe.flow(given) == expected
