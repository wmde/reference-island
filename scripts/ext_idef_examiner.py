import os

import requests

from wikidatarefisland.config import BLACKLISTED_EXTERNAL_IDENTIFIERS
from wikidatarefisland.external_identifier import ExternalIdentifier
from wikidatarefisland.storage import Storage
from wikidatarefisland.wdqs_reader import WdqsReader

wdqs_reader = WdqsReader()
external_identifier_tools = ExternalIdentifier()
storage = Storage.newFromScript(os.path.realpath(__file__))


def get_usecases(pid):
    query = """SELECT ?item ?value
WHERE
{
  ?item wdt:""" + pid + """ ?value
}

LIMIT 10
    """
    return wdqs_reader.get_sparql_data(query)


def check_cases(usecases, formatter_urls_for_id):
    total_number = 0
    good_responses = 0
    schema_org_responses = 0
    for case in usecases:
        total_number += 1
        value = case['value']['value']
        url = formatter_urls_for_id[0].replace('$1', value)
        try:
            r = requests.get(url, timeout=30)
        except:
            continue
        if r.status_code == 200:
            good_responses += 1
        if 'http://schema.org' in r.text:
            schema_org_responses += 1
    return total_number, good_responses, schema_org_responses


external_identifiers = storage.get('external_idefs.json')
try:
    final_results = storage.get('ext_idef_check_result.json')
except:
    final_results = {}

for i in external_identifiers:
    if i in final_results or i in BLACKLISTED_EXTERNAL_IDENTIFIERS:
        continue
    formatter_url = external_identifier_tools.get_formatter(i)
    if not formatter_url:
        print('{0} does not have a formatter'.format(i))
        continue
    print('Checking {0}'.format(i))
    usecases = get_usecases(i)
    final_results[i] = check_cases(usecases, formatter_url)
    storage.store('ext_idef_check_result.json', final_results)
