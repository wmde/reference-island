import pytest

from wikidatarefisland.data_model.wikibase.value_matchers import ValueMatchers

from mock_data import mock

given = {
    "no_type": {
        "statement": mock["statement"]["without_type"]
    },
    "no_quantity_match": {
        "statement": mock["statement"]["with_quantity"],
        "reference": mock["reference"]["without_match"]
    },
    "single_quantity_match": {
        "statement": mock["statement"]["with_quantity"],
        "reference": mock["reference"]["with_one_quantity_match"]
    },
    "multiple_quantity_match": {
        "statement": mock["statement"]["with_quantity"],
        "reference": mock["reference"]["with_multiple_values_match"]
    },
    "no_string_match": {
        "statement": mock["statement"]["with_string"],
        "reference": mock["reference"]["without_match"]
    },
    "single_string_match": {
        "statement": mock["statement"]["with_string"],
        "reference": mock["reference"]["with_one_string_match"]
    },
    "single_url_match": {
        "statement": mock["statement"]["with_url"],
        "reference": mock["reference"]["with_one_string_match"]
    },
    "single_monolingualtext_match": {
        "statement": mock["statement"]["with_monolingualtext"],
        "reference": mock["reference"]["with_one_string_match"]
    },
    "multiple_string_match": {
        "statement": mock["statement"]["with_string"],
        "reference": mock["reference"]["with_multiple_values_match"]
    }
}


class TestValueMatchers:

    @pytest.mark.parametrize("given,expected", [
        (given["no_type"], False),
        (given["no_string_match"], False),
        (given["single_string_match"], True),
        (given["single_url_match"], True),
        (given["single_monolingualtext_match"], True),
        (given["multiple_string_match"], True),
    ])
    def test_match_text(self, given, expected):
        assert ValueMatchers.match_text(given) == expected

    @pytest.mark.parametrize("given,expected", [
        (given["no_type"], False),
        (given["no_quantity_match"], False),
        (given["single_quantity_match"], True),
        (given["multiple_quantity_match"], True),
    ])
    def test_match_quantity(self, given, expected):
        assert ValueMatchers.match_quantity(given) == expected