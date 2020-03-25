import json
import os
import pprint
from collections import OrderedDict, defaultdict
from time import gmtime, strftime

import extruct
import requests
from w3lib.html import get_base_url

from wikidatarefisland.external_identifier import ExternalIdentifier
from wikidatarefisland.storage import Storage
from wikidatarefisland.wdqs_reader import WdqsReader

storage = Storage.newFromScript(os.path.realpath(__file__))
wdqs_reader = WdqsReader()
whitelisted_ext_idefs = storage.get('whitelisted_ext_idefs.json')
external_identifier = ExternalIdentifier()
pp = pprint.PrettyPrinter(indent=4)
schemaorg_mapping = wdqs_reader.get_schemaorg_mapping()
wtf_mapping = defaultdict(list)
for case in schemaorg_mapping:
    wtf_mapping[case['url']['value']].append(case['property']['value'])

non_existing_schemaorg_types = defaultdict(int)


def extract_external_idef_data(pid, value):
    extracted_data = {}
    formatter_urls = external_identifier.get_formatter(pid)
    if not formatter_urls:
        return extracted_data
    url = formatter_urls[0].replace('$1', value)
    try:
        r = requests.get(url, timeout=30)
        base_url = get_base_url(r.text, r.url)
        data = extruct.extract(r.text, base_url=base_url)
        if not data.get('microdata') and not data.get('json-ld'):
            return extracted_data
    except KeyboardInterrupt:
        raise
    except:
        return extracted_data
    for datum in data.get('json-ld', []):
        for property_ in datum:
            if property_.startswith('@'):
                continue
            if not datum[property_]:
                continue
            if 'http://schema.org/' + property_ in wtf_mapping:
                value_pid = wtf_mapping['http://schema.org/' + property_][0]
                value_pid = value_pid.replace('http://www.wikidata.org/entity/', '')
                data_set = extracted_data.get(value_pid, [])
                if not datum[property_] in data_set:
                    data_set.append(datum[property_])
                extracted_data[value_pid] = data_set
            else:
                non_existing_schemaorg_types[property_] += 1
    for datum in data.get('microdata', []):
        for property_ in datum.get('properties', []):
            if not datum['properties'][property_]:
                continue
            if 'http://schema.org/' + property_ in wtf_mapping:
                value_pid = wtf_mapping['http://schema.org/' + property_][0]
                value_pid = value_pid.replace('http://www.wikidata.org/entity/', '')
                data_set = extracted_data.get(value_pid, [])
                if not datum['properties'][property_] in data_set:
                    data_set.append(datum['properties'][property_])
                extracted_data[value_pid] = data_set
            else:
                non_existing_schemaorg_types[property_] += 1
    return extracted_data


def check_data(item_data):
    extracted_data = dict()
    ext_idefs = item_data['ext_idefs']
    unrefed_statements = item_data['unrefed_statements']
    item_id = item_data['item_id']
    final_final_data = []
    for ext_idef in ext_idefs:
        key = ext_idef[0] + ':' + ext_idef[1]
        extracted_data[key] = extract_external_idef_data(ext_idef[0], ext_idef[1])
    for ext_idef in extracted_data:
        for pid in extracted_data[ext_idef]:
            if not extracted_data[ext_idef][pid]:
                continue
            for claim in unrefed_statements:
                if claim[0] != pid:
                    continue
                ext_idef_property = ext_idef.split(':')[0]
                ext_idef_value = ':'.join(ext_idef.split(':')[1:])
                formatter_urls = external_identifier.get_formatter(ext_idef_property)
                url = formatter_urls[0].replace('$1', ext_idef_value)
                data = [
                    item_id,
                    claim,
                    ext_idef_property,
                    url,
                    extracted_data[ext_idef][pid],
                    strftime("%Y-%m-%d %H:%M:%S", gmtime())
                ]
                print(data)
                final_final_data.append(data)

    return final_final_data


def main():
    final_res = storage.getLines('final_data.jsonl')
    try:
        checked_items = storage.get('checked_items.json')
    except:
        checked_items = {}

    for item_data in final_res:
        if item_data['item_id'] in checked_items:
            continue
        data = check_data(item_data)
        checked_items[item_data['item_id']] = True
        storage.append(
            'extracted_refs.jsonl',
            '\n'.join([json.dumps(i, ensure_ascii=False) for i in data]),
            raw=True)
        storage.store('checked_items.json', checked_items)

    ordered_stats = OrderedDict(
        sorted(non_existing_schemaorg_types.items(), key=lambda t: t[1],
               reverse=True))
    storage.store('non_existing_schemaorg_types.json', ordered_stats)


if __name__ == "__main__":
    main()
