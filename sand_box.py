from PIDO import *
from visualisation_tools import *
from evaluation import *
from graphs_generators import *


#Test functions
def initalTest():

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

    o1 = set(['a','c'])
    o2 = set(['b','d'])
    o3 = set(['e'])

    os = [o1,o2,o3]

    #g, os = instanceGenerator()

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
    visualisation(g,os,s, title = "Laforest")

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
    visualisation(g,os,s, title = "IZIGANG")



def visualisationTest(generator):
    g, os = generator()
    printInstance(g,os)

    s = searchIDO(copy(g),copy(os), mode = "Laforest")
    s1 = searchIDO(copy(g),copy(os), mode = "IZIGANG")
    s2 = searchIDO(copy(g),copy(os), mode = "Random")

    coveredVertices, dominantVertices = evaluatePIDO(g,s)
    graphs_visualisation(g,os,s, title = "Laforest")
    graphs_visualisation(g,os,s1, title = "IZIGANG")
    graphs_visualisation(g,os,s2, title = "Random")


def main():
    d = statisticCompare(100, instanceGeneratorConnexe)
    #statisticsVisualisation(d, "PIDO results on 100 connexes instances")

    d = statisticCompare(100, instanceGenerator)
    statisticsVisualisation(d, "PIDO results on 100 full random instances")

    #visualisationTest(instanceGeneratorProportionnal)

main()