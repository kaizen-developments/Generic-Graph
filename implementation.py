import subprocess

from googleapiclient.discovery import build, Resource

from graph import Edge, Graph 

from typing import List, Set
from icontract import ensure

import logging 

import networkx
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)

def get_youtube_API_key():
    youtube_API_key_raw = subprocess.run(['/home/solteszistvan/scripts/access_tokens/youtube_API_key.py'], stdout=subprocess.PIPE)
    youtube_API_key = youtube_API_key_raw.stdout.decode('utf-8').strip()
    return youtube_API_key

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

def get_video_resources(username)->List[Resource]:
    youtube = build('youtube', 'v3', developerKey=get_youtube_API_key())

    # Get the channel's content details
    channel_request = youtube.channels().list(
        part='contentDetails',
        forUsername=username
    )
    channel_response = channel_request.execute()
    uploads_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get the list of videos in the uploads playlist
    playlist_request = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_id,
        maxResults=50  # Change this to get more videos
    )
    playlist_response = playlist_request.execute()

    # Extract the video IDs from the response
    video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response['items']]

    # Get the video resources
    video_resources = []
    for video_id in video_ids:
        video_request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        )
        video_response = video_request.execute()
        video_resources.append(video_response['items'][0])
    
    assert (result_s_elements_are_videos := all([video_resource["kind"] == "youtube#video" for video_resource in video_resources])), "All resources returned must be youtube videos."
    logging.info(f"Returning {len(video_resources)} video resources with get_video_resources.")
    return video_resources

videoResources = get_video_resources('schafer5')

graph = ResourceGraph(videoResources, set())
for resource in graph.getNodes():
    neighbours = ResourceGraph.searchForNeighbours(resource)
    for videoResource in neighbours:
        graph.addEdge(Link(resource, videoResource))

graph.visualize()




#videoLinks = ["https://www.youtube.com/watch?v="+ video["id"] for video in videoResources]

#print(videoLinks)