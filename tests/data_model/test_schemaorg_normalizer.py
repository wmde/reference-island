import json

import pytest

from wikidatarefisland.data_access.offline_document_loader import OfflineDocumentLoader
from wikidatarefisland.data_model.schemaorg_normalizer import (
    SchemaOrgGraph, SchemaOrgNode, SchemaOrgNormalizer)


class MockSchemaOrgNode:
    def get_props(self, *args):
        return {"test": "mock"}


@pytest.fixture
def document_loader():
    import os
    script_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_path, 'mock_data', 'jsonldcontext.jsonld')) as f:
        schema_context = json.load(f)
    return OfflineDocumentLoader(schema_context)


class TestSchemaOrgNode:
    def test_get_prop(self):
        given = {
            "@id": "123",
            "http://schema.org/name": {
                "@value": "test"
            }
        }

        expected = "test"

        result = SchemaOrgNode(given, None).get_prop("http://schema.org/name")

        assert result == expected, "Should get simple value"

    def test_get_prop_list(self):
        given = {
            "@id": "123",
            "http://schema.org/additionalName": [
                {"@value": "test"},
                {"@value": "hello"}
            ]
        }

        expected = ["test", "hello"]

        result = SchemaOrgNode(given, None).get_prop("http://schema.org/additionalName")

        assert result == expected, "Should get list of values"

    def test_get_prop_id(self, monkeypatch, document_loader):
        def mock_hasNode(*args):
            return False

        monkeypatch.setattr(SchemaOrgGraph, "has_node", mock_hasNode)
        graph = SchemaOrgGraph([], document_loader)

        given = {
            "@id": "123",
            "http://schema.org/additionalName": [
                {"@value": "test"},
                {"@id": "fakeId"}
            ]
        }

        expected = ["test", "fakeId"]

        result = SchemaOrgNode(given, graph).get_prop("http://schema.org/additionalName")

        assert result == expected, "Should get id value if no node is found"

    def test_get_prop_node(self, monkeypatch, document_loader):
        def mock_has_node(*args):
            return True

        def mock_get_node(*args):
            return MockSchemaOrgNode()

        monkeypatch.setattr(SchemaOrgGraph, "has_node", mock_has_node)
        monkeypatch.setattr(SchemaOrgGraph, "get_node", mock_get_node)
        graph = SchemaOrgGraph([], document_loader)

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

        result = SchemaOrgNode(given, graph).get_prop("http://schema.org/additionalName")

        assert result == expected, "Should get nested nodes"

    def test_get_props(self):
        given = {
            "@id": "123",
            "http://schema.org/name": {"@value": "test"},
            "http://schema.org/additionalName": {"@value": "hello"}
        }

        expected = {
            "http://schema.org/name": "test",
            "http://schema.org/additionalName": "hello"
        }

        result = SchemaOrgNode(given, None).get_props()

        assert result == expected, "Should get properties dictionary"

    def test_has_props(self):
        given = {
            "@id": "123",
            "http://schema.org/name": {"@value": "test"}
        }

        result = SchemaOrgNode(given, None).has_props()

        assert result is True, "Should return true if has schema.org"

    def test_has_props_no_schemaorg(self):
        given = {
            "@id": "123",
            "http://ogp.me/#ns/name": {"@value": "test"}
        }

        result = SchemaOrgNode(given, None).has_props()

        assert result is False, "Should return false if doesn't have schema.org"

    def test_to_jsonld(self):
        given = {
            "@id": "123",
            "http://schema.org/name": {"@value": "test"}
        }

        result = SchemaOrgNode(given, None).to_jsonld()

        assert result == given, "Should return expanded json-ld format"

    def test_to_jsonld_type(self):
        given = {
            "@id": "123",
            "@type": "http://schema.org/Thing",
            "http://schema.org/name": {"@value": "test"}
        }

        result = SchemaOrgNode(given, None).to_jsonld()

        assert result == given, "Should include @type in json-ld format"


class TestSchemaOrgGraph:
    def test_get_node(self, monkeypatch, document_loader):
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

        result = SchemaOrgGraph(given, document_loader).get_node("http://example.com/123")

        expected = SchemaOrgNode(given[0], None)

        assert result == expected, "Should get a node by it's id"

    def test_has_node(self, document_loader):
        given = [
            {
                "@id": "http://example.com/123",
                "http://schema.org/name": [{"@value": "test"}]
            }
        ]

        result = SchemaOrgGraph(given, document_loader).has_node("http://example.com/123")

        assert result is True, "Should return true if node exists"

    def test_has_node_no_node(self, document_loader):
        given = [
            {
                "@id": "http://example.com/123",
                "http://schema.org/name": [{"@value": "test"}]
            }
        ]

        result = SchemaOrgGraph(given, document_loader).has_node("123")

        assert result is False, "Should return false if node doesn't exist"

    def test_get_nodes(self, document_loader):
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

        result = SchemaOrgGraph(given, document_loader).get_nodes()

        assert result == expected, "Should get the nodes' properties"

    def test_get_nodes_nested(self, document_loader):
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

        result = SchemaOrgGraph(given, document_loader).get_nodes()

        assert result == expected, "Should include nested nodes"

    def test_get_nodes_graph_child(self, document_loader):
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

        result = SchemaOrgGraph(given, document_loader).get_nodes()

        assert result == expected, "Should extract nested graphs"

    def test_to_jsonld(self, document_loader):
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

        result = SchemaOrgGraph(given, document_loader).to_jsonld()

        assert result == given, "Should return flattened expanded json-ld format"

    def test_to_jsonld_graph_child(self, document_loader):
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

        result = SchemaOrgGraph(given, document_loader).to_jsonld()

        assert result == expected, "Should extract graphs"

    def test_get_nodes_self_referring(self, document_loader):
        given = [{
            "@id": "_:b0",
            "http://schema.org/name": [
                {
                    "@id": "_:b0"
                }
            ]
        }]
        expected = {'http://schema.org/name': ["_:b0"]}
        result = SchemaOrgGraph(given, document_loader).get_nodes()

        assert result == [expected]

    def test_get_nodes_circular_referring(self, document_loader):
        given = [
            {
                "@id": "http://example.com/eltonId",
                "@type": "Person",
                "http://schema.org/name": {"@value": "Elton John"},
                "http://schema.org/additionalName": {"@id": "http://example.com/reginaldId"}
            },
            {
                "@id": "http://example.com/reginaldId",
                "@type": "Person",
                "http://schema.org/name": {"@value": "Reginald Dwight"},
                "http://schema.org/additionalName": {"@id": "http://example.com/eltonId"}
            }
        ]

        expected = [
            {
                "http://schema.org/additionalName": [
                    {
                        "http://schema.org/name": ["Reginald Dwight"],
                        "http://schema.org/additionalName": ["http://example.com/eltonId"]
                    }
                ],
                "http://schema.org/name": ["Elton John"]
            },
            {
                "http://schema.org/additionalName": [
                    {
                        "http://schema.org/name": ["Elton John"],
                        "http://schema.org/additionalName": ["http://example.com/reginaldId"]
                    }
                ],
                "http://schema.org/name": ["Reginald Dwight"]
            }
        ]

        result = SchemaOrgGraph(given, document_loader).get_nodes()
        assert result == expected


@pytest.fixture
def normalizer(document_loader):
    return SchemaOrgNormalizer(document_loader.get_loader)


class TestSchemaOrgNormalizer:
    def test_normamaize_form_extruct_not_schema_org(self, normalizer):
        given = {
            'some_key': [
                {
                    "@context": "http://schema-cat-not-real-hat.org",
                    "@id": "http://example.com/123",
                    "name": [{"@value": "test"}],
                    "additionalName": [{
                        "@id": "http://example.com/124"
                    }]
                },
                {
                    "@context": "http://schema-cat-not-real-hat.org",
                    "@id": "http://example.com/124",
                    "firstName": [{"@value": "Lola"}],
                    "lastName": [{"@value": "Showgirl"}]
                }
            ]
        }

        expected = []

        result = normalizer.normalize_from_extruct(given)

        assert result == expected, "Should normalize nested compacted data"

    def test_normalize_from_extruct(self, normalizer):
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

        result = normalizer.normalize_from_extruct(given)

        assert result == expected, "Should normalize nested compacted data"

    def test_normalize_from_extruct_multiple(self, normalizer):
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

        result = normalizer.normalize_from_extruct(given)

        assert result == expected, "Should normalize from multiple sources"
