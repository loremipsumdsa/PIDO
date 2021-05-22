from PIDO import *
from graphs_generators import *
from visualisation_tools import printD

def checkSolution(os,solution):
    """
    Take an obligations set and a solution and check whether the solution respects the obligations or not
    """
    for o in os:
        if o.intersection(solution) != set() and o - solution != set() :
            return False
    return True 


def evaluatePIDO(graph, solution):
    """
    take a graph (dictionnary) and a PIDO solution (set of dominants vertices)
    return a tuple of the covered vertices rate, dominants vertices rate (dominants are included in covered) and True if the solution in complet, else False
    """
    vertices = set(graph.keys())
    coveredVertices = set()
    coveredVertices = coveredVertices | solution
    for v in solution:
        coveredVertices = coveredVertices | graph[v]

        coveredRate = len(coveredVertices)/len(vertices) * 100
        dominantRate = len(solution)/len(vertices) * 100
        domination = (coveredRate - dominantRate) / dominantRate

    complet = len(coveredVertices) == len(graph.keys())

    return (coveredRate, dominantRate, domination, complet)


def statisticCompare(n, generator, selectors, ordered = False):
    """
    take a integer n, an instance generator function and a list of obligation selector modes
    Calculate and evaluate a PIDO solution for n instance from the generator with each mode
    return a dictionnary, the keys are modes and values are tuples with average covered vertices rate, dominant vertices rate and dominated vertices peer dominant vertex
    """
    globalMeta = {"n" : n, "vertices" : 0, "obligations" : 0, "minVertices" : 0, "maxVertices" : 0, "minObligations" : 0, "maxObligations" : 0}

    statistics = dict()
    for selector in selectors:
        statistics[selector.__name__] = [0,0,0,0]


    for i in range(n):
        g, os, meta = generator()

        globalMeta["vertices"] += meta["vertices"]
        globalMeta["obligations"] += meta["obligations"]
        globalMeta["type"] = meta["type"]
        if meta["vertices"] > globalMeta["maxVertices"]:
            globalMeta["maxVertices"] = meta["vertices"]
        if meta["vertices"] < globalMeta["minVertices"] or globalMeta["minVertices"] == 0:
            globalMeta["minVertices"]= meta["vertices"]

        if meta["obligations"] > globalMeta["maxObligations"]:
            globalMeta["maxObligations"] = meta["obligations"]
        if meta["obligations"] < globalMeta["minObligations"] or globalMeta["minObligations"] == 0:
            globalMeta["minObligations"]= meta["obligations"]

        for selector in selectors:
            
            if ordered:
                os = obligationsOrder(g, os, selector)
                solution = searchIDO(g, os, nextObligation)
            
            else :
                solution = searchIDO(g, os, selector)
            
            coveredRate, dominantRate, domination, complet = evaluatePIDO(g,solution)
            statistics[selector.__name__][0] += coveredRate
            statistics[selector.__name__][1] += dominantRate
            statistics[selector.__name__][2] += domination
            statistics[selector.__name__][3] += 1 if complet else 0

    for selector in selectors:
        statistics[selector.__name__][0]/=n
        statistics[selector.__name__][1]/=n
        statistics[selector.__name__][2]/=n

        printD(f"Mode {selector.__name__} : covered : {statistics[selector.__name__][0]} , dominants :{statistics[selector.__name__][1]} , domination : {statistics[selector.__name__][2]}, complets : {statistics[selector.__name__][3]}.")

    globalMeta["vertices"] = round(globalMeta["vertices"]/n)
    globalMeta["obligations"] = round(globalMeta["obligations"]/n)

    if ordered:
        globalMeta["type"] = "Ordered " + globalMeta["type"]


    return statistics, globalMeta