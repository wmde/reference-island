import pytest

from wikidatarefisland.pipes.value_matcher_pipe import ValueMatcherPipe

given = {
    "string_match": {
        "method": "match_text",
        "return": True
    },
    "string_mismatch": {
        "method": "match_text",
        "return": False
    },
    "number_match": {
        "method": "match_quantity",
        "return": True
    },
    "number_mismatch": {
        "method": "match_quantity",
        "return": False
    },
    "geo_match": {
        "method": "match_geo",
        "return": True
    },
    "geo_mismatch": {
        "method": "match_geo",
        "return": False
    }
}


class MockMatchers:
    @staticmethod
    def match_text(potential_match):
        return False

    @staticmethod
    def match_quantity(potential_match):
        return False

    @staticmethod
    def match_geo(potential_match):
        return False


class TestValueMatcherPipe:

    @pytest.mark.parametrize("mock,expected", [
        (given["string_match"], ["Test"]),
        (given["string_mismatch"], []),
        (given["number_match"], ["Test"]),
        (given["number_mismatch"], []),
        (given["geo_match"], ["Test"]),
        (given["geo_mismatch"], [])
    ])
    def test_flow(self, monkeypatch, mock, expected):
        monkeypatch.setattr(MockMatchers, mock["method"], lambda potential_match: mock["return"])

        pipe = ValueMatcherPipe(MockMatchers)

        assert pipe.flow("Test") == expected
