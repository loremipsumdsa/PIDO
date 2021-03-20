from copy import copy
from random import randint, choice
from graphviz import Graph

# Debug tools
DEBUGMODE = False

def printD(message):
    if DEBUGMODE:
        print(message)

graph = dict()

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
        
    vertices = randint(minVertices, maxVertices)

    obligations = randint(minObligations, maxObligations)

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

    for i in range(edges):

        o1 = randint(0,obligations - 1)
        o2 = o1
        while o2 == o1:
            o2 = randint(0,obligations - 1)

        p1 = randint(0, len(obligationSet[o1]) - 1)
        p2 = randint(0, len(obligationSet[o2]) - 1)

        addEdge(graph, list(obligationSet[o1])[p1], list(obligationSet[o2])[p2])

    return (graph, obligationSet)

def instanceGeneratorConnexe(minVertices = 100, maxVertices = 1000, minObligations = 3, maxObligations = 100, minEdges = 100, maxEdges = 1000):
    
    vertices = randint(minVertices, maxVertices)

    obligations = randint(minObligations, maxObligations)

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

def instanceGeneratorProportionnal(coef = 1):
    minVertices = randint(1,100)
    maxVertices = minVertices + 9900
    minEdges = int(coef * minVertices)
    maxEdges = int(coef * maxVertices)
    return instanceGenerator(minVertices = minVertices, maxVertices = maxVertices, minEdges = minEdges, maxEdges = maxEdges)


# PIDO algorithm, original
def biggestObligation(obligationSet):
    b = 0
    for i in range (len(obligationSet)):
        if len(obligationSet[i]) > len(obligationSet[b]) :
            b = i
    return obligationSet[b]


# PIDO algorithm, IZIGANG alternative
def moreConnectedObligation(graph, obligationSet):
    b = 0
    neighbourI=set()
    neighbourB=set()

    for i in range (len(obligationSet)):
        neighbourI=set()

        for vertex in obligationSet[i]:

            for neighbourVertex in graph[vertex]:
                neighbourI.add(neighbourVertex)

            if len(neighbourI)>len(neighbourB):
                b=i
                neighbourB=neighbourI.copy()

    return obligationSet[b]


# PIDO algorithm, Random alternative
def randomObligation(obligationSet):
    return choice(obligationSet)


def searchIDO(graph1, obligationSet1, mode = "Laforest"):
    
    graph = copy(graph1)
    obligationSet = copy(obligationSet1)
    s = set()

    while len(obligationSet) != 0:

        if mode ==  "Laforest" : 
            b = biggestObligation(obligationSet)
            print("Laforest")

        elif mode == "IZIGANG":
            b = moreConnectedObligation(graph, obligationSet)
            print("IZIGANG")

        elif mode == "Random":
            b = randomObligation(obligationSet)
            print("Random")

        else :
            exit("Error : Unknown mode")

        printD(f"Working on obligation containing {b} ")
        s = s | b

        n = set()
        for vertex in b :
            try :
                n = n | graph[vertex]
            except KeyError:
                pass

        o = set()
        for obligation in obligationSet:
            for neihbourg in n:
                if neihbourg in obligation:
                    o = o | obligation
                    break

        for vertex in b:
            deleteVertex(graph,vertex)
        obligationSet.remove(b)

        for vertex in o:
            deleteVertex(graph,vertex)
            for obligation in obligationSet:
                if vertex in obligation:
                        obligationSet.remove(obligation)
                        break

    return s

#Solution evaluation function
def evaluateIDO(graph, solution):
    vertices = set(graph.keys())

    isCovered = dict()
    for v in vertices:
        isCovered[v] = False

    for v in solution:
        isCovered[v] = True
        for neihbourg in graph[v]:
            isCovered[neihbourg] = True
    count = 0
    for v in vertices:
        if isCovered[v]:
            count +=1

    return (count/len(vertices) * 100, len(solution)/len(vertices) * 100)




#Prints functions
def printInstance(graph, obligationSet):
    print("------- INSTANCE -----------")
    print(f"Number of vertices : {len(graph.keys())}")
    print(f"Number of obligation : {len(obligationSet)}")

    print("\n")


def printResult(graph, solution, evaluation = True):
    print("------- RESULT -----------")
    print("Dominating Vertices", end = " : ")
    for v in solution:
        print(v, end = ", ")

    if evaluation:
        overedVertices, dominatingVertices = evaluateIDO(graph,solution)
        print("\nSolution's evaluation :")
        print(f"    Covered vertices rate : {coveredVertices} %")
        print(f"    Dominating vertices rate : {dominatingVertices} %")

    print("\n")


def visualisation(graph, obligationSet, solution, title = "new_graph_view"):

    includedEdges = set()
    includedVertices = dict()

    verticesColor  = dict()

    for obligation in obligationSet:
        random_number = randint(0,16777215)
        hex_number = str(hex(random_number))
        hex_number ='#'+ hex_number[2:]
        for vertex in obligation:
            verticesColor[vertex] = hex_number

    for vertex in graph.keys():
        includedVertices[vertex] = False

    g = Graph('G', filename=title+'.gv', engine='sfdp')

    for vertex in solution:
        g.node(str(vertex), fillcolor = "#b5ff66", style = "filled", color = verticesColor[vertex], penwidth = "2")
        includedVertices[vertex] = True
        
        for neihbourg in graph[vertex]:
            g.node(str(neihbourg), fillcolor = "#e6ffcc", style = "filled", color = verticesColor[neihbourg], penwidth = "2")
            includedVertices[neihbourg] = True

        for vertex in graph.keys():
            if not(includedVertices[vertex]):
                g.node(str(vertex), fillcolor = "white", style = "filled", color = verticesColor[vertex], penwidth = "2")
                includedVertices[vertex] = True

    for vertex in graph.keys():
        for neihbourg in graph[vertex]:
            if not((vertex,neihbourg) in includedEdges):
                g.edge(str(vertex), str(neihbourg))
                includedEdges.add((vertex,neihbourg))
                includedEdges.add((neihbourg,vertex))


    g.view()


#Test functions
def initalTest():
    
    """
    g = createGraph()
    
    addVertex(g,'a')
    addVertex(g,'b')
    addVertex(g,'c')
    addVertex(g,'d')
    addVertex(g,'e')

    addEdge(g,'a','b')
    addEdge(g,'b','c')
    addEdge(g,'c','d')
    addEdge(g,'b','e')

    o1 = ['a','c']
    o2 = ['b','d']
    o3 = ['e']

    os = [o1,o2,o3]

    """

    g, os = instanceGenerator()

    print("------- INSTANCE -----------")
    print(f"Number of vertices : {len(g.keys())}")
    print(f"Number of obligation : {len(os)}")

    print("\n")

    print("------- ALGORITHM (Laforest's version) -----------")
    s = searchIDO(copy(g),copy(os), mode = "Laforest")

    print("\n")

    print("------- RESULT -----------")
    print("Dominating Vertices", end = " : ")
    for v in s:
        print(v, end = ", ")

    coveredVertices, dominatingVertices = evaluateIDO(g,s)
    print("\nSolution's evaluation :")
    print(f"    Covered vertices rate : {coveredVertices} %")
    print(f"    Dominating vertices rate : {dominatingVertices} %")

    print("\n")

    print("------- ALGORITHM (IZIGANG tm's version) -----------")
    s = searchIDO(copy(g),copy(os), mode = "IZIGANG")

    print("\n")

    print("------- RESULT -----------")
    print("Dominating Vertices", end = " : ")
    for v in s:
        print(v, end = ", ")

    coveredVertices, dominatingVertices = evaluateIDO(g,s)
    print("\nSolution's evaluation :")
    print(f"    Covered vertices rate : {coveredVertices} %")
    print(f"    Dominating vertices rate : {dominatingVertices} %")


def statisticCompare(n):
    avgcr1 = 0
    avgdr1 = 0
    avgcr2 = 0
    avgdr2 = 0
    avgcr3 = 0
    avgdr3 = 0
    for i in range(n):
        #g, os = intanceGeneratorProportionnal(coef = 15)
        g, os = instanceGenerator()
        s1 = searchIDO(copy(g),copy(os), mode = "Laforest")
        s2 = searchIDO(copy(g),copy(os), mode = "IZIGANG")
        s3 = searchIDO(copy(g),copy(os), mode = "Random")
        cr1,dr1 = evaluateIDO(g, s1)
        cr2,dr2 = evaluateIDO(g, s2)
        cr3,dr3 = evaluateIDO(g, s3)

        avgcr1 += cr1
        avgdr1 += dr1

        avgcr2 += cr2
        avgdr2 += dr2

        avgcr3 += cr3
        avgdr3 += dr3

    print(f"Laforest : {avgcr1/n} ---- IZIGANG : {avgcr2/n} ---- Random : {avgcr3/n}")

#statisticCompare(1000)

def visualisationTest():
    g, os = instanceGenerator()
    s = searchIDO(copy(g),copy(os), mode = "Laforest")
    s2 = searchIDO(copy(g),copy(os), mode = "IZIGANG")

    print("------- INSTANCE -----------")
    print(f"Number of vertices : {len(g.keys())}")
    print(f"Number of obligation : {len(os)}")

    print("------- RESULT -----------")
    print("Dominating Vertices", end = " : ")
    for v in s:
        print(v, end = ", ")

    coveredVertices, dominatingVertices = evaluateIDO(g,s)
    print("\nSolution's evaluation :")
    print(f"    Covered vertices rate : {coveredVertices} %")
    print(f"    Dominating vertices rate : {dominatingVertices} %")

    print("\n")
    visualisation(g,os,s, title = "Laforest")
    visualisation(g,os,s2, title = "IZIGANG")


#visualisationTest()

statisticCompare(1000)

#initalTest()
#g,os = instanceGeneratorConnexe(minVertices = 10, maxVertices = 20, minObligations = 3, maxObligations = 10, minEdges = 10, maxEdges = 30)
#s = searchIDO(copy(g),copy(os), mode = "IZIGANG")
#visualisation(g,os,s, title = "IZIGANG")