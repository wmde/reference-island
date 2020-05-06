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
    },
    "no_datetime_match": {
        "statement": mock["statement"]["with_datetime"]["day_precision"],
        "reference": mock["reference"]["without_match"]
    },
    "single_day_match": {
        "statement": mock["statement"]["with_datetime"]["day_precision"],
        "reference": mock["reference"]["with_one_day_match"]
    },
    "single_month_match": {
        "statement": mock["statement"]["with_datetime"]["month_precision"],
        "reference": mock["reference"]["with_one_day_match"]
    },
    "single_year_match": {
        "statement": mock["statement"]["with_datetime"]["year_precision"],
        "reference": mock["reference"]["with_one_year_match"]
    },
    "multiple_datetime_match": {
        "statement": mock["statement"]["with_datetime"]["day_precision"],
        "reference": mock["reference"]["with_multiple_values_match"]
    },
    "invalid_globe-coordinate": {
        "statement": mock["statement"]["with_globe-coordinate"]["on_mars"]
    },
    "no_globe-coordinate_match": {
        "statement": mock["statement"]["with_globe-coordinate"]["on_earth"],
        "reference": mock["reference"]["without_match"]
    },
    "single_globe-coordinate_match": {
        "statement": mock["statement"]["with_globe-coordinate"]["on_earth"],
        "reference": mock["reference"]["with_one_geo_match"]
    },
    "multiple_globe-coordinate_match": {
        "statement": mock["statement"]["with_globe-coordinate"]["on_earth"],
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

    @pytest.mark.parametrize("given,expected", [
        (given["no_type"], False),
        (given["invalid_globe-coordinate"], False),
        (given["no_globe-coordinate_match"], False),
        (given["single_globe-coordinate_match"], True),
        (given["multiple_globe-coordinate_match"], True),
    ])
    def test_match_geo(self, given, expected):
        assert ValueMatchers.match_geo(given) == expected

    @pytest.mark.parametrize("given,expected", [
        (given["no_type"], False),
        (given["no_datetime_match"], False),
        (given["single_day_match"], True),
        (given["single_month_match"], False),
        (given["single_year_match"], True),
        (given["multiple_datetime_match"], True),
    ])
    def test_match_datetime(self, given, expected):
        assert ValueMatchers.match_datetime(given) == expected
