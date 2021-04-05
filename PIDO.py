from copy import copy
from random import randint, choice
from graphs_generators import *
from visualisation_tools import *


# Obligation selector algorithm, original
def biggestObligation(obligationSet):
    """
    Take the set of  obligations and return the one which contains a maximum of vertices. This is the original selector by C. Laforest 
    """
    b = 0
    for i in range (len(obligationSet)):
        if len(obligationSet[i]) > len(obligationSet[b]) :
            b = i
    return obligationSet[b]


# Obligation selector algorithm, IZIGANG alternative
def moreConnectedObligation(graph, obligationSet):
    """
    Take the set of  obligations and return the one which cumulate a maximum of neighbours. This is the alternative selector by IZIGANG tm
    """
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


# Obligation selector algorithm, Random alternative
def randomObligation(obligationSet):
    """
    Take the set of  obligations and return a random one
    """
    return choice(obligationSet)


def searchIDO(graph1, obligationSet1, mode = "Laforest"):
    """
    Take the an instance : a graphs (dictionnary) and an obligation set plus a mode (Laforest, IZIGANG or Random)
    Calculate a PIDO by using the selected selector
    return the solution (set of dominants vertices)
    """
    graph = copy(graph1)
    obligationSet = copy(obligationSet1)
    s = set()

    while len(obligationSet) != 0:

        if mode ==  "Laforest" : 
            b = biggestObligation(obligationSet)
            #print("Laforest")

        elif mode == "IZIGANG":
            b = moreConnectedObligation(graph, obligationSet)
            #print("IZIGANG")

        elif mode == "Random":
            b = randomObligation(obligationSet)
            #print("Random")

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