import os

from wikidatarefisland.storage import Storage
from wikidatarefisland.wdqs_reader import WdqsReader

wdqs_reader = WdqsReader()
storage = Storage.newFromScript(os.path.realpath(__file__))


def main():
    query = """SELECT ?externalIdProps
WHERE
{
  ?externalIdProps wikibase:propertyType <http://wikiba.se/ontology#ExternalId> .
}
    """

    external_idefs = [
        i['externalIdProps']['value'].replace('http://www.wikidata.org/entity/', '')
        for i in wdqs_reader.get_sparql_data(query)]

    storage.store('external_idefs.json', external_idefs)


if __name__ == "__main__":
    main()
    print('Done!')
