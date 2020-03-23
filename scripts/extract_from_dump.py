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
storage.store('unrefed_statements.jsonl', '', raw=True)
storage.store('usable_ext_idefs.jsonl', '', raw=True)
unrefed_statements = []
usable_ext_idefs = []
for item_serialization in dump_reader.read_items():
    item_id = item_serialization['id']
    item = Item(item_id, item_serialization)
    if item.hasPropertyItemValue('P31', BLACKLISTED_ITEMS):
        continue

    if int(item_id[1:]) % 1000 == 0:
        print(item_id)
        storage.append(
            'unrefed_statements.jsonl',
            '\n'.join([json.dumps(i, ensure_ascii=False) for i in unrefed_statements]),
            raw=True)
        storage.append(
            'usable_ext_idefs.jsonl',
            '\n'.join([json.dumps(i, ensure_ascii=False) for i in usable_ext_idefs]),
            raw=True)
        usable_ext_idefs = []
        unrefed_statements = []
    (unrefed_statements_item, ext_idefs) = inspect_statements(item)
    if not unrefed_statements_item or not ext_idefs:
        continue
    for ext_idef in ext_idefs:
        usable_ext_idefs.append([item_id, *ext_idef])
    for unrefed_statement in unrefed_statements_item:
        unrefed_statements.append([item_id, *unrefed_statement])
