Wikidata Reference Island
-------------------------

This is a pipeline to extract references for Wikidata using extrenal identifiers.

# Usage
In order to install the framework part, do: ``python3 setup.py install``

# Extracting data
You can use ``make`` but you need to determine `DUMP_PATH` enviromental variable which is the path to json dump of wikidata entities (the gzipped one). The default value is the path to the dump in stat machines (like stat1007)

This for example works just fine:

``DUMP_PATH='data/latest-all.json.gz' make``


If you're in stat1007:

``make``
