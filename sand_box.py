from PIDO import *
from visualisation_tools import *
from evaluation import *
from graphs_generators import *
#from graphs_generators2 import *
import matplotlib.pyplot as plt

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

    coveredVertices, dominatingVertices = evaluatePIDO(g,s)
    print("\nSolution's evaluation :")
    print(f"    Covered vertices rate : {coveredVertices} %")
    print(f"    Dominating vertices rate : {dominatingVertices} %")
    graphs_visualisation(g,os,s, title = "Laforest")

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

    coveredVertices, dominantVertices, caca = evaluatePIDO(g,s)
    graphs_visualisation(g,os,s, title = "Laforest")
    graphs_visualisation(g,os,s1, title = "IZIGANG")
    graphs_visualisation(g,os,s2, title = "Random")

    plt.text(bar, (statistics[bar][1]+statistics[bar][0])/2, str(round(statistics[bar][0],1))+"%", color='black', fontweight='light', fontsize = "large")
def main():
    #d = statisticCompare(3, instanceGeneratorHypercube)
    #statisticsVisualisation(d, "PIDO results on 3 hypercubes instances")

    # d = statisticCompare(100, instanceGenerator)
    # statisticsVisualisation(d, "PIDO results on 100 full random instances")

    d = statisticCompare(500, instanceGenerator,["Laforest","IZIGANG","Alternative","Alternative2","Random"])
    statisticsVisualisation(d, "PIDO results on 100 hypercubes instances")

    #print("caca")
    #visualisationTest(instanceGeneratorHypercube)
    #print("caca2")
    #initalTest()

    #g,os = InstanceFromFile("H3")
    #s = searchIDO(g,os, mode = "IZIGANG")
    #graphs_visualisation(g,os,s, title = "IZIGANG")

    """
    g,os = instanceGeneratorHypercube()
    instanceToFile(g,os,"test.txt")

    g1,os1 = instanceFromFile("test.txt")
    s = searchIDO(g1,os1, mode = "IZIGANG")
    graphs_visualisation(g1,os1,s, title = "IZIGANG")
    """

main()