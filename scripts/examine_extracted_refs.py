import os
import re
from dateutil import parser
from datetime import datetime
from collections import defaultdict

from wikidatarefisland.storage import Storage

storage = Storage.newFromScript(os.path.realpath(__file__))
matches = 0
mapping = defaultdict(list)
for data in storage.getLines('extracted_refs.jsonl'):
    item = data[0]
    claim = data[1][0]
    value = data[1][1]
    ext_idef_pid = data[2]
    ext_idef_url = data[3]
    # TODO: Fix it for later
    ext_idef_values = []
    for i in data[4]:
        if isinstance(i, list):
            ext_idef_values += i
        else:
            ext_idef_values.append(i)
    retrieved_timestamp = data[5]
    matched = False
    if not isinstance(value, str):
        if isinstance(value, dict):
            if 'text' in value:
                for i in ext_idef_values:
                    try:
                        noramlized_values = [i.lower() for i in ext_idef_values]
                    except:
                        continue
                if value['text'].lower() in noramlized_values:
                    matched = True
            elif 'amount' in value:
                try:
                    noramlized_values = [i.split(' ')[0] for i in ext_idef_values]
                except:
                    continue
                if value['amount'] in noramlized_values or \
                        value['amount'].replace('+', '') in noramlized_values:
                    matched = True
            elif 'time' in value:
                # TODO: Proper parsing

                # Requires python >= 3.7
                try:
                    time_value = datetime.fromisoformat(value['time'][1:][:-1])
                except:
                    pass
                    # Happens when we set the month to zero. Handled below
                try:
                    parsed_values = [parser.parse(i) for i in ext_idef_values]
                except:
                    continue
                if value['precision'] == 11:
                    if time_value.date() in [i.date() for i in parsed_values]:
                        matched = True
                elif value['precision'] == 9:
                    if int(value['time'][1:].split('-')[0]) in [i.year for i in parsed_values]:
                        matched = True
            elif 'latitude' in value:
                # TODO: They should match properly
                latitudes = [round(float(i.get('latitude', 666)), 3) for i in ext_idef_values]
                longtitudes = [round(float(i.get('longitude', 666)), 3) for i in ext_idef_values]
                if round(value['latitude'], 3) in latitudes and \
                        round(value['longitude'], 3) in longtitudes:
                    matched = True
        if not matched:
            pass
        else:
            matches += 1
    elif not re.search(r'^Q\d+$', value):
        if value in ext_idef_values:
            matches += 1
    else:
        for i in ext_idef_values:
            if isinstance(i, str):
                mapping[ext_idef_pid + ':' + i].append(value)
            if isinstance(i, dict) and i.get('name'):
                mapping[ext_idef_pid + ':' + i['name']].append(value)
final_mapping = {}
for case in mapping:
    if len(mapping[case]) < 3:
        continue
    for possible_value in set(mapping[case]):
        if mapping[case].count(possible_value) > (len(mapping[case]) * 0.5):
            final_mapping[case] = possible_value
for data in storage.getLines('extracted_refs.jsonl'):
    if not isinstance(data[1][1], str) or not re.search(r'^Q\d+$', data[1][1]):
        continue
    claim = data[1][0]
    value = data[1][1]
    ext_idef_pid = data[2]
    ext_idef_url = data[3]
    # TODO: Fix it for later
    ext_idef_values = []
    for i in data[4]:
        if isinstance(i, list):
            ext_idef_values += i
        else:
            ext_idef_values.append(i)
    retrieved_timestamp = data[5]
    values = []
    for i in ext_idef_values:
        if isinstance(i, str) and (ext_idef_pid + ':' + i) in final_mapping:
            values.append(final_mapping[ext_idef_pid + ':' + i])
        if isinstance(i, dict) and i.get('name') and \
                (ext_idef_pid + ':' + i['name']) in final_mapping:
            values.append(final_mapping[ext_idef_pid + ':' + i['name']])
    if value in values:
        matches += 1
print(matches)
