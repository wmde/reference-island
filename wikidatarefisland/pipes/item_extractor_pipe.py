from functools import reduce
from itertools import chain

from wikidatarefisland.data_model import StatementFilterer

from ..data_model.filters import StatementFilters
from .abstract_pipe import AbstractPipe


class ItemExtractorPipe(AbstractPipe):
    """Pipe that extracts statements that could be referenced from an item"""
    def __init__(self, external_id_formatter,
                 blacklisted_properties=None, whitelisted_ext_ids=None):
        self.external_id_formatter = external_id_formatter
        if blacklisted_properties is None:
            blacklisted_properties = []
        self.blacklisted_properties = blacklisted_properties
        if whitelisted_ext_ids is None:
            whitelisted_ext_ids = []
        self.whitelisted_ext_ids = whitelisted_ext_ids

    def flow(self, input_data):
        return self._process_item(input_data)

    def _process_item(self, item_data):
        # TODO: Filter out bail early if item is in excluded list. see: T251282
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
            statement_filters.get_property_id_statement_includer(self.whitelisted_ext_ids),
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
            statement_filters.referenced_statement_excluder,
            statement_filters.external_id_statement_excluder,
            statement_filters.get_property_id_statement_excluder(self.blacklisted_properties)
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
