from wikidatarefisland.data_model.schemaorg_normalizer import (
    SchemaOrgNormalizer,
    SchemaOrgGraph,
    SchemaOrgNode
)


class MockSchemaOrgNode:
    def getProps(self):
        return {"test": "mock"}


class TestSchemaOrgNode:
    def test_getProp(self):
        given = {
            "@id": "123",
            "http://schema.org/name": {
                "@value": "test"
            }
        }

        expected = "test"

        result = SchemaOrgNode(given, None).getProp("http://schema.org/name")

        assert result == expected, "Should get simple value"

    def test_getProp_list(self):
        given = {
            "@id": "123",
            "http://schema.org/additionalName": [
                {"@value": "test"},
                {"@value": "hello"}
            ]
        }

        expected = ["test", "hello"]

        result = SchemaOrgNode(given, None).getProp("http://schema.org/additionalName")

        assert result == expected, "Should get list of values"

    def test_getProp_id(self, monkeypatch):
        def mock_hasNode(*args):
            return False

        monkeypatch.setattr(SchemaOrgGraph, "hasNode", mock_hasNode)
        graph = SchemaOrgGraph([])

        given = {
            "@id": "123",
            "http://schema.org/additionalName": [
                {"@value": "test"},
                {"@id": "fakeId"}
            ]
        }

        expected = ["test", "fakeId"]

        result = SchemaOrgNode(given, graph).getProp("http://schema.org/additionalName")

        assert result == expected, "Should get id value if no node is found"

    def test_getProp_node(self, monkeypatch):
        def mock_hasNode(*args):
            return True

        def mock_getNode(*args):
            return MockSchemaOrgNode()

        monkeypatch.setattr(SchemaOrgGraph, "hasNode", mock_hasNode)
        monkeypatch.setattr(SchemaOrgGraph, "getNode", mock_getNode)
        graph = SchemaOrgGraph([])

        given = {
            "@id": "http://example.com/123",
            "http://schema.org/additionalName": [
                {"@value": "test"},
                {"@id": "124"}
            ]
        }

        expected = [
            "test",
            {
              "test":  "mock"
            }
        ]

        result = SchemaOrgNode(given, graph).getProp("http://schema.org/additionalName")

        assert result == expected, "Should get nested nodes"

    def test_getProps(self):
        given = {
            "@id": "123",
            "http://schema.org/name": {"@value": "test"},
            "http://schema.org/additionalName": {"@value": "hello"}
        }

        expected = {
            "http://schema.org/name": "test",
            "http://schema.org/additionalName": "hello"
        }

        result = SchemaOrgNode(given, None).getProps()

        assert result == expected, "Should get properties dictionary"

    def test_hasProps(self):
        given = {
            "@id": "123",
            "http://schema.org/name": {"@value": "test"}
        }

        result = SchemaOrgNode(given, None).hasProps()

        assert result is True, "Should return true if has schema.org"

    def test_hasProps_noSchemaOrg(self):
        given = {
            "@id": "123",
            "http://ogp.me/#ns/name": {"@value": "test"}
        }

        result = SchemaOrgNode(given, None).hasProps()

        assert result is False, "Should return false if doesn't have schema.org"

    def test_toJsonLd(self):
        given = {
            "@id": "123",
            "http://schema.org/name": {"@value": "test"}
        }

        result = SchemaOrgNode(given, None).toJsonLd()

        assert result == given, "Should return expanded json-ld format"

    def test_toJsonLd_type(self):
        given = {
            "@id": "123",
            "@type": "http://schema.org/Thing",
            "http://schema.org/name": {"@value": "test"}
        }

        result = SchemaOrgNode(given, None).toJsonLd()

        assert result == given, "Should include @type in json-ld format"


class TestSchemaOrgGraph:
    def test_getNode(self, monkeypatch):
        def mock_eq(self, other):
            if isinstance(self, other.__class__):
                return self.id == other.id and self._props == other._props
            return False

        monkeypatch.setattr(SchemaOrgNode, "__eq__", mock_eq)

        given = [
            {
                "@id": "http://example.com/123",
                "http://schema.org/name": [{"@value": "test"}]
            }
        ]

        result = SchemaOrgGraph(given).getNode("http://example.com/123")

        expected = SchemaOrgNode(given[0], None)

        assert result == expected, "Should get a node by it's id"

    def test_hasNode(self):
        given = [
            {
                "@id": "http://example.com/123",
                "http://schema.org/name": [{"@value": "test"}]
            }
        ]

        result = SchemaOrgGraph(given).hasNode("http://example.com/123")

        assert result is True, "Should return true if node exists"

    def test_hasNode_noNode(self):
        given = [
            {
                "@id": "http://example.com/123",
                "http://schema.org/name": [{"@value": "test"}]
            }
        ]

        result = SchemaOrgGraph(given).hasNode("123")

        assert result is False, "Should return false if node doesn't exist"

    def test_getNodes(self):
        given = [
            {
                "@id": "http://example.com/123",
                "http://schema.org/name": [{"@value": "test"}]
            }
        ]

        expected = [
            {
                "http://schema.org/name": ["test"]
            }
        ]

        result = SchemaOrgGraph(given).getNodes()

        assert result == expected, "Should get the nodes' properties"

    def test_getNodes_nested(self):
        given = [
            {
                "@id": "http://example.com/123",
                "http://schema.org/name": [{"@value": "test"}],
                "http://schema.org/additionalName": [{
                    "@id": "http://example.com/124"
                }]
            },
            {
                "@id": "http://example.com/124",
                "http://schema.org/firstName": [{"@value": "Lola"}],
                "http://schema.org/lastName": [{"@value": "Showgirl"}]
            }
        ]

        expected = [
            {
                "http://schema.org/name": ["test"],
                "http://schema.org/additionalName": [{
                    "http://schema.org/firstName": ["Lola"],
                    "http://schema.org/lastName": ["Showgirl"]
                }]
            },
            {
                "http://schema.org/firstName": ["Lola"],
                "http://schema.org/lastName": ["Showgirl"]
            }
        ]

        result = SchemaOrgGraph(given).getNodes()

        assert result == expected, "Should include nested nodes"

    def test_get_nodes_graph_child(self):
        given = [
            {
                "@graph": [
                    {
                        "@id": "http://example.com/124",
                        "http://schema.org/firstName": [{"@value": "Lola"}],
                        "http://schema.org/lastName": [{"@value": "Showgirl"}]
                    }
                ]
            }
        ]

        expected = [
            {
                "http://schema.org/firstName": ["Lola"],
                "http://schema.org/lastName": ["Showgirl"]
            }
        ]

        result = SchemaOrgGraph(given).getNodes()

        assert result == expected, "Should extract nested graphs"

    def test_toJsonLd(self):
        given = [
            {
                "@id": "http://example.com/123",
                "http://schema.org/name": [{"@value": "test"}],
                "http://schema.org/additionalName": [{
                    "@id": "http://example.com/124"
                }]
            },
            {
                "@id": "http://example.com/124",
                "http://schema.org/firstName": [{"@value": "Lola"}],
                "http://schema.org/lastName": [{"@value": "Showgirl"}]
            }
        ]

        result = SchemaOrgGraph(given).toJsonLd()

        assert result == given, "Should return flattened expanded json-ld format"

    def test_to_jsonld_graph_child(self):
        given = [
            {   
                "@graph": [
                    {
                        "@id": "http://example.com/124",
                        "http://schema.org/firstName": [{"@value": "Lola"}],
                        "http://schema.org/lastName": [{"@value": "Showgirl"}]
                    }
                ]
            }
        ]

        expected = [
            {
                "@id": "http://example.com/124",
                "http://schema.org/firstName": [{"@value": "Lola"}],
                "http://schema.org/lastName": [{"@value": "Showgirl"}]
            }
        ]

        result = SchemaOrgGraph(given).toJsonLd()

        assert result == expected, "Should extract graphs"


class TestSchemaOrgNormalizer:
    def test_normalizeFromExtruct(self):
        given = {
            'some_key': [
                {
                    "@context": "http://schema.org",
                    "@id": "http://example.com/123",
                    "name": [{"@value": "test"}],
                    "additionalName": [{
                        "@id": "http://example.com/124"
                    }]
                },
                {
                    "@context": "http://schema.org",
                    "@id": "http://example.com/124",
                    "firstName": [{"@value": "Lola"}],
                    "lastName": [{"@value": "Showgirl"}]
                }
            ]
        }

        expected = [
            {
                "http://schema.org/name": ["test"],
                "http://schema.org/additionalName": [{
                    "http://schema.org/firstName": ["Lola"],
                    "http://schema.org/lastName": ["Showgirl"]
                }]
            },
            {
                "http://schema.org/firstName": ["Lola"],
                "http://schema.org/lastName": ["Showgirl"]
            }
        ]

        result = SchemaOrgNormalizer.normalizeFromExtruct(given)

        assert result == expected, "Should normalize nested compacted data"

    def test_normalizeFromExtruct_multiple(self):
        given = {
            'some_key': [
                {
                    "@context": "http://schema.org",
                    "@id": "http://example.com/123",
                    "name": [{"@value": "test"}],
                    "additionalName": [{
                        "@id": "http://example.com/124"
                    }]
                },
                {
                    "@context": "http://schema.org",
                    "@id": "http://example.com/124",
                    "firstName": [{"@value": "Lola"}],
                    "lastName": [{"@value": "Showgirl"}]
                }
            ],
            'some_other_key': [
                {
                    "@type": "http://schema.org/Thing",
                    "http://schema.org/name": "Lovely Test"
                }
            ]
        }

        expected = [
            {
                "http://schema.org/name": ["Lovely Test"]
            },
            {
                "http://schema.org/name": ["test"],
                "http://schema.org/additionalName": [{
                    "http://schema.org/firstName": ["Lola"],
                    "http://schema.org/lastName": ["Showgirl"]
                }]
            },
            {
                "http://schema.org/firstName": ["Lola"],
                "http://schema.org/lastName": ["Showgirl"]
            }
        ]

        result = SchemaOrgNormalizer.normalizeFromExtruct(given)

        assert result == expected, "Should normalize from multiple sources"
