from SPARQLWrapper import JSON, SPARQLWrapper


class WdqsReader(object):
    def __init__(self, user_agent, url):
        self.user_agent = user_agent
        self.url = url

    def get_sparql_data(self, query):
        sparql = SPARQLWrapper(self.url, agent=self.user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()['results']['bindings']

    def get_usecases(self, pid):
        query = """SELECT ?item ?value
WHERE {
?item wdt:""" + pid + """ ?value
}

LIMIT 10
        """
        return self.get_sparql_data(query)

    def get_schemaorg_mapping(self):
        query = """SELECT ?property ?url
WHERE {
  ?property wdt:P1628 ?url.
  FILTER(STRSTARTS(str(?url), "http://schema.org")).
}"""
        return self.get_sparql_data(query)

    @classmethod
    def newFromConfig(cls, config):
        return cls(config.get('user_agent'), config.get('wdqs_url'))
