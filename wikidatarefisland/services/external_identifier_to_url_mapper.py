from collections import defaultdict


class ExternalIdentifierToUrlMapper(object):
    """ Side-step 4: Mapper of property id to list of formatters for that property"""
    def get_formatter(self, pid):
        raise NotImplementedError


class WdqsExternalIdentifierToUrlMapper(ExternalIdentifierToUrlMapper):
    def __init__(self, wdqs_reader):
        """
        :type wdqs_reader: .wdqs_reader.WdqsReader
        """
        self.wdqs_reader = wdqs_reader
        self._formatter_urls = {}

    def get_formatter(self, pid):
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
