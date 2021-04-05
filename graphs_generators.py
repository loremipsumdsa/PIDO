from random import randint, choice
from visualisation_tools import *

# Graph manipulation functions
def addEdge(graph, v1,v2):
    try :
        graph[v1].add(v2)
        graph[v2].add(v1)
    except KeyError:
        pass

def createGraph():
    return dict()

def addVertex(graph, v):
    graph[v] = set()


def deleteVertex(graph, v):
    try :
        del graph[v]
    except KeyError:
        pass


#Instance generators
def instanceGenerator(minVertices = 100, maxVertices = 1000, minObligations = 3, maxObligations = 100, minEdges = 100, maxEdges = 1000):
    """
    Return a random instance : a tuple of a graph (dictionnary) and an obligation set. 
    The instance will respect the specifications in parameter : minVertices, maxVertices, minObligations, maxObligations, minEdges, maxEdges
    Warning : it can't exist a instance with more obligations than vertices, and it can't exist a graph with more than 2^{n-1} edges where n is the number of vertices
    the function treat that kind of exception
    """
    vertices = randint(minVertices, maxVertices)

    if maxObligations > vertices:
        maxObligations = vertices
    if minObligations > vertices:
        minObligations = vertices
    obligations = randint(minObligations, maxObligations)

    if maxEdges > 2**(vertices - 1):
        maxEdges = 2**(vertices - 1)
    if minEdges > 2**(vertices - 1):
        minEdges = 2**(vertices - 1)
    edges = randint(minEdges, maxEdges)
    
    graph = dict()
    obligationSet = []

    for i in range(obligations):
        obligationSet.append(set())

    for v in range(vertices):
        o = randint(0,obligations - 1)
        obligationSet[o].add(v)
        addVertex(graph, v)

    while set() in obligationSet:
        obligationSet.remove(set())
        obligations -=1 

    actualEdges = 0
    while actualEdges < edges:

        o1 = randint(0,obligations - 1)
        o2 = o1
        while o2 == o1:
            o2 = randint(0,obligations - 1)

        p1 = randint(0, len(obligationSet[o1]) - 1)
        p2 = randint(0, len(obligationSet[o2]) - 1)

        if not(p1 in graph[p2]):
            addEdge(graph, list(obligationSet[o1])[p1], list(obligationSet[o2])[p2])
            actualEdges+=1

    return (graph, obligationSet)

def instanceGeneratorConnexe(minVertices = 100, maxVertices = 1000, minObligations = 3, maxObligations = 100, minEdges = 100, maxEdges = 1000):
    """
    Return a random instance : a tuple of a connexe graph (dictionnary) and an obligation set. 
    The instance will respect the specifications in parameter : minVertices, maxVertices, minObligations, maxObligations, minEdges, maxEdges
    Warning : it can't exist a instance with more obligations than vertices, and it can't exist a graph with more than 2^{n-1} edges where n is the number of vertices
    as the graph is connexe, the minimum number of edges is n-1 where n is the actual number of vertices 
    the function treat that kind of exception
    """
    vertices = randint(minVertices, maxVertices)


    if maxObligations > vertices:
        maxObligations = vertices
    if minObligations > vertices:
        minObligations = vertices
    obligations = randint(minObligations, maxObligations)

    if maxEdges > 2**(vertices - 1):
        maxEdges = 2**(vertices - 1)
    if minEdges < vertices - 1:
        minEdges = vertices -1
    edges = randint(minEdges, maxEdges)
    
    actualEdges = 0

    graph = dict()
    obligationSet = []

    for i in range(obligations):
        obligationSet.append(set())

    obligationSet[0].add(0)
    addVertex(graph,0)

    for v in range(1, vertices):
        vp = randint(0,v-1)
        o = choice(obligationSet)
        while vp in o:
            o = choice(obligationSet)

        o.add(v)
        addVertex(graph, v)
        addEdge(graph, v, vp)


    while set() in obligationSet:
        obligationSet.remove(set())
        obligations -=1 

    for i in range(edges - vertices):

        o1 = randint(0,obligations - 1)
        o2 = o1
        while o2 == o1:
            o2 = randint(0,obligations - 1)

        p1 = randint(0, len(obligationSet[o1]) - 1)
        p2 = randint(0, len(obligationSet[o2]) - 1)

        addEdge(graph, list(obligationSet[o1])[p1], list(obligationSet[o2])[p2])

    return (graph, obligationSet)

def instanceGeneratorProportionnal(minVertices = 10 , maxVertices = 100,coef = 25):
    """
    Return a random instance : a tuple of a graph (dictionnary) and an obligation set.
    The instance will respect the specifications in parameter : minVertices, maxVertices


    """
    vertices = randint(minVertices,maxVertices)
    edges = int(coef * vertices)
    return instanceGenerator(minVertices = vertices, maxVertices = vertices, minEdges = edges, maxEdges = edges)
