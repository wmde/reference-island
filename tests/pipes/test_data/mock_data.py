IGNORED_REFERENCE_PROPERTY = "P143"
ALLOWED_EXT_ID = "P3029"
EXTERNAL_ID_VALUE = "tst1234"
NON_ALLOWED_EXT_ID = "P3028"
ITEM_ID = "Q23"
SKIPPED_PROPERTY = "P26"
NON_SKIPPED_PROPERTY = "P509"
IGNORED_CLASS = "Q987"
IGNORED_CLASS_INT_ID = 987
INSTANCE_OF_PROPERTY = "P31"
DATATYPE = "wikibase-item"

VALUE_BLOB = {
    "entity-type": "item",
    "numeric-id": 191789,
    "id": "Q191789"
}

IGNORED_CLASS_VALUE_BLOB = {
    "entity-type": "item",
    "numeric-id": IGNORED_CLASS_INT_ID,
    "id": IGNORED_CLASS
}

STATEMENT_BLOB = {
    "pid": NON_SKIPPED_PROPERTY,
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
        'referenceMetadata': {ALLOWED_EXT_ID: 'fooid'},
        'extractedData': ['foo', 'bar']
    }
}
mock = {
    "claim": {
        "with_ignored_references_only": {
            "mainsnak": {
                "property": NON_SKIPPED_PROPERTY,
                "datavalue": {
                    "value": VALUE_BLOB
                },
                "datatype": DATATYPE
            },
            "references": [
                {
                    "snaks": {IGNORED_REFERENCE_PROPERTY: "bar"}
                }
            ]
        },
        "with_references": {
            "mainsnak": {
                "property": NON_SKIPPED_PROPERTY
            },
            "references": [
                {
                    "snaks": {
                        "foo": "bar",
                        IGNORED_REFERENCE_PROPERTY: "bar"
                    }
                }
            ]
        },
        "with_any_external_id": {
            "mainsnak": {
                "property": NON_ALLOWED_EXT_ID,
                "datatype": "external-id"
            }
        },
        "with_allowed_external_id": {
            "mainsnak": {
                "datatype": "external-id",
                "property": ALLOWED_EXT_ID,
                "datavalue": {
                    "value": EXTERNAL_ID_VALUE
                }
            }
        },
        "with_any_unreferenced_property": {
            "mainsnak": {
                "property": NON_SKIPPED_PROPERTY,
                "datavalue": {
                    "value": VALUE_BLOB
                },
                "datatype": DATATYPE
            }
        },
        "with_ignored_class": {
            "mainsnak": {
                "property": INSTANCE_OF_PROPERTY,
                "datavalue": {
                    "value": IGNORED_CLASS_VALUE_BLOB
                },
                "datatype": DATATYPE
            }
        },
        "with_skipped_property": {
            "mainsnak": {
                "property": SKIPPED_PROPERTY
            }
        }
    }
}
