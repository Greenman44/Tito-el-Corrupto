from collections import defaultdict
import numpy as np


def GraphBuilder(graph):
    graph = np.array(graph)
    m = np.shape(graph)[0]
    cities = [graph[i, i] for i in range(m)]
    streets = []
    streetName = []
    for i in range(m):
        for j in range(m):
            if j > i and graph[i, j] > 0:
                streets.append(graph[i, j])
                streetName.append((i, j))
    graph = np.zeros((len(cities) + len(streets) + 2,
                      len(cities) + len(streets) + 2))
    for i in range(len(cities)):
        graph[i + 1, len(cities) + len(streets) + 1] = cities[i]

    for i in range(len(streets)):
        graph[0, len(cities) + i + 1] = streets[i]
        graph[len(cities) + i + 1, streetName[i][0] + 1] = np.inf
        graph[len(cities) + i + 1, streetName[i][1] + 1] = np.inf

    return graph, len(cities), streetName


class Graph:

    def __init__(self, graph):
        self.graph = graph
        self. ROW = len(self.graph)

    # Using BFS as a searching algorithm

    def searching_algo_BFS(self, s, t, parent):

        visited = [False] * (self.ROW)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    # Applying fordfulkerson algorithm
    def ford_fulkerson(self, source, sink):
        parent = [-1] * (self.ROW)
        max_flow = 0

        while self.searching_algo_BFS(source, sink, parent):

            path_flow = float("Inf")
            s = sink
            while (s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Adding the path flows
            max_flow += path_flow

            # Updating the residual values of edges
            v = sink
            while (v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow


def DFS(graph, currentVertex, visited):
    visited[currentVertex] = True
    for i in range(np.shape(graph)[1]):
        if graph[currentVertex][i] > 0 and not visited[i]:
            DFS(graph, i, visited)
    return visited


# gx = [[0, 10, 20, 3, 0, 0, 0, 0, 0],
#       [0, 0, 0, 0, np.inf, np.inf, 0, 0, 0],
#       [0, 0, 0, 0, 0, np.inf, np.inf, 0, 0],
#       [0, 0, 0, 0, 0, np.inf, np.inf, np.inf, 0],
#       [0, 0, 0, 0, 0, 0, 0, 0, 5],
#       [0, 0, 0, 0, 0, 0, 0, 0, 15],
#       [0, 0, 0, 0, 0, 0, 0, 0, 4],
#       [0, 0, 0, 0, 0, 0, 0, 0, 7],
#       [0, 0, 0, 0, 0, 0, 0, 0, 0]
#       ]
# gx = [[0, 10, 15, 0, 0, 0, 0],
#       [0, 0, 0, np.inf, np.inf, 0, 0],
#       [0, 0, 0, np.inf, 0, np.inf, 0],
#       [0, 0, 0, 0, 0, 0, 15],
#       [0, 0, 0, 0, 0, 0, 1],
#       [0, 0, 0, 0, 0, 0, 1],
#       [0, 0, 0, 0, 0, 0, 0]
#       ]
# g = Graph(gx)

# source = 0
# sink = 6
# print("Max Flow: %d " % g.ford_fulkerson(source, sink))
# print(DFS(np.array(g.graph), 0, [False for i in range(np.shape(g.graph)[0])]))
