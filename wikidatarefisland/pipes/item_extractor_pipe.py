from functools import reduce
from itertools import chain

from wikidatarefisland.data_model import StatementFilterer

from ..data_model.filters import ItemFilters, StatementFilters
from .abstract_pipe import AbstractPipe


class ItemExtractorPipe(AbstractPipe):
    """Pipe that extracts statements that could be referenced from an item"""
    def __init__(self, external_id_formatter,
                 skipped_properties=None,
                 allowed_ext_ids=None,
                 ignored_classes=None,
                 ignored_reference_properties=[]):
        self.external_id_formatter = external_id_formatter
        if skipped_properties is None:
            skipped_properties = []
        self.skipped_properties = skipped_properties
        if allowed_ext_ids is None:
            allowed_ext_ids = []
        self.allowed_ext_ids = allowed_ext_ids
        if ignored_classes is None:
            ignored_classes = []
        self.ignored_classes = ignored_classes
        self.ignored_reference_properties = ignored_reference_properties

    def flow(self, input_data):
        item_class_excluder = ItemFilters().get_item_class_excluder(self.ignored_classes)
        if item_class_excluder(input_data) is False:
            return []
        return self._process_item(input_data)

    def _process_item(self, item_data):
        all_statements = list(chain.from_iterable([i for i in item_data['claims'].values()]))
        result_statements = list(self._filter_potential_referenced_statements(
            all_statements))
        resource_urls = list(self._extract_potential_resource_urls(all_statements))

        if not result_statements or not resource_urls:
            return []

        return [{
            'itemId': item_data['id'],
            'statements': result_statements,
            'resourceUrls': resource_urls
        }]

    def _extract_potential_resource_urls(self, all_statements):
        statement_filters = StatementFilters()

        external_id_statements = list(filter(
            statement_filters.get_property_id_statement_includer(self.allowed_ext_ids),
            all_statements
        ))
        resource_urls = map(self._format_external_id, external_id_statements)
        return resource_urls

    def _format_external_id(self, statement):
        pid = statement.get('mainsnak', {}).get('property', '')
        value = statement.get('mainsnak', {}).get('datavalue', {}).get('value', '')
        resource_url = self.external_id_formatter.format(pid, value)
        return resource_url

    def _filter_potential_referenced_statements(self, all_statements):
        statement_filters = StatementFilters()
        ref_statement_filters = [
            lambda statement: statement is not None,
            statement_filters.get_referenced_statement_excluder(self.ignored_reference_properties),
            statement_filters.external_id_statement_excluder,
            statement_filters.get_property_id_statement_excluder(self.skipped_properties)
        ]
        potentially_ref_statement_filterer = StatementFilterer(
            ref_statement_filters
        )
        filtered_statements = potentially_ref_statement_filterer.filter_statements(
            all_statements)
        result_statements = reduce(_extract_statement, filtered_statements, [])
        return result_statements


def _extract_statement(acc, statement):
    pid = statement.get('mainsnak', {}).get('property')
    datatype = statement.get('mainsnak', {}).get('datatype')
    datavalue = statement.get('mainsnak', {}).get('datavalue', {}).get('value')

    if pid is None or datatype is None or datavalue is None:
        return acc
    acc.append({
        'pid': pid,
        'datatype': datatype,
        'value': datavalue
    })
    return acc
