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

    return (len(coveredVertices)/len(vertices) * 100, len(solution)/len(vertices) * 100)


def statisticCompare(n, generator):
    """
    take a integer n and an instance generator function
    Calculate and evaluate a PIDO solution for n instance from the generator with each mode
    return a dictionnary, the keys are modes and values are tuples with average covered vertices rate and dominant vertices rate 
    """
    avgCoveredRateLaforest = 0
    avgDominantRateLaforest = 0
    
    avgCoveredRateIzigang = 0
    avgDominantRateIzigang = 0

    avgCoveredRateRandom = 0
    avgDominantRateRandom = 0

    for i in range(n):
        g, os = generator()

        sLaforest = searchIDO(g,os, mode = "Laforest")
        sIzigang = searchIDO(g,os, mode = "IZIGANG")
        sRandom = searchIDO(g,os, mode = "Random")

        coveredRateLaforest,dominantRateLaforest = evaluatePIDO(g, sLaforest)
        coveredRateIzigang,dominantRateIzigang = evaluatePIDO(g, sIzigang)
        coveredRateRandom,dominantRateRandom = evaluatePIDO(g, sRandom)

        avgCoveredRateLaforest += coveredRateLaforest
        avgDominantRateLaforest += dominantRateLaforest

        avgCoveredRateIzigang += coveredRateIzigang
        avgDominantRateIzigang += dominantRateIzigang

        avgCoveredRateRandom += coveredRateRandom
        avgDominantRateRandom += dominantRateRandom

    printD(f"Laforest : {avgCoveredRateLaforest/n}  ({avgDominantRateLaforest/n}) ---- IZIGANG : {avgCoveredRateIzigang/n} ({avgDominantRateIzigang/n})---- Random : {avgCoveredRateRandom/n} ({avgDominantRateRandom/n})")
    statistics = dict()
    statistics["Laforest"] = (avgCoveredRateLaforest/n, avgDominantRateLaforest/n)
    statistics["IZIGANG"] = (avgCoveredRateIzigang/n, avgDominantRateIzigang/n)
    statistics["Random"] = (avgCoveredRateRandom/n, avgDominantRateRandom/n)

    return statistics