import pytest

from wikidatarefisland.data_model import statement_filterer

mock_statement = {"pid": "P1"}


@pytest.mark.parametrize(
    "filters,statements,expected",
    [
        ([(lambda x: True)], [mock_statement], [mock_statement]),
        ([(lambda x: False)], [mock_statement], []),
    ]
)
def test_filter_statements(filters, statements, expected):
    filterer = statement_filterer.StatementFilterer(filters)
    assert list(filterer.filter_statements(statements)) == expected
