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
    for i in range(np.shape(solve)[1]):
        if solve[0, i] > 0:
            streets.append(streetName[i-cities - 1])

    return streets


# gx = [[50, 150, 0, 100],
#       [150, 70, 50, 0],
#       [0, 50, 60, 0],
#       [100, 0, 0, 10]]

# print(solve(gx))
