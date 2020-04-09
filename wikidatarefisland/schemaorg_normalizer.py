from functools import reduce
from pyld import jsonld


class SchemaOrgNode:
    def __init__(self, data, graph):
        self._graph = graph
        self.id = data["@id"]
        self._type = data["@type"] if "@type" in data else None
        self._props = dict(filter(lambda kvPair: "schema.org" in kvPair[0], data.items()))

    def _getValue(self, leaf):
        if "@id" in leaf:
            id = leaf["@id"]
            return self._graph.getNode(id).getProps() if self._graph.hasNode(id) else id

        return leaf["@value"]

    def getProp(self, propName):
        leaf = self._props[propName]

        if isinstance(leaf, list):
            return list(map(lambda item: self._getValue(item), leaf))

        return self._getValue(leaf)

    def getProps(self):
        return dict(map(lambda kvPair: (kvPair[0], self.getProp(kvPair[0])), self._props.items()))

    def hasProps(self):
        return len(self._props) > 0

    def toJsonLd(self):
        jsonLdFormat = {
            "@id": self.id,
            **self._props
        }

        if self._type:
            jsonLdFormat["@type"] = self._type

        return jsonLdFormat


class SchemaOrgGraph:
    def __init__(self, data):
        flattened = jsonld.flatten(data)

        self._nodes = reduce(self._reduceNodes, flattened, {})

    def _reduceNodes(self, nodes_dict, raw_node):
        if '@graph' in raw_node:
            return {
                **nodes_dict,
                **reduce(self._reduceNodes, raw_node["@graph"], {})
            }

        node = SchemaOrgNode(raw_node, self)

        if not node.hasProps():
            return nodes_dict

        return {
            **nodes_dict,
            node.id: node
        }

    def getNode(self, id):
        return self._nodes[id]

    def hasNode(self, id):
        return id in self._nodes

    def getNodes(self):
        return list(map(lambda node: node.getProps(), self._nodes.values()))

    def toJsonLd(self):
        return list(map(lambda node: node.toJsonLd(), self._nodes.values()))


class SchemaOrgNormalizer:

    @staticmethod
    def normalizeFromExtruct(data):
        scrapedList = reduce(lambda acc, arg: acc + arg, data.values())
        graph = SchemaOrgGraph(scrapedList)

        return graph.getNodes()
