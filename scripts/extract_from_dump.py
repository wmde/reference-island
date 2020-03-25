import json
import os
import sys

from wikidatarefisland.config import BLACKLISTED_ITEMS, CLASSIFYING_PROPERTIES
from wikidatarefisland.dump_reader import DumpReader
from wikidatarefisland.item import Item
from wikidatarefisland.storage import Storage

storage = Storage.newFromScript(os.path.realpath(__file__))

external_identifiers = storage.get('external_idefs.json')
whitelisted_ext_idefs = storage.get('whitelisted_ext_idefs.json')


def inspect_statements(item):
    ext_idefs = []
    unrefed_statements = []
    for pid in item.getClaims():
        if pid in CLASSIFYING_PROPERTIES:
            continue
        if pid in whitelisted_ext_idefs:
            for claim in item.getPropertyClaims(pid):
                ext_idefs.append((pid, claim.getValue()))
            continue
        if pid in external_identifiers:
            continue
        for claim in item.getPropertyClaims(pid):
            if not claim.hasValidReference():
                if claim.hasItemValue():
                    unrefed_statements.append((pid, claim.getItemValue()))
                else:
                    unrefed_statements.append((pid, claim.getValue()))

    return (unrefed_statements, ext_idefs)


dump_reader = DumpReader(sys.argv[1])
storage.store('final_data.jsonl', '', raw=True)
final_data = []
for item_serialization in dump_reader.read_items():
    item_id = item_serialization['id']
    item = Item(item_id, item_serialization)
    if item.hasPropertyItemValue('P31', BLACKLISTED_ITEMS):
        continue

    if int(item_id[1:]) % 1000 == 0:
        print(item_id)
        storage.append(
            'final_data.jsonl',
            '\n'.join([json.dumps(i, ensure_ascii=False) for i in final_data]),
            raw=True)
        final_data = []
    (unrefed_statements_item, ext_idefs) = inspect_statements(item)
    if not unrefed_statements_item or not ext_idefs:
        continue
    final_data.append(
        {'item_id': item_id,
         'ext_idefs': ext_idefs,
         'unrefed_statements': unrefed_statements_item})
