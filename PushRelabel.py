import numpy as np


class Edge:

    def __init__(self, flow, capacity, u, v):
        self.flow = flow
        self.capacity = capacity
        self.u = u
        self.v = v


class Vertex:

    def __init__(self, h, e_flow):
        self.h = h
        self.e_flow = e_flow


class Graph:

    def __init__(self, graph):

        graph = np.array(graph)
        cities = [graph[i, i] for i in range(np.shape(graph)[0])]
        streets = []
        streetsName = []
        self.streetsName = streetsName
        for i in range(np.shape(graph)[0]):
            for j in range(np.shape(graph)[0]):
                if j > i and graph[i, j] > 0:
                    streets.append(graph[i, j])
                    streetsName.append((i, j))

        self.V = len(cities) + len(streets) + 2
        self.edge = []
        self.ver = []
        for i in range(self.V):
            self.ver.append(Vertex(0, 0))

        for i in range(len(streets)):
            self.addEdge(0, i + 1, streets[i])

        for i in range(len(cities)):
            self.addEdge(len(streets) + i + 1, len(self.ver) - 1, cities[i])

        for i in range(len(streetsName)):
            self.addEdge(i + 1, len(streets) + 1 + streetsName[i][0], np.inf)
            self.addEdge(i + 1, len(streets) + 1 + streetsName[i][1], np.inf)

    def addEdge(self, u, v, capacity):
        self.edge.append(Edge(0, capacity, u, v))

    def preflow(self, s):

        self.ver[s].h = len(self.ver)

        for i in range(len(self.edge)):

            if (self.edge[i].u == s):

                self.edge[i].flow = self.edge[i].capacity

                self.ver[self.edge[i].v].e_flow += self.edge[i].flow

                self.edge.append(
                    Edge(-self.edge[i].flow, 0, self.edge[i].v, s))

    def overFlowVertex(self):

        for i in range(1, len(self.ver)-1):

            if (self.ver[i].e_flow > 0):
                return i

        return -1

    def updateReverseEdgeFlow(self, i, flow):

        u = self.edge[i].v
        v = self.edge[i].u

        for j in range(0, len(self.edge)):
            if (self.edge[j].v == v and self.edge[j].u == u):
                self.edge[j].flow -= flow
                return

        e = Edge(0, flow, u, v)
        self.edge.append(e)

    def push(self, u):

        for i in range(0, len(self.edge)):

            if (self.edge[i].u == u):

                if (self.edge[i].flow == self.edge[i].capacity):
                    continue

                if (self.ver[u].h > self.ver[self.edge[i].v].h):

                    flow = min(self.edge[i].capacity -
                               self.edge[i].flow, self.ver[u].e_flow)

                    self.ver[u].e_flow -= flow

                    self.ver[self.edge[i].v].e_flow += flow

                    self.edge[i].flow += flow

                    self.updateReverseEdgeFlow(i, flow)

                    return True

        return False

    def relabel(self, u):

        mh = 2100000

        for i in range(len(self.edge)):
            if (self.edge[i].u == u):

                if (self.edge[i].flow == self.edge[i].capacity):
                    continue

                if (self.ver[self.edge[i].v].h < mh):
                    mh = self.ver[self.edge[i].v].h

                    self.ver[u].h = mh + 1

    def getMaxFlow(self, s, t):

        self.preflow(s)

        while (self.overFlowVertex() != -1):

            u = self.overFlowVertex()
            if (self.push(u) == False):
                self.relabel(u)

        return self.ver[len(self.ver)-1].e_flow


# gx = [[50, 150, 0, 100],
#       [150, 70, 50, 0],
#       [0, 50, 60, 0],
#       [100, 0, 0, 10]]

# g = Graph(gx)
# print(g.getMaxFlow(0, len(g.ver) - 1))

# for item in g.edge:
#     print(item.u, item.v, item.capacity - item.flow)
