from copy import copy
from random import randint, choice
from graphs_generators import *
from visualisation_tools import *


def biggestObligation(graph,obligationSet):
    """
    Take an instance and return the obligation which contains a maximum of vertices. This is the original selector by C. Laforest 
    """
    b = 0
    for i in range (len(obligationSet)):
        if len(obligationSet[i]) > len(obligationSet[b]) :
            b = i
    return obligationSet[b]


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
    Take an instance and return the obligation which has the better domination balance.
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
    Take an instance and return a random obligation
    """
    return choice(obligationSet)


def obligationsOrder(graph1, obligationsSet1, selector):
    '''
    Take an instance, a selector function and return the obligation set, ordered on the criteria of the selector
    '''
    obligationsSet = copy(obligationsSet1)
    graph = copy(graph1)
    orderedObligationsSet = []
    while obligationsSet != []:
        o = selector(graph,obligationsSet)
        orderedObligationsSet.append(o)
        obligationsSet.remove(o)

    return orderedObligationsSet


def nextObligation(graph, obligationSet):
    '''
    Take an instance with an ordered set of obligation, return the fist obligation
    '''
    return obligationSet[0]


def searchIDO(graph1, obligationSet1, selector):
    """
    Take the an instance : a graphs (dictionnary) and an obligation set plus a selector
    Calculate a PIDO by using the given selector
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