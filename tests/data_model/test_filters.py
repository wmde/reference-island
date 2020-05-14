import pytest

from wikidatarefisland.data_model import StatementFilters

IGNORED_REFERENCE_PROPERTY = 'P123'

mock_ignored_reference_statement = {'mainsnak': {'property': 'P1'}, 'references': [
    {'snaks': {IGNORED_REFERENCE_PROPERTY: 'bar'}}
]}
mock_reference_having_statement = {'mainsnak': {'property': 'P1'}, 'references': [
    {'snaks': {
        'foo': 'bar',
        IGNORED_REFERENCE_PROPERTY: 'bar'
    }}
]}
mock_reference_missing_statement = {'mainsnak': {'property': 'P1'}}
mock_external_id_statement = {'mainsnak': {'property': 'P2', 'datatype': 'external-id'}}
mock_p1_statement = {'mainsnak': {'property': 'P1'}}
mock_p2_statement = {'mainsnak': {'property': 'P2'}}


@pytest.fixture
def referenced_statement_excluder():
    return StatementFilters().referenced_statement_excluder


@pytest.fixture
def external_id_statement_excluder():
    return StatementFilters().external_id_statement_excluder


@pytest.fixture
def external_id_statement_includer():
    return StatementFilters().external_id_statement_includer


@pytest.fixture
def get_property_id_statement_excluder():
    return StatementFilters().get_property_id_statement_excluder


@pytest.fixture
def get_property_id_statement_includer():
    return StatementFilters().get_property_id_statement_includer


@pytest.fixture
def get_referenced_statement_excluder():
    return StatementFilters().get_referenced_statement_excluder


@pytest.mark.parametrize(
    "statement,expected",
    [
        (mock_reference_having_statement, False),
        (mock_reference_missing_statement, True)
    ]
)
def test_referenced_statement_excluder(statement, expected, referenced_statement_excluder):
    assert referenced_statement_excluder(statement) == expected


@pytest.mark.parametrize(
    "statement,expected",
    [
        (mock_external_id_statement, False),
        (mock_reference_missing_statement, True)
    ]
)
def test_external_id_statement_excluder(statement, expected, external_id_statement_excluder):
    assert external_id_statement_excluder(statement) == expected


@pytest.mark.parametrize(
    "statement,expected",
    [
        (mock_reference_having_statement, False),
        (mock_reference_missing_statement, True),
        (mock_ignored_reference_statement, True)
    ]
)
def test_imported_statements_includer(statement, expected, get_referenced_statement_excluder):
    assert get_referenced_statement_excluder([IGNORED_REFERENCE_PROPERTY])(statement) == expected


@pytest.mark.parametrize(
    "statement,expected",
    [
        (mock_p1_statement, False),
        (mock_p2_statement, True)
    ]
)
def test_property_id_statement_excluder(statement, expected, get_property_id_statement_excluder):
    assert get_property_id_statement_excluder(['P1'])(statement) == expected


@pytest.mark.parametrize(
    "statement,expected",
    [
        (mock_p1_statement, True),
        (mock_p2_statement, False)
    ]
)
def test_property_id_statement_includer(statement, expected, get_property_id_statement_includer):
    assert get_property_id_statement_includer(['P1'])(statement) == expected
