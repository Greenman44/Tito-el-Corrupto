from FordFulkerson import *
import numpy as np


def SolveFordFulkerson(graph):
    graph, cities, streetName = GraphBuilder(graph)
    g = Graph(graph)
    source = 0
    sink = np.shape(g.graph)[0]-1
    maxf = g.ford_fulkerson(source, sink)
    solve = g.graph
    streets = []
    cST = DFS(np.array(g.graph), 0, [
              False for i in range(np.shape(g.graph)[0])])

    for i in range(len(streetName)):
        if cST[i + 1]:
            streets.append(streetName[i])

    return streets


gx = [[15, 10, 15],
      [10, 1, 0],
      [15, 0, 1],
      ]

x = SolveFordFulkerson(gx)
print(x)
