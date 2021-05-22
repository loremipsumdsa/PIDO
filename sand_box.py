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

    
    generators = [instanceGenerator, instanceGeneratorConnexe, instanceGeneratorComplete_graph, instanceGeneratorGrid_graph, instanceGeneratorTorus_graph, instanceGeneratorHypercube, instanceGeneratorFullRandom]
    selectors = [biggestObligation, mostDominantObligation, mostCoveringObligation, mostDominatingObligation, randomObligation]

    #recevability_test()

    #g,os, m = instanceFromFile("graph_in_file_example")
    
    # g,os, m = instanceGeneratorTorus_graph()
    # s = searchIDO(g,os,mostCoveringObligation)
    # graphs_visualisation(g,os,s,view = False, save = True)


    # ultimateTest(30_000, generators, selectors)# <---------- P A U L

    # ultimateTestO(100, generators, selectors)  # <---------- T H O M A S

main()