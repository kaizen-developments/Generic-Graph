from abc import ABC, abstractmethod
from typing import List, Tuple, Set
from collections.abc import MutableSet
from typing import TypeVar

import logging
#logging.basicConfig(level=logging.INFO)

class Edge(ABC):
    @abstractmethod
    def startNode(self):
        pass

    @abstractmethod
    def endNode(self):
        pass

    def elements(self):
        return {self.startNode(), self.endNode()}
    
    def __str__(self) -> str:
        return f"({self.startNode()}, {self.endNode()})"

class Graph(ABC):
    Edge = TypeVar('Edge', bound='Edge')
    @abstractmethod
    def getNodes(self) -> Set:
        pass

    @abstractmethod
    def getEdges(self) -> Set[Edge]:
        pass

    def neighboursOf(self, node) -> MutableSet:
        logging.info(f"Starting to search for the neighbours of {node}.")
        if node not in self.getNodes():
            logging.info(f"There are no neighbours of {node}.")
            return []
        else:
            neighbours = {edge.endNode() for edge in self.getEdges() if edge.startNode() == node}
            logging.info(f"The neighbours of {node} are {neighbours}.")
            return neighbours

    def addNode(self, node) -> None:
        """
        This function has a side effect. It modifies the state of the returned value of getNodes
        """
        self.getNodes().add(node)

    def removeNode(self, node) -> None:
        """
        This function has a side effect. It modifies the state of the returned value of getNodes
        """
        self.getNodes().discrad(node)

    def addEdge(self, edge) -> None:
        """
        This function has a side effect. It modifies the state of the returned value of getEdges
        """
        self.getEdges().add(edge)

    def __contains__(self, node) -> bool:
        return node in self.getNodes()

    def __str__(self) -> str:
        node_str = "Nodes:\n" + "\n".join(str(node) for node in self.getNodes())
        edge_str = "Edges:\n" + "\n".join(str(edge) for edge in self.getEdges())
        return node_str + "\n" + edge_str