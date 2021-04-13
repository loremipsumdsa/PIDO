from PIDO import *
from graphs_generators import *
from visualisation_tools import printD


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

    return (len(coveredVertices)/len(vertices) * 100, len(solution)/len(vertices) * 100, ((len(coveredVertices)- len(solution))/len(vertices) * 100) / (len(solution)/len(vertices) * 100)  )


def statisticCompare(n, generator, modes):
    """
    take a integer n, an instance generator function and a list of obligation selector modes
    Calculate and evaluate a PIDO solution for n instance from the generator with each mode
    return a dictionnary, the keys are modes and values are tuples with average covered vertices rate, dominant vertices rate and dominated vertices peer dominant vertex
    """
    
    statistics = dict()
    for mode in modes:
        statistics[mode] = [0,0,0]


    for i in range(n):
        g, os = generator()

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

    return statistics