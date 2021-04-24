from PIDO import *
from visualisation_tools import *
from evaluation import *
from graphs_generators import *
#from graphs_generators2 import *
import matplotlib.pyplot as plt
import time


def recevability_test():
    """
    A lot of tests to check if the solutions produced by the algorithms are recevables
    if an error occurred, print the failling mode and continue
    """
    for i in range(1000):
        g,os,meta = instanceGeneratorFullRandom()
        s = searchIDO(g,os,"Size")

        if not(checkSolution(os,s)):
            print("Error found on Size mode")

    for i in range(1000):
        g,os,meta = instanceGeneratorFullRandom()
        s = searchIDO(g,os,"Dominant")

        if not(checkSolution(os,s)):
            print("Error found on Dominant mode")

    for i in range(1000):
        g,os,meta = instanceGeneratorFullRandom()
        s = searchIDO(g,os,"Covering")

        if not(checkSolution(os,s)):
            print("Error found on Covering mode")

    for i in range(1000):
        g,os,meta = instanceGeneratorFullRandom()
        s = searchIDO(g,os,"Dominating")

        if not(checkSolution(os,s)):
            print("Error found on Dominating mode")

    for i in range(1000):
        g,os,meta = instanceGeneratorFullRandom()
        s = searchIDO(g,os,"Random")

        if not(checkSolution(os,s)):
            print("Error found on Random mode")


def ultimateTest(n, generators, modes):
    for generator in generators:
            statistics, meta = statisticCompare(n, generator, modes)
            statisticsVisualisation(statistics, meta, view = False, save = True)

def ultimateTestO(n, generators, modes):
    for generator in generators:
            statistics, meta = statisticCompare(n, generator, modes, ordered = True)
            statisticsVisualisation(statistics, meta, view = False, save = True)
    
def main():

    #recevability_test()

    # selectors = [biggestObligation, mostDominantObligation, mostCoveringObligation, mostDominatingObligation, randomObligation]
    # s, m = statisticCompare(10000,instanceGenerator,selectors)
    # statisticsVisualisation(s,m)

    # s, m = statisticCompare(10000,instanceGenerator,selectors, ordered = True)
    # statisticsVisualisation(s,m)

    #g,os, m = instanceGeneratorHypercube()
    #s = searchIDO(g,os,biggestObligation)
    #graphs_visualisation(g,os,s,view = True, save = True)


    generators = [instanceGenerator, instanceGeneratorConnexe, instanceGeneratorComplete_graph, instanceGeneratorGrid_graph, instanceGeneratorTorus_graph, instanceGeneratorHypercube, instanceGeneratorFullRandom]
    selectors = [biggestObligation, mostDominantObligation, mostCoveringObligation, mostDominatingObligation, randomObligation]
    #ultimateTest(10000, generators , modes)


    #ultimateTest(30_000, generators, selectors)# <---------- P A U L

    #ultimateTestO(30_000, generators, selectors)  # <---------- T H O M A S

main()