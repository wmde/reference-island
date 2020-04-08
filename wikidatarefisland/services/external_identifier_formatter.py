from collections import defaultdict


class ExternalIdentifierFormatter(object):
    """ Side-step 4: Mapper of property id to list of formatters for that property"""
    def get_formatter(self, pid):
        raise NotImplementedError


class WdqsExternalIdentifierFormatter(ExternalIdentifierFormatter):
    def __init__(self, wdqs_reader):
        """
        :type wdqs_reader: .wdqs_reader.WdqsReader
        """
        self.wdqs_reader = wdqs_reader
        self._formatter_urls = {}
        self._representing_items = {}

    def format(self, pid, value):
        formatter = self._get_formatter(pid)
        if not formatter:
            return False
        data = {
            'url': formatter[0].replace('$1', value),
            'referenceMetadata': {pid: value}
        }
        item = self._get_representing_item(pid)
        if not item:
            return data
        data['referenceMetadata']['P248'] = item
        return data

    def _get_formatter(self, pid):
        if self._formatter_urls == {}:
            self._populate_formatter_urls()
        return self._formatter_urls.get(pid)

    def _populate_formatter_urls(self):
        query = """SELECT ?property ?formatter
WHERE {
  ?property wdt:P1630 ?formatter
}"""
        self._formatter_urls = defaultdict(list)
        for case in self.wdqs_reader.get_sparql_data(query):
            pid = case['property']['value'].replace('http://www.wikidata.org/entity/', '')
            self._formatter_urls[pid].append(case['formatter']['value'])

    def _get_representing_item(self, pid):
        if self._representing_items == {}:
            self._populate_representing_items()
        return self._representing_items.get(pid)

    def _populate_representing_items(self):
        query = """SELECT ?property
  (COUNT(?value) AS ?var2)
  (GROUP_CONCAT(DISTINCT ?value; SEPARATOR = ", ") AS ?item)
WHERE {
  ?property wdt:P1629 ?value.
   ?property wikibase:propertyType wikibase:ExternalId.
}
GROUP BY ?property
HAVING(?var2 = 1)"""
        self._representing_items = {}
        for case in self.wdqs_reader.get_sparql_data(query):
            pid = case['property']['value'].replace('http://www.wikidata.org/entity/', '')
            self._representing_items[pid] = case['item']['value'] \
                .replace('http://www.wikidata.org/entity/', '')
