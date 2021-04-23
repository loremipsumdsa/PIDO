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


#Solution evaluation function
def evaluatePIDO(graph, solution):
    """
    take a graph (dictionnary) and a PIDO solution (set of dominants vertices)
    return a tuple of the covered vertices rate and dominants vertices rate (dominants are included in covered)
    """
    vertices = set(graph.keys())
    coveredVertices = set()
    coveredVertices = coveredVertices | solution
    for v in solution:
        coveredVertices = coveredVertices | graph[v]

        coveredRate = len(coveredVertices)/len(vertices) * 100
        dominantRate = len(solution)/len(vertices) * 100
        domination = (coveredRate - dominantRate) / dominantRate

    return (coveredRate, dominantRate, domination)


def statisticCompare(n, generator, modes):
    """
    take a integer n, an instance generator function and a list of obligation selector modes
    Calculate and evaluate a PIDO solution for n instance from the generator with each mode
    return a dictionnary, the keys are modes and values are tuples with average covered vertices rate, dominant vertices rate and dominated vertices peer dominant vertex
    """
    globalMeta = {"n" : n, "vertices" : 0, "obligations" : 0, "minVertices" : 0, "maxVertices" : 0, "minObligations" : 0, "maxObligations" : 0}

    statistics = dict()
    for mode in modes:
        statistics[mode] = [0,0,0]


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

        for mode in modes:
            solution = searchIDO(g,os, mode = mode)
            coveredRate, dominantRate, domination = evaluatePIDO(g,solution)
            statistics[mode][0] += coveredRate
            statistics[mode][1] += dominantRate
            statistics[mode][2] += domination

    for mode in modes:
        statistics[mode][0]/=n
        statistics[mode][1]/=n
        statistics[mode][2]/=n

        printD(f"Mode {mode} : covered : {statistics[mode][0]} , dominants :{statistics[mode][1]} , domination : {statistics[mode][2]}.")

    globalMeta["vertices"] = round(globalMeta["vertices"]/n)
    globalMeta["obligations"] = round(globalMeta["obligations"]/n)



    return statistics, globalMeta