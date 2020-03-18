import gzip
import sys
import json
from collections import OrderedDict

black_listed_items = [
    'Q86995636',  # scientific articles
    'Q318',  # galaxy
    'Q4167410',  # disambig
    'Q4167836',  # category
    'Q11266439',  # template
    'Q15184295',  # Module
    'Q13442814',  # Journal article
    'Q13406463',  # Wikimedia list
]
classifying_properties = [
    'P31',
    'P279',
    'P373',  # Commons category
    'P910',  # Topic's main category
]

with open('../data/external_idefs.json', 'r') as f:
    external_identifiers = json.loads(f.read())

with open('../data/whitelisted_ext_idefs.json', 'r') as f:
   whitelisted_ext_idefs = json.loads(f.read())


def check_data(line):
    try:
        item = json.loads(line.replace('\n', '')[:-1])
    except:
        # It's not using json-lines, it's a big json thus this mess.
        return
    if item['type'] != 'item':
        return
    return item


def remove_blacklisted_items(p31):
    if not p31:
        return False
    for claim in p31:
        try:
            pid = claim['mainsnak']['datavalue']['value'].get('id')
        except:
            continue
        if pid in black_listed_items:
            return True
    return False


def handle_statements(claims):
    unrefed_statements = 0
    statements_that_should_have_ref = 0
    ex_idefs = 0
    ext_idefs_stats = {}
    for pid in claims:
        if pid in classifying_properties:
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


# /mnt/data/xmldatadumps/public/wikidatawiki/entities/latest-all.json.gz
with gzip.open(sys.argv[1], 'rt') as f:
    total_statements_that_should_have_ref = 0
    total_unref_statements_that_should_have_ref = 0
    total_statements_that_should_have_ref_and_can_have = 0
    total_unref_statements_that_should_have_ref_and_can_have = 0
    total_good_items = 0
    total_good_items_with_external_identifers = 0
    total_ex_idefs = 0
    fully_refed_items = 0
    ext_idefs_stats = {}
    for line in f:
        item = check_data(line)
        if item is None:
            continue
        if remove_blacklisted_items(item['claims'].get('P31')):
            continue
        if int(item['id'][1:]) % 1000 == 0:
            with open('../data/final_res.json', 'w') as f:
                ordered_stats = OrderedDict(
                    sorted(ext_idefs_stats.items(), key=lambda t: t[1],
                           reverse=True)
                )
                res = {
                    'total_total': total_statements_that_should_have_ref,
                    'total_unref': total_unref_statements_that_should_have_ref,
                    'potential_total': total_statements_that_should_have_ref_and_can_have,
                    'potential_unref': total_unref_statements_that_should_have_ref_and_can_have,
                    'good_items': total_good_items,
                    'good_items_with_ex_idef': total_good_items_with_external_identifers,
                    'done_up_to': item['id'],
                    'total_ex_idefs': total_ex_idefs,
                    'fully_refed_items': fully_refed_items,
                    'detailed_stats': ordered_stats,
                }
                f.write(json.dumps(res))
            print(item['id'])
        (total, unrefed, external_idefs, ext_idefs_stats_in_item) = handle_statements(item['claims'])
        if unrefed == 0:
            fully_refed_items += 1
            continue
        total_statements_that_should_have_ref += total
        total_unref_statements_that_should_have_ref += unrefed
        total_good_items += 1
        total_ex_idefs += external_idefs
        for pid in ext_idefs_stats_in_item:
            ext_idefs_stats[pid] = ext_idefs_stats.get(pid, 0) + ext_idefs_stats_in_item[pid]
        if external_idefs != 0:
            total_statements_that_should_have_ref_and_can_have += total
            total_unref_statements_that_should_have_ref_and_can_have += unrefed
            total_good_items_with_external_identifers += 1
