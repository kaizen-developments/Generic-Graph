from googleapiclient.discovery import build, Resource
from Classes.abstractModule_graph import Edge, Graph 
from typing import List, Set
import networkx as nx
import matplotlib.pyplot as plt

from implementationCallables import get_youtube_API_key

class Link(Edge):
    def __init__(self, source:Resource, target:Resource):
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
    
class ResourceGraph(Graph):
    youtube = build('youtube', 'v3', developerKey=get_youtube_API_key())
    def __init__(self, nodes:Set[Resource], edges:Set[Link]):
        self.nodes = nodes
        self.edges = edges
    
    def getNodes(self):
        return self.nodes
    
    def getEdges(self):
        return self.edges
    
    @staticmethod
    def _getRelatedVideos(video:Resource) -> List[Resource]:
        # Get the video title
        video_title = video['snippet']['title']

        # Search for videos with the same title
        request = ResourceGraph.youtube.search().list(
            part="snippet",
            type="video",
            maxResults=5,
            q=video_title
        )
        response = request.execute()

        # Get the video resources for the search results
        relatedVideos = []
        for item in response['items']:
            video_id = item['id']['videoId']
            request = ResourceGraph.youtube.videos().list(
                part="snippet,contentDetails",
                id=video_id
            )
            response = request.execute()
            for video_resource in response['items']:
                relatedVideos.append(video_resource)

        return relatedVideos

    def searchForNeighbours(video:Resource) -> List[Resource]:
        return ResourceGraph._getRelatedVideos(video)

    def visualize(self):
        # Create a new directed graph
        graph = nx.DiGraph()

        # Add nodes to the graph
        for node in self.getNodes():
            graph.add_node(node['id'])

        # Add edges to the graph
        for edge in self.getEdges():
            graph.add_edge(edge.sourceNode()['id'], edge.targetNode()['id'])

        # Draw the graph
        nx.draw(graph, with_labels=True)
        plt.show()

    def __str__(self) -> str:
        node_str = "Nodes:\n" + "\n".join(str(node["id"]) for node in self.getNodes())
        edge_str = "Edges:\n" + "\n".join(str(edge) for edge in self.getEdges())
        return node_str + "\n" + edge_str