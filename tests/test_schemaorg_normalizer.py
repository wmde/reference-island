from wikidatarefisland.schemaorg_normalizer import SchemaOrgNormalizer as normalizer


def test_filterProps():
    assert normalizer.filterProps('schema.org'), 'Returns true when contains `schema.org`'
    assert not normalizer.filterProps('example.com'), {'Returns false when doesn\'t contain '
                                                       '`schema.org`'}


def test_filterScraped():
    assert normalizer.filterScraped({'schema.org': 'test'}), {'Returns true when scrape has '
                                                              '`schema.org` keys'}
    assert not normalizer.filterScraped({'example.com': 'test'}), {'Returns false when scrape '
                                                                   'doesn\'t have `schema.org '
                                                                   'keys`'}


def test_extractGraphs():
    assert normalizer.extractGraphs([], {"@graph": ["test"]}) == ["test"], {'Extracts values '
                                                                           'from graph property'}


def test_normalizeExpanded_flattens():
    given = [{
        "@type": ["http://schema.org/Thing"],
        "http://schema.org/name": [{"@value": "Test"}],
        "http://schema.org/sameAs": [{
            "@type": ["http://schema.org/Thing"],
            "http://schema.org/name": [{"@value": "Example Test"}]
        }]
    }]

    expected = [
        {
            "@id": "_:b0",
            "@type": ["http://schema.org/Thing"],
            "http://schema.org/name": [{"@value": "Test"}],
            "http://schema.org/sameAs": [{"@id": "_:b1"}]
        },
        {
            "@id": "_:b1",
            "@type": ["http://schema.org/Thing"],
            "http://schema.org/name": [{"@value": "Example Test"}]
        }
    ]

    assert normalizer.normalizeExpanded(given) == expected, 'Flattens nested objects'


def test_normalizeExpanded_extracts():
    given = [
        {
            "@graph": [
                {
                    "@id": "_:b111",
                    "@type": ["http://schema.org/Thing"],
                    "http://schema.org/name": [{"@value": "Test"}]
                },
                {
                    "@id": "_:b112",
                    "@type": ["http://schema.org/Thing"],
                    "http://schema.org/isPartOf": [{"@id": "_:b111"}],
                    "http://schema.org/name": [{"@value": "Example Test"}]
                }
            ]
        }
    ]

    expected = [
        {
            "@id": "_:b0",
            "@type": ["http://schema.org/Thing"],
            "http://schema.org/name": [{"@value": "Test"}]
        },
        {
            "@id": "_:b1",
            "@type": ["http://schema.org/Thing"],
            "http://schema.org/isPartOf": [{"@id": "_:b0"}],
            "http://schema.org/name": [{"@value": "Example Test"}]
        }
    ]

    assert normalizer.normalizeExpanded(given) == expected, 'Extracts top-level @graphs'
    #assert False
