from Implementations import Node
from Implementations import Edge
import numpy as np


def TitoBruteForce(graph):
    graph = np.array(graph)
    cityTake = [False for i in range(np.shape(graph)[0])]
    cities = [graph[i, i] for i in range(np.shape(graph)[0])]
    streets = []
    streetName = []
    for i in range(np.shape(graph)[0]):
        for j in range(np.shape(graph)[1]):
            if j > i and graph[i, j] > 0:
                streets.append(graph[i, j])
                streetName.append((i, j))

    return Solve(streetName, streets, cityTake, cities, 0)


def Solve(streetName, streets, cityTake, cities, funds):
    if len(streets) == 0:
        return [], 0

    cStreet = streetName[0]
    nCityCopy = cityTake.copy()
    nTakePath, nTake = Solve(
        streetName[1:], streets[1:], nCityCopy, cities, funds)

    cityCopy = cityTake.copy()
    funds = 0
    if not cityCopy[cStreet[0]]:
        funds += cities[cStreet[0]]
        cityCopy[cStreet[0]] = True

    if not cityCopy[cStreet[1]]:
        funds += cities[cStreet[1]]
        cityCopy[cStreet[1]] = True

    gain = streets[0] - funds

    if gain >= 0:
        funds = 0
    else:
        funds -= streets[0]

    TakePath, Take = Solve(
        streetName[1:], streets[1:], cityCopy, cities, funds)
    TakePath.append(cStreet)
    Take += gain

    if Take > nTake:
        return TakePath, Take

    else:
        return nTakePath, nTake


# gx = [[50, 150, 0, 100],
#       [150, 70, 50, 0],
#       [0, 50, 60, 0],
#       [100, 0, 0, 10]]

# print(TitoBruteForce(gx))
