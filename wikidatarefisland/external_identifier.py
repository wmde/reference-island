from collections import defaultdict

from .wdqs_reader import WdqsReader


class ExternalIdentifier(object):
    def __init__(self):
        self.formatter_urls = {}
        self.wdqs_reader = WdqsReader()

    def get_formatter(self, pid):
        if self.formatter_urls == {}:
            self._populate_formatter_urls()
        return self.formatter_urls.get(pid)

    def _populate_formatter_urls(self):
        query = """
    SELECT ?property ?formatter
WHERE
{
  ?property wdt:P1630 ?formatter
}
    """
        self.formatter_urls = defaultdict(list)
        for case in self.wdqs_reader.get_sparql_data(query):
            pid = case['property']['value'].replace('http://www.wikidata.org/entity/', '')
            self.formatter_urls[pid].append(case['formatter']['value'])
