from random import randint, choice, shuffle
from visualisation_tools import *
from math import *
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



def obligationsGenerator(graph,minObligations=5,maxObligations=10):
    """Returns a set of minObligations to maxObligations obligations for a graph.
    If the generator is not able to create a set of minObligations to maxObligations obligations, then it will increase the number of obligations to do so."""
    obligations = randint(minObligations,maxObligations)

    obligationSet=[]

    for i in range(obligations):
        obligationSet.append(set())

    for v in graph:
        shuffle(obligationSet)
        for o in range(0,len(obligationSet)):
            isStable=True
            for n in graph[v]:
                if n in obligationSet[o]:
                    isStable=False
                    break
            if isStable==True:
                obligationSet[o].add(v)
                break
        if isStable==False:
            obligationSet.append(set())
            obligationSet[o+1].add(v)

    while set() in obligationSet:
        obligationSet.remove(set())

    if len(obligationSet)>obligations:
        printW(f"WARNING: The obligations generator could not generate a number of obligations uncluded between {minObligations} and {maxObligations}.")
        printW(f"It, instead, created {len(obligationSet)} obligations.")

    return (obligationSet,len(obligationSet))



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



def instanceGeneratorComplete_graph(minVertices=5,maxVertices=10,minObligations=10,maxObligations=20):
    """Constructs a complete graph of n vertices, returns the corresponding graph and a setof minObligations to maxObligations obligations.
    n varies randomly between minVertices and maxVertices."""
    n = randint(minVertices,maxVertices)

    obligations = randint(minObligations,maxObligations)

    obligationSet=[]

    graph=createGraph()

    for vertex in range(0,n):
        addVertex(graph,vertex)
        for neighbour in range(0,vertex):
            addEdge(graph,vertex,neighbour)
        for neighbour in range(vertex+1,n):
            addEdge(graph,vertex,neighbour)

    obligationSet,obligations=obligationsGenerator(graph,obligations,obligations)

    return (graph,obligationSet)



def instanceGeneratorGrid_graph(minColumns=5,maxColumns=10,minLines=5,maxLines=10,minObligations=5,maxObligations=20):
    """Constructs a grid pXq, returns the corresponding graph and a set of minObligations to maxObligations obligations.
    p varis between minColumns and maxColumns and q varies between minLines and maxLines."""
    p = randint(minColumns,maxColumns)

    q = randint(minLines,maxLines)

    obligations = randint(minObligations, maxObligations)

    obligationSet=[]

    graph=createGraph()

    for i in range(p):
        for j in range(q):
            addVertex(graph,str(i)+str(j))
    for i in range(p):
        for j in range(q):
            if i-1 >= 0 :
                addEdge(graph,str(i)+str(j),str(i-1)+str(j))
            if i+1 < p:
                addEdge(graph,str(i)+str(j),str(i+1)+str(j))
            if j-1 >= 0 :
                addEdge(graph,str(i)+str(j),str(i)+str(j-1))
            if j+1 < q:
                addEdge(graph,str(i)+str(j),str(i)+str(j+1))

    obligationSet,obligations=obligationsGenerator(graph,obligations,obligations)

    return (graph,obligationSet)



def instanceGeneratorTorus_graph(minColumns=5,maxColumns=10,minLines=5,maxLines=10,minObligations=5,maxObligations=20):
    """Constructs a torus pXq, returns the corresponding graph and a set of minObligations to maxObligations obligations.
    p varies between minColumns and maxColumns and q varies between minLines and maxLines."""
    p = randint(minColumns,maxColumns)

    q = randint(minLines,maxLines)

    obligations = randint(minObligations, maxObligations)

    obligationSet=[]

    graph=createGraph()

    for i in range(p):
        for j in range(q):
            addVertex(graph,str(i)+str(j))
    for i in range(p):
        for j in range(q):
            if i-1 >= 0 :
                graph[str(i)+str(j)].add(str(i-1)+str(j))
                #graph[str(i-1)+str(j)].add(str(i)+str(j))
            if i+1 < p:
                graph[str(i)+str(j)].add(str(i+1)+str(j))
                #graph[str(i+1)+str(j)].add(str(i)+str(j))
            if j-1 >= 0 :
                graph[str(i)+str(j)].add(str(i)+str(j-1))
                #graph[str(i)+str(j-1)].add(str(i)+str(j))
            if j+1 < q:
                graph[str(i)+str(j)].add(str(i)+str(j+1))
                #graph[str(i)+str(j+1)].add(str(i)+str(j))

            if (i == p-1):
                graph[str(i)+str(j)].add('0'+str(j))
                graph['0'+str(j)].add(str(i)+str(j))

            if (j == q-1):
                graph[str(i)+str(j)].add(str(i)+'0')
                graph[str(i)+'0'].add(str(i)+str(j))

    obligationSet,obligations=obligationsGenerator(graph,obligations,obligations)

    return (graph,obligationSet)



def instanceGeneratorHypercube(minDimensions = 10, maxDimensions = 10, minObligations =6 , maxObligations = 6):
    """Constructs the hypercube graph of random dimension between minDimensions and maxDimensions and returns the graph plus the set of minObligations to maxObligations obligations.
    Each vertex is associated to a binary word of length d.
    For example '001101' is a vertex of hypercube of dimension 6.
    Two vertices are neighbors iff they differ on exactly one bit.
    For example, 01001 and 01101 are neighbors in hypercube(5)."""
    dimensions = randint(minDimensions, maxDimensions)

    obligations = randint(minObligations, maxObligations)

    obligationSet = []

    graph=createGraph()

    for vertex in range(0,2**(dimensions)):

        vertex="{0:b}".format(vertex)
        vertex="0"*(dimensions-len(vertex))+vertex
        binary=list(vertex)
        addVertex(graph,vertex)
        for bit in range(0,len(binary)):
            binary[bit]=str((int(binary[bit])-1)*(-1))
            addEdge(graph,vertex,''.join(binary))
            binary[bit]=str((int(binary[bit])-1)*(-1))
    

    obligationSet,obligations=obligationsGenerator(graph,obligations,obligations)


    return (graph,obligationSet)


def instanceFromFile(file):
    graphMode = True

    graph = dict()
    obligationsSet = []
    with open(file) as f :
        for line in f:

            if line == "\n":
                graphMode = False


            elif graphMode:
                if line[-1] == '\n':
                    line = line[:-1]

                info = line.split(":")
                graph[info[0]] = set(info[1:])

            else:
                if line[-1] == '\n':
                    line = line[:-1]
                obligation = set(line.split(","))
                obligationsSet.append(obligation)


    if obligationsSet == []:
        printW("Warning : Aucune obligation n'a été lu. Un set d'obligation aléatoire va être généré")
        obligationsSet = obligationsGenerator(graph, minObligations = 1, maxObligations = len(graph.keys()))

    return (graph,obligationsSet)

def instanceToFile(graph, obligationsSet, file):
    graphMode = True

    with open(file,"w+") as f :
        for v in graph.keys():

            print(str(v))
            print(":".join(str(n) for n in graph[v]))
            f.write(str(v))
            if len(graph[v])>0:
                f.write(":"+ ":".join(str(n) for n in graph[v])+"\n")
            else:
                f.write("\n")

        f.write("\n")

        for o in obligationsSet:
            f.write(",".join(str(v) for v in o)+"\n")