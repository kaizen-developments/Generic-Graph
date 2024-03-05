from implementationClasses import Link, YoutubeVideoGraph
from implementationCallables import get_videos_on_the_channel

videoResources = get_videos_on_the_channel('schafer5')

graph = YoutubeVideoGraph(videoResources, set())
for resource in graph.getNodes():
    neighbours = YoutubeVideoGraph.searchForNeighbours(resource)
    for videoResource in neighbours:
        graph.addEdge(Link(resource, videoResource))

graph.visualize()