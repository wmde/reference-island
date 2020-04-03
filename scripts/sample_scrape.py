import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import sys
import extruct
import pprint
from w3lib.html import get_base_url

with open('data/whitelisted_ext_idefs.json', 'r') as f:
    external_identifiers = json.loads(f.read())

def get_sparql_data(query):
    user_agent = "reference-island Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper('https://query.wikidata.org/sparql', agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()['results']['bindings']

def get_formatter_urls():
    query = """SELECT ?property ?formatter
WHERE
{
  ?property wdt:P1630 ?formatter
}
    """
    pids = defaultdict(list)
    for case in get_sparql_data(query):
        pid = case['property']['value'].replace('http://www.wikidata.org/entity/', '')
        pids[pid].append(case['formatter']['value'])
    return pids

def get_usecases(pid):
    query = """SELECT ?item ?value
WHERE
{
  ?item wdt:""" + pid + """ ?value
}
LIMIT 1
    """
    return get_sparql_data(query)

def check_cases(usecases, formatter_urls_for_id):
    total_number = 0
    extractedData = {}
    for case in usecases:
        total_number += 1
        value = case['value']['value']
        url = formatter_urls_for_id[0].replace('$1', value)
        print(url)
        try:
            r = requests.get(url, timeout=30)
            base_url = get_base_url(r.text, r.url)
            data = extruct.extract(r.text, base_url=base_url)
            extractedData[url] = data
        except Exception as err:
            print(err)
            continue
    return extractedData

formatter_urls = get_formatter_urls()
final_results = {}
for i in external_identifiers:
    if i not in formatter_urls:
        print('{0} does not have a formatter'.format(i))
        continue
    print('Checking {0}'.format(i))
    usecases = get_usecases(i)
    final_results[i] = check_cases(usecases, formatter_urls[i])
    with open('data/ext_idef_check_result_limit10.json', 'w') as f:
        f.write(json.dumps(final_results))