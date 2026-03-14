import networkx as nx


class CayleyGraph:

    def __init__(self, generators):

        self.generators = generators
        self.graph = nx.Graph()

    def build(self, nodes):

        for node in nodes:
            self.graph.add_node(node)

        for node in nodes:

            for name, op in self.generators.items():

                target = op(node)

                self.graph.add_edge(node, target, label=name)

        return self.graph
