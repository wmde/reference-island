class SchemaorgPropertyMapper(object):
    """ Side-step 2: Mapper of Wikidata properties and schema.org properties"""
    def get_mapping(self):
        raise NotImplementedError


class WdqsSchemaorgPropertyMapper(SchemaorgPropertyMapper):
    def __init__(self, wdqs_reader):
        """

        :type wdqs_reader: wikidatarefisland.data_access.WdqsReader
        """
        self.wdqs_reader = wdqs_reader
        self._mapping = {}

    def get_mapping(self):
        if self._mapping == {}:
            self._populate_mapping()
        return self._mapping

    def _populate_mapping(self):
        query = """SELECT ?property ?url
WHERE {
  ?property wdt:P1628 ?url.
  FILTER(STRSTARTS(str(?url), "http://schema.org")).
}"""
        self._mapping = [{
            'property': i['property']['value'].replace('http://www.wikidata.org/entity/', ''),
            'url': i['url']['value']
        } for i in self.wdqs_reader.get_sparql_data(query)]
