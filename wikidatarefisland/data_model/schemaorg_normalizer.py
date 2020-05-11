from functools import reduce

from pyld import jsonld


class SchemaOrgNode:
    def __init__(self, data, graph):
        self._graph = graph
        self.id = data["@id"]
        self._type = data["@type"] if "@type" in data else None
        self._props = dict(filter(lambda kvPair: "schema.org" in kvPair[0], data.items()))

    def _get_value(self, leaf):
        if "@id" in leaf:
            id = leaf["@id"]
            return self._graph.get_node(id).get_props() if self._graph.has_node(id) else id

        return leaf["@value"]

    def get_prop(self, propName):
        leaf = self._props[propName]

        if isinstance(leaf, list):
            return list(map(lambda item: self._get_value(item), leaf))

        return self._get_value(leaf)

    def get_props(self):
        return dict(map(lambda kvPair: (kvPair[0].replace('https://', 'http://'),
                                        self.get_prop(kvPair[0])), self._props.items()))

    def has_props(self):
        return len(self._props) > 0

    def to_jsonld(self):
        jsonld_format = {
            "@id": self.id,
            **self._props
        }

        if self._type:
            jsonld_format["@type"] = self._type

        return jsonld_format


class SchemaOrgGraph:
    def __init__(self, data):
        flattened = jsonld.flatten(data)

        self._nodes = reduce(self._reduce_nodes, flattened, {})

    def _reduce_nodes(self, nodes_dict, raw_node):
        if '@graph' in raw_node:
            return {
                **nodes_dict,
                **reduce(self._reduce_nodes, raw_node["@graph"], {})
            }

        node = SchemaOrgNode(raw_node, self)

        if not node.has_props():
            return nodes_dict

        return {
            **nodes_dict,
            node.id: node
        }

    def get_node(self, id):
        return self._nodes[id]

    def has_node(self, id):
        return id in self._nodes

    def get_nodes(self):
        return list(map(lambda node: node.get_props(), self._nodes.values()))

    def to_jsonld(self):
        return list(map(lambda node: node.to_jsonld(), self._nodes.values()))


class SchemaOrgNormalizer:

    @staticmethod
    def normalize_from_extruct(data):
        scrapedList = reduce(lambda acc, arg: acc + arg, data.values())
        graph = SchemaOrgGraph(scrapedList)

        return graph.get_nodes()
