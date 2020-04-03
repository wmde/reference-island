import os

from wikidatarefisland.storage import Storage
from wikidatarefisland.wdqs_reader import WdqsReader

wdqs_reader = WdqsReader()
storage = Storage.newFromScript(os.path.realpath(__file__))


def main():
    query = """
    SELECT ?property ?url 
WHERE 
{
  ?property wdt:P1628 ?url.
  FILTER(STRSTARTS(str(?url), "http://schema.org")).
}
    """

    schema_props = [ {'property': i['property']['value'], 'url': i['url']['value']} for i in wdqs_reader.get_sparql_data(query) ]

    storage.store('schema_equiv_props.json', schema_props)


if __name__ == "__main__":
    main()
    print('Generated Schema Equivalent Properties List')
