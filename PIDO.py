from copy import copy
from random import randint, choice
from graphs_generators import *
from visualisation_tools import *


# Obligation selector algorithm, original
def biggestObligation(graph,obligationSet):
    """
    Take the set of  obligations and return the one which contains a maximum of vertices. This is the original selector by C. Laforest 
    """
    b = 0
    for i in range (len(obligationSet)):
        if len(obligationSet[i]) > len(obligationSet[b]) :
            b = i
    return obligationSet[b]


# Obligation selector algorithm, IZIGANG alternative
def mostDominantObligation(graph, obligationSet):
    """
    Take the graph and the set of  obligations and return the one which cumulate a maximum of neighbours.
    """
    b = 0
    neighbourI=set()
    neighbourB=set()

    for i in range (len(obligationSet)):
        neighbourI=set()

        for vertex in obligationSet[i]:

            neighbourI = neighbourI | graph[vertex]
            #for neighbourVertex in graph[vertex]:
                #neighbourI.add(neighbourVertex)

            if len(neighbourI)>len(neighbourB):
                b=i
                neighbourB=neighbourI.copy()

    return obligationSet[b]


def mostCoveringObligation(graph,obligationSet):
    """
    Take the graph and the set of  obligations and return the one which covers a maximum of vertices .
    """
    b = 0
    neighbourI=set()
    neighbourB=set()

    for i in range (len(obligationSet)):
        neighbourI=set()

        for vertex in obligationSet[i]:
            neighbourI.add(vertex)
            neighbourI = neighbourI | graph[vertex]

            if len(neighbourI) > len(neighbourB):
                b=i
                neighbourB=neighbourI.copy()

    return obligationSet[b]


def mostDominatingObligation(graph,obligationSet):
    """
    Take the graph and the set of  obligations and return the one which has the better domination balance.
    """
    b = 0
    neighbourI=set()
    neighbourB=set()

    for i in range (len(obligationSet)):
        neighbourI=set()

        for vertex in obligationSet[i]:
            neighbourI.add(vertex)
            neighbourI = neighbourI | graph[vertex]

            if len(neighbourI)/len(obligationSet[i])>len(neighbourB)/len(obligationSet[b]):
                b=i
                neighbourB=neighbourI.copy()

    return obligationSet[b]

def randomObligation(graph,obligationSet):
    """
    Take the set of  obligations and return a random one
    """
    return choice(obligationSet)

def nextObligation(graph, obligationSet):
    return obligationSet[0]

def searchIDO(graph1, obligationSet1, selector):
    """
    Take the an instance : a graphs (dictionnary) and an obligation set plus a mode (Laforest, IZIGANG or Random)
    Calculate a PIDO by using the selected selector
    return the solution (set of dominants vertices)
    """
    graph = copy(graph1)
    obligationSet = copy(obligationSet1)
    s = set()

    while len(obligationSet) != 0:

        b = selector(graph,obligationSet)

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