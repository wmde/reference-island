import os
import concurrent.futures

import requests

from wikidatarefisland.config import BLACKLISTED_EXTERNAL_IDENTIFIERS
from wikidatarefisland.external_identifier import ExternalIdentifier
from wikidatarefisland.storage import Storage
from wikidatarefisland.wdqs_reader import WdqsReader


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


def check_external_identifier(pid, formatter_url):
    wdqs_reader = WdqsReader()
    print('Checking {0}'.format(pid))
    usecases = wdqs_reader.get_usecases(pid)
    return check_cases(usecases, formatter_url)


def main():
    external_identifier_tools = ExternalIdentifier()
    storage = Storage.newFromScript(os.path.realpath(__file__))
    external_identifiers = storage.get('external_idefs.json')
    try:
        final_results = storage.get('ext_idef_check_result.json')
    except:
        final_results = {}

    pids = {}
    for i in external_identifiers:
        if i in final_results or i in BLACKLISTED_EXTERNAL_IDENTIFIERS:
            continue
        formatter_url = external_identifier_tools.get_formatter(i)
        if not formatter_url:
            print('{0} does not have a formatter'.format(i))
            continue
        pids[i] = formatter_url

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_pid = {executor.submit(check_external_identifier, i, pids[i]): i for i in pids}
        for future in concurrent.futures.as_completed(future_to_pid):
            pid = future_to_pid[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (pid, exc))
            else:
                final_results[pid] = data
                storage.store('ext_idef_check_result.json', final_results)

    data = storage.get('ext_idef_check_result.json')
    print('Total: ', len(data))
    goods = []
    schemas = []
    for i in data:
        if data[i][1] > 5:
            goods.append(i)
        if data[i][2] > 5:
            schemas.append(i)
    print('Good: ', len(goods))
    print('Schemas: ', len(schemas))
    storage.store('whitelisted_ext_idefs.json', schemas)


if __name__ == "__main__":
    main()
