from implementationClasses import Link, ResourceGraph
from implementationCallables import get_video_resources

videoResources = get_video_resources('schafer5')

graph = ResourceGraph(videoResources, set())
for resource in graph.getNodes():
    neighbours = ResourceGraph.searchForNeighbours(resource)
    for videoResource in neighbours:
        graph.addEdge(Link(resource, videoResource))

graph.visualize()