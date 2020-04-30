import pytest

from wikidatarefisland.data_model.wikibase.value_types import TextValue, QuantityValue

from mock_data import mock


class TestQuantityValue:

    @pytest.mark.parametrize("statement,equivalent", [
        (mock["statement"]["with_quantity"], "12")
    ])
    def test_equivalence(self, statement, equivalent):
        assert QuantityValue(statement) == equivalent


class TestTextValue:

    @pytest.mark.parametrize("statement,equivalent", [
        (mock["statement"]["with_string"], "Test"),
        (mock["statement"]["with_url"], "Test"),
        (mock["statement"]["with_monolingualtext"], "Test"),
        (mock["statement"]["with_string"], "test"),
        (mock["statement"]["with_string"], "  Test ")
    ])
    def test_equivalence(self, statement, equivalent):
        assert TextValue(statement) == equivalent
