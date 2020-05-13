WHITELISTED_EXT_ID = "P3029"
EXTERNAL_ID_VALUE = "tst1234"
NON_WHITELISTED_EXT_ID = "P3028"
ITEM_ID = "Q23"
BLACKLISTED_PROPERTY = "P26"
NON_BLACKLISTED_PROPERTY = "P509"
DATATYPE = "wikibase-item"

VALUE_BLOB = {
    "entity-type": "item",
    "numeric-id": 191789,
    "id": "Q191789"
}

STATEMENT_BLOB = {
    "pid": NON_BLACKLISTED_PROPERTY,
    "datatype": DATATYPE,
    "value": VALUE_BLOB
}

RESOURCE_BLOB = {
    "url": f"http://example.com/{EXTERNAL_ID_VALUE}",
    "referenceMetadata": None
}

ITEM = {
    "pageid": 136,
    "ns": 0,
    "title": ITEM_ID,
    "lastrevid": 1150873645,
    "modified": "2020-04-05T21:23:54Z",
    "type": "item",
    "id": ITEM_ID,
    "labels": {},
    "descriptions": {},
    "aliases": {},
    "claims": {},
    "sitelinks": {}
}

LINE = {
    "itemId": ITEM_ID,
    "statements": [],
    "resourceUrls": []
}
REFERENCE_LINE = {
    'statement': {},
    'itemId': ITEM_ID,
    'reference': {'referenceMetadata': {},
                  'extractedData': []}}

EXAMPLE_LINE = {
    **REFERENCE_LINE,
    'statement': STATEMENT_BLOB,
    'reference': {
        'referenceMetadata': {WHITELISTED_EXT_ID: 'fooid'},
        'extractedData': ['foo', 'bar']
    }
}
mock = {
    "claim": {
        "with_references": {
            "mainsnak": {
                "property": NON_BLACKLISTED_PROPERTY
            },
            "references": []
        },
        "with_any_external_id": {
            "mainsnak": {
                "property": NON_WHITELISTED_EXT_ID,
                "datatype": "external-id"
            }
        },
        "with_whitelisted_external_id": {
            "mainsnak": {
                "datatype": "external-id",
                "property": WHITELISTED_EXT_ID,
                "datavalue": {
                    "value": EXTERNAL_ID_VALUE
                }
            }
        },
        "with_any_unreferenced_property": {
            "mainsnak": {
                "property": NON_BLACKLISTED_PROPERTY,
                "datavalue": {
                    "value": VALUE_BLOB
                },
                "datatype": DATATYPE
            }
        },
        "with_blacklisted_property": {
            "mainsnak": {
                "property": BLACKLISTED_PROPERTY
            }
        }
    }
}
