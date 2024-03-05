from googleapiclient.discovery import build, Resource
from typing import List, Set
import networkx as nx
import matplotlib.pyplot as plt

import sys
import os

import pickle

import logging 

import inspect

logging.basicConfig(level=logging.DEBUG)

def import_the_folder_n_steps_above(n: int) -> None:
    current_folder = os.path.abspath(os.path.dirname(__file__))
    steps = [".."] * n
    target_folder = os.path.abspath(os.path.join(current_folder, *steps))
    sys.path.insert(0, target_folder)
import_the_folder_n_steps_above(n=1)
import_the_folder_n_steps_above(n=2)

from Implementation.implementationCallables import get_youtube_API_key, YoutubeVideo

from abstractModule_graph import Edge, Graph
from types import MappingProxyType
import re

from Classes.classModule_debugMessage import DebugMessage

class YoutubeVideoNode(YoutubeVideo):
    @classmethod
    def _increment_id_key(resource: 'YoutubeVideoNode') -> None:
        pattern = r'___index___\d+$'
        match = re.search(pattern, resource['id'])
        resource_had_been_incremented:bool = bool(match)
        if resource_had_been_incremented:
            pattern = r'__index__(\d+)'
            index = int(match.group(1))
            index += 1
            resource['id'] = re.sub(pattern=pattern, repl=f'__index__{index}', string=resource['id'])
        else:
            resource['id'] = resource['id'] + "__index__0"

    @classmethod
    def _nodeGenerator(cls) -> 'YoutubeVideoNode':
        pickledObjectPath = os.path.join(os.getcwd(), "Classes", "Implementation", "arbitraryResource.pickle")
        with open(pickledObjectPath, 'rb') as f:
            resource:Resource = pickle.load(f)
            logging.debug(DebugMessage.valueOfVariableInContext(className="ResourceNode", methodName="_nodeGenerator", linenumber=57, variableName="resource", obj=resource))
            resourceNode:YoutubeVideoNode = YoutubeVideoNode(resource)
            logging.debug(DebugMessage.valueOfVariableInContext(className="ResourceNode", methodName="_nodeGenerator", linenumber=59, variableName="resourceNode", obj=resourceNode))
        yield resource
        while True:
            cls._increment_id_key(resource)
            yield resource

class Link(Edge[YoutubeVideoNode]):
    def __init__(self, source:Resource="", target:Resource=""):
        self.source = source
        self.target = target
    
    def startNode(self):
        return self.source
    
    def endNode(self):
        return self.target
    
    def __str__(self) -> str:
        sourceName = self.source["id"]
        targetName = self.target["id"]
        return f"({sourceName}, {targetName})"

#TODO: Make the implementation's responsibility, that the nodes will only store at most 1 element of each object, and that nodes can store mutable objects!
#TODO: Ensure, that parallel execution is supported, and the collection of codes during the execution of a method will remain unchanged from outside methods!
#TODO: In case of a major update of the API of googleapiclient, this class might have to be updated. Make a check for whether the class is usable if a new googleapiclient is available, or don't worry because versions of packages are fixed.
class YoutubeVideoGraph(Graph):
    youtube = build('youtube', 'v3', developerKey=get_youtube_API_key())
    def __init__(self, nodes:Set[YoutubeVideoNode], edges:Set[Link]):
        self.nodes = set()
        self.edges = set()

        for node in nodes:
            self.addNode(node)
        
        for edge in edges:
            self.addEdge(edge)
    
    def getNodes(self):
        return self.nodes
    
    def getEdges(self):
        return self.edges
    
    @staticmethod
    def _getRelatedVideos(video:YoutubeVideoNode) -> List[YoutubeVideoNode]:
        # Get the video title
        video_title = video['snippet']['title']

        # Search for videos with the same title
        request = YoutubeVideoGraph.youtube.search().list(
            part="snippet",
            type="video",
            maxResults=1,
            q=video_title
        )
        response = request.execute()

        # Get the video resources for the search results
        relatedVideos = []
        for item in response['items']:
            video_id = item['id']['videoId']
            request = YoutubeVideoGraph.youtube.videos().list(
                part="snippet,contentDetails",
                id=video_id
            )
            response = request.execute()
            for video_resource in response['items']:
                relatedVideos.append(video_resource)

        return relatedVideos

    def searchForNeighbours(video:YoutubeVideoNode) -> List[YoutubeVideoNode]:
        return YoutubeVideoGraph._getRelatedVideos(video)

    def visualize(self):
        # Create a new directed graph
        graph = nx.DiGraph()

        # Add nodes to the graph
        for node in self.getNodes():
            graph.add_node(node['id'])

        # Add edges to the graph
        for edge in self.getEdges():
            graph.add_edge(edge.startNode()['id'], edge.endNode()['id'])

        # Draw the graph
        nx.draw(graph, with_labels=True)
        plt.show()

    def __str__(self) -> str:
        node_str = "Nodes:\n" + "\n".join(str(node["id"]) for node in self.getNodes())
        edge_str = "Edges:\n" + "\n".join(str(edge) for edge in self.getEdges())
        return node_str + "\n" + edge_str