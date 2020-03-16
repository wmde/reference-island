import requests
import json
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict

blacklisted_properties = [
    'P646'
]


def get_sparql_data(query):
    user_agent = "github.com/Ladsgroup/reference-island Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper('https://query.wikidata.org/sparql', agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()['results']['bindings']


def get_usecases(pid):
    query = """SELECT ?item ?value
WHERE
{
  ?item wdt:""" + pid + """ ?value
}

LIMIT 10
    """
    return get_sparql_data(query)


def get_formatter_urls():
    query = """
    SELECT ?property ?formatter
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


def check_cases(usecases, formatter_urls_for_id):
    total_number = 0
    good_responses = 0
    schema_org_responses = 0
    for case in usecases:
        total_number += 1
        value = case['value']['value']
        url = formatter_urls_for_id[0].replace('$1', value)
        try:
            r = requests.get(url)
        except:
            continue
        if r.status_code == 200:
            good_responses += 1
        if 'http://schema.org' in r.text:
            schema_org_responses += 1
    return total_number, good_responses, schema_org_responses


with open('external_idefs.json', 'r') as f:
    external_identifiers = json.loads(f.read())

formatter_urls = get_formatter_urls()
final_results = {}
for i in external_identifiers:
    if i not in formatter_urls:
        print('{0} does not have a formatter'.format(i))
        continue
    print('Checking {0}'.format(i))
    usecases = get_usecases(i)
    final_results[i] = check_cases(usecases, formatter_urls[i])
    with open('ext_idef_check_result.json', 'w') as f:
        f.write(json.dumps(final_results))
