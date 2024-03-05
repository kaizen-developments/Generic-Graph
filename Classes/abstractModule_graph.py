from abc import ABC, abstractmethod
from typing import List, Tuple, Set
from collections.abc import MutableSet
from typing import TypeVar, Generic

import logging
logging.basicConfig(level=logging.DEBUG)

import sys
import os

def import_the_folder_n_steps_above(n: int) -> None:
    current_folder = os.path.abspath(os.path.dirname(__file__))
    steps = [".."] * n
    target_folder = os.path.abspath(os.path.join(current_folder, *steps))
    sys.path.insert(0, target_folder)
import_the_folder_n_steps_above(n=1)

from Classes.classModule_debugMessage import DebugMessage

class Node(type):
    def nextNode(self) -> 'Node':
        raise NotImplementedError("This method should be implemented by subclasses.")

N = TypeVar('N', bound=Node)
class Edge(ABC, Generic[N]):
    @abstractmethod
    def startNode(self) -> N:
        pass

    @abstractmethod
    def endNode(self) -> N:
        pass

    def elements(self):
        return {self.startNode(), self.endNode()}
    
    def __str__(self) -> str:
        return f"({self.startNode()}, {self.endNode()})"

class Graph(ABC):
    Edge = TypeVar('Edge', bound='Edge')
    @abstractmethod
    def getNodes(self) -> Set[Node]:
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abstractmethod
    def getEdges(self) -> Set[Edge]:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def neighboursOf(self, node) -> MutableSet:
        logging.info(f"Starting to search for the neighbours of {node}.")
        if node not in self.getNodes():
            logging.info(f"There are no neighbours of {node}.")
            return []
        else:
            neighbours = {edge.endNode() for edge in self.getEdges() if edge.startNode() == node}
            logging.info(f"The neighbours of {node} are {neighbours}.")
            return neighbours

    #TODO: Ensure, that addNode and removeNode's behaviour ensures that the graph's nodes will have the properties of a set!
    def addNode(self, node) -> None:
        """
        This function has a side effect. It modifies the state of the returned value of getNodes
        """
        if node not in self.getNodes():
            logging.debug(DebugMessage.usingMethodWithParameters(className="Graph", methodName="addNode", linenumber=53, nameOfMethodCalled="self.getNodes().add", parameters=[node]))
            self.getNodes().add(node)
        else:
            return

    def removeNode(self, node) -> None:
        """
        This function has a side effect. It modifies the state of the returned value of getNodes
        """
        self.getNodes().discrad(node)

    #TODO: Ensure, that an edge only gets added, if the edge does not exist in the edges for any input! (Perhaps use a contraction to two boolean values and assume, that according to these boolean values the program will show behaviour which is well determined!)
    def addEdge(self, edge) -> None:
        """
        This function has a side effect. It modifies the state of the returned value of getEdges
        """
        if edge not in self.getEdges():
            self.getEdges().add(edge)
            self.getNodes().add(edge.startNode())
            self.getNodes().add(edge.endNode())
        else:
            return

    def __contains__(self, node) -> bool:
        return node in self.getNodes()

    def __str__(self) -> str:
        node_str = "Nodes:\n" + "\n".join(str(node) for node in self.getNodes())
        edge_str = "Edges:\n" + "\n".join(str(edge) for edge in self.getEdges())
        return node_str + "\n" + edge_str