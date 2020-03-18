from SPARQLWrapper import JSON, SPARQLWrapper


class WdqsReader(object):
    def __init__(self):
        self.user_agent = "github.com/wmde/reference-island Python3"
        self.url = 'https://query.wikidata.org/sparql'

    def get_sparql_data(self, query):
        sparql = SPARQLWrapper(self.url, agent=self.user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()['results']['bindings']
