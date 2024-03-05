import unittest
from typing import Type, TypeVar

import sys
import os

import logging

def import_the_folder_n_steps_above(n: int) -> None:
    current_folder = os.path.abspath(os.path.dirname(__file__))
    steps = [".."] * n
    target_folder = os.path.abspath(os.path.join(current_folder, *steps))
    sys.path.insert(0, target_folder)
import_the_folder_n_steps_above(n=1)

from abstractModule_graph import Graph, Edge
from Implementation.implementationClasses import YoutubeVideoGraph, Link, YoutubeVideoNode, DebugMessage
from Classes.classModule_debugMessage import DebugMessage

G = TypeVar('G', bound=Graph)
E = TypeVar('E', bound=Edge)
N = TypeVar('N', bound=Graph)

#TODO: For testing purposes, ensure that node has a generator allowing for creating arbitrary nodes during tests!
#TODO: Ensure
class TestGraph(unittest.TestCase):
    graph_class: Type[G]
    edge_class: Type[E]

    @classmethod
    def setUpClass(cls):
        #TODO: Document, that _nodeGenerators succesful implementation ensures test cases for the class.
        cls.nodeGenerator = cls.get_node_class()._nodeGenerator()

    @classmethod
    def get_graph_class(cls) -> Type[G]:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    @classmethod
    def get_edge_class(cls) -> Type[E]:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_node_class(cls) -> Type[N]:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def test_nodeGenerator_returns_a_node(cls):
        node = next(cls.nodeGenerator)
        logging.debug(DebugMessage.valueOfVariableInContext(className="TestGraph", methodName="test_nodeGenerator_returns_a_node", linenumber=47, variableName="node", obj=node))
        cls.assertIsInstance(node, cls.get_node_class())

    def test_edge_class_has_default_constructor(cls):
        edge = cls.get_edge_class()()
        cls.assertIsInstance(edge, cls.get_edge_class())

    def test_nodes_are_a_set_like_object(cls):
        graph = cls.graph_class(set(), set())
        node = cls.get_node_class().nextNode()
        graph.getNodes().add(node)

    def test_remove_node(cls):
        graph = cls.graph_class(set(), set())
        node = cls.get_node_class().nextNode()
        graph.getNodes().add(node)
        graph.getNodes().remove(node)
        print(node)
        cls.assertNotIn(node, graph.getNodes())

    def test_add_edge(cls):
        graph = cls.graph_class(set(), set())
        edge = cls.get_edge_class()
        cls.assertNotIn(edge, graph.getEdges())

        graph.getEdges().add(edge)
        cls.assertIn(edge, graph.getEdges())
    
    def test_adding_edges_adds_nodes(cls):
        graph = cls.graph_class(set(), set())
        edge = cls.get_edge_class()()
        graph.getEdges().add(edge)
        cls.assertIn(edge.startNode(), graph.getNodes())
        cls.assertIn(edge.endNode(), graph.getNodes())

# To use this test class, you would subclass it and implement the `get_graph_class` method.

class TestResourceGraph(TestGraph):
    @classmethod
    def get_graph_class(cls):
        return YoutubeVideoGraph

    @classmethod
    def get_edge_class(cls):
        return Link

    @classmethod
    def get_node_class(cls):
        return YoutubeVideoNode

if __name__ == '__main__':
    suite = unittest.TestSuite()

    # Get all subclasses of TestGraphBase
    subclasses = TestGraph.__subclasses__()

    for subclass in subclasses:
        # Add the test cases from the subclass to the test suite
        suite.addTest(unittest.makeSuite(subclass))

    # Run the test suite
    unittest.TextTestRunner().run(suite)