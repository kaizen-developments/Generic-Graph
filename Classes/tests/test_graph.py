import unittest
from typing import Type, TypeVar

import sys
import os

def import_the_folder_n_steps_above(n: int) -> None:
    current_folder = os.path.abspath(os.path.dirname(__file__))
    steps = [".."] * n
    target_folder = os.path.abspath(os.path.join(current_folder, *steps))
    sys.path.insert(0, target_folder)
import_the_folder_n_steps_above(n=1)

from abstractModule_graph import Graph, Edge
from Implementation.implementationClasses import ResourceGraph, Link

G = TypeVar('G', bound=Graph)
E = TypeVar('E', bound=Edge)
N = TypeVar('N', bound=Graph)

class TestGraph(unittest.TestCase):
    graph_class: Type[G]
    edge_class: Type[E]

    @classmethod
    def setUpClass(cls):
        cls.graph_class = cls.get_graph_class()
        cls.edge_class = cls.get_edge_class()

    @classmethod
    def get_graph_class(cls) -> Type[G]:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    @classmethod
    def get_edge_class(cls) -> Type[E]:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_node_class(cls) -> Type[N]:


    def test_edge_class_has_default_constructor(self):
        edge = self.get_edge_class()()
        self.assertIsInstance(edge, self.get_edge_class())

    def test_remove_node(self):
        graph = self.graph_class(set(), set())
        node = {"id": "test_node"}
        graph.getNodes().add(node)
        graph.getNodes().remove(node)
        self.assertNotIn(node, graph.getNodes())

    def test_add_edge(self):
        graph = self.graph_class(set(), set())
        edge = self.get_edge_class()
        self.assertNotIn(edge, graph.getEdges())

        graph.getEdges().add(edge)
        self.assertIn(edge, graph.getEdges())
    
    def test_adding_edges_adds_nodes(self):
        graph = self.graph_class(set(), set())
        edge = self.get_edge_class()()
        graph.getEdges().add(edge)
        self.assertIn(edge.startNode(), graph.getNodes())
        self.assertIn(edge.endNode(), graph.getNodes())

# To use this test class, you would subclass it and implement the `get_graph_class` method.

class TestResourceGraph(TestGraph):
    @classmethod
    def get_graph_class(cls):
        return ResourceGraph

    @classmethod
    def get_edge_class(cls):
        return Link

if __name__ == '__main__':
    suite = unittest.TestSuite()

    # Get all subclasses of TestGraphBase
    subclasses = TestGraph.__subclasses__()

    for subclass in subclasses:
        # Add the test cases from the subclass to the test suite
        suite.addTest(unittest.makeSuite(subclass))

    # Run the test suite
    unittest.TextTestRunner().run(suite)