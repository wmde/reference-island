import os
import sys
from collections import OrderedDict

from wikidatarefisland.config import BLACKLISTED_ITEMS, CLASSIFYING_PROPERTIES
from wikidatarefisland.dumpreader import DumpReader
from wikidatarefisland.storage import Storage

storage = Storage.newFromScript(os.path.realpath(__file__))

external_identifiers = storage.get('external_idefs.json')
whitelisted_ext_idefs = storage.get('whitelisted_ext_idefs.json')


def remove_blacklisted_items(p31):
    if not p31:
        return False
    for claim in p31:
        try:
            pid = claim['mainsnak']['datavalue']['value'].get('id')
        except:
            continue
        if pid in BLACKLISTED_ITEMS:
            return True
    return False


def handle_statements(claims):
    unrefed_statements = 0
    statements_that_should_have_ref = 0
    ex_idefs = 0
    ext_idefs_stats = {}
    for pid in claims:
        if pid in CLASSIFYING_PROPERTIES:
            continue
        if pid in whitelisted_ext_idefs:
            ex_idefs += len(claims[pid])
            ext_idefs_stats[pid] = len(claims[pid])
            continue
        if pid in external_identifiers:
            continue
        for claim in claims[pid]:
            statements_that_should_have_ref += 1
            if not claim.get('references'):
                unrefed_statements += 1
                continue
            isAllRefsBS = True
            for ref in claim['references']:
                if 'P143' in ref['snaks'] or 'P4656' in ref['snaks']:
                    continue
                isAllRefsBS = False
            if isAllRefsBS:
                unrefed_statements += 1

    return (statements_that_should_have_ref, unrefed_statements, ex_idefs, ext_idefs_stats)


res = {
    'total_total': 0,
    'total_unref': 0,
    'potential_total': 0,
    'potential_unref': 0,
    'good_items': 0,
    'good_items_with_ex_idef': 0,
    'items_checked': 0,
    'total_ex_idefs': 0,
    'fully_refed_items': 0,
    'detailed_stats': 0,
}
ext_idefs_stats = {}

# /mnt/data/xmldatadumps/public/wikidatawiki/entities/latest-all.json.gz
dump_reader = DumpReader(sys.argv[1])
for item in dump_reader.read_items():
    res['items_checked'] += 1
    if remove_blacklisted_items(item['claims'].get('P31')):
        continue
    if int(item['id'][1:]) % 1000 == 0:
        ordered_stats = OrderedDict(
            sorted(ext_idefs_stats.items(), key=lambda t: t[1],
                   reverse=True))
        res['detailed_stats'] = ordered_stats
        storage.store('extracted_stats.json', res)
        print(item['id'])
    (total, unrefed, external_idefs, ext_idefs_stats_in_item) = handle_statements(item['claims'])
    if unrefed == 0:
        res['fully_refed_items'] += 1
        continue
    res['total_total'] += total
    res['total_unref'] += unrefed
    res['good_items'] += 1
    res['total_ex_idefs'] += external_idefs
    for pid in ext_idefs_stats_in_item:
        ext_idefs_stats[pid] = ext_idefs_stats.get(pid, 0) + ext_idefs_stats_in_item[pid]
    if external_idefs != 0:
        res['potential_total'] += total
        res['potential_unref'] += unrefed
        res['good_items_with_ex_idef'] += 1
