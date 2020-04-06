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

