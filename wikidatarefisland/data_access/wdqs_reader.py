from collections import defaultdict

from SPARQLWrapper import JSON, SPARQLWrapper


class WdqsReader(object):
    def __init__(self, user_agent, url):
        self.user_agent = user_agent
        self.url = url
        self._formatter_urls = {}

    def get_sparql_data(self, query):
        sparql = SPARQLWrapper(self.url, agent=self.user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()['results']['bindings']

    def get_usecases(self, pid, limit=10):
        query = """SELECT ?item ?value
WHERE {
?item wdt:""" + pid + """ ?value
}
LIMIT """ + str(limit)
        return self.get_sparql_data(query)

    def get_schemaorg_mapping(self):
        query = """SELECT ?property ?url
WHERE {
  ?property wdt:P1628 ?url.
  FILTER(STRSTARTS(str(?url), "http://schema.org")).
}"""
        return self.get_sparql_data(query)

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
        for case in self.get_sparql_data(query):
            pid = case['property']['value'].replace('http://www.wikidata.org/entity/', '')
            self._formatter_urls[pid].append(case['formatter']['value'])

    def get_all_external_identifiers(self):
        query = """SELECT ?externalIdProps
WHERE {
  ?externalIdProps wikibase:propertyType <http://wikiba.se/ontology#ExternalId> .
}"""

        return [
            i['externalIdProps']['value'].replace('http://www.wikidata.org/entity/', '')
            for i in self.get_sparql_data(query)]

    @classmethod
    def newFromConfig(cls, config):
        return cls(config.get('user_agent'), config.get('wdqs_url'))
