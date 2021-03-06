from graphviz import Graph
import matplotlib.pyplot as plt
from random import randint, choice
import os

DOMINANT_COLOR = "#44cc00"
DOMNINATED_COLOR = "#66ccff"
SAVE_PATH = "visualisation_results/"

def randomColor():
    """
    return a random color (hexa code)
    """
    r = lambda: randint(0,255)
    return('#%02X%02X%02X' % (r(),r(),r()))


# Debug tools
DEBUGMODE = False
WARNINGMODE = False

def printD(message):
    """
    print message if DebugMode
    """
    if DEBUGMODE:
        print(message)

def printW(message):
    """
    print message if WARNINGMODE
    """
    if WARNINGMODE:
        print(message)

def printInstance(graph, obligationSet):
    """
    Take an instance : a graph (dictionnary) and an obligation set
    print the number of vertices and the number of obligations
    """
    print("------- INSTANCE -----------")
    print(f"Number of vertices : {len(graph.keys())}")
    print(f"Number of obligation : {len(obligationSet)}")

    print("\n")


def printResult(graph, obligationSet, solution, coveredVertices, dominantVertices):
    print("------- INSTANCE -----------")
    print(f"Number of vertices : {len(graph.keys())}")
    print(f"Number of obligation : {len(obligationSet)}")

    print("------- RESULT -----------")
    print("Dominating Vertices", end = " : ")
    for v in solution:
        print(v, end = ", ")


    print("\nSolution's evaluation :")
    print(f"    Covered vertices rate : {coveredVertices} %")
    print(f"    Dominating vertices rate : {dominantVertices} %")

    print("\n")


def graphs_visualisation(graph, obligationSet, solution, title = "new_graph_view", view = False, save = True):
    """
    Take an instance : a graph (dictionnary) and an obligation set, a PIDO solution (set of vertices) and a title
    Generate a graphic representation of the graph and the solution
    print it if view, save it if save (the name of the file will be the title)
    """
    includedEdges = set()
    includedVertices = dict()

    verticesColor  = dict()

    for obligation in obligationSet:
        obligationColor = randomColor()
        for vertex in obligation:
            verticesColor[vertex] = obligationColor

    for vertex in graph.keys():
        includedVertices[vertex] = False

    g = Graph('G', filename=SAVE_PATH + title+'.gv', engine='sfdp')

    for vertex in solution:
        g.node(str(vertex), fillcolor = DOMINANT_COLOR, style = "filled", color = verticesColor[vertex], penwidth = "2")
        includedVertices[vertex] = True
        
        for neihbourg in graph[vertex]:
            g.node(str(neihbourg), fillcolor = DOMNINATED_COLOR, style = "filled", color = verticesColor[neihbourg], penwidth = "2")
            includedVertices[neihbourg] = True

        for vertex in graph.keys():
            if not(includedVertices[vertex]):
                g.node(str(vertex), fillcolor = "white", style = "filled", color = verticesColor[vertex], penwidth = "2")
                includedVertices[vertex] = True

    for vertex in graph.keys():
        for neihbourg in graph[vertex]:
            if not((vertex,neihbourg) in includedEdges):
                g.edge(str(vertex), str(neihbourg))
                includedEdges.add((vertex,neihbourg))
                includedEdges.add((neihbourg,vertex))


    g.render(SAVE_PATH+title+".gv", view=view)

    if not(save):
        print("unsave")
        os.remove(SAVE_PATH + title+".gv")
        os.remove(SAVE_PATH + title+".gv.pdf")



def statisticsVisualisation(statistics, meta, view = False, save = True):
    """
    Take a statistic report and a meta dictionnary generated by the statisticCompare function
    create a graphical representation of theses statistics, set the title according to the meta
    print it if view, save it if save
    """
    
    mainTitle = "PIDO results on "+ str(meta["n"]) + " "+ meta["type"] + " instances" 
    subTitle= "\n" + "vertices : " + "-" + str(meta["minVertices"]) + " +" + str(meta["maxVertices"]) + " ~" + str(meta["vertices"])
    subTitle += "\n" + "obligations : " + "-" + str(meta["minObligations"]) + " +" + str(meta["maxObligations"]) + " ~" + str(meta["obligations"])
    title = mainTitle + subTitle
    width = 0.8
    y1 = []
    y2 = []
    labels = []
    x = range(len(statistics.keys()))

    for k in statistics.keys():
        y2.append(int(statistics[k][0] - statistics[k][1]))
        y1.append(int(statistics[k][1]))
        labels.append(k)

    plt.bar(labels, y1, width = width, color = DOMINANT_COLOR, label = "Dominant Vertices")
    plt.bar(labels, y2, width = width, bottom = y1, color = DOMNINATED_COLOR, label = "Dominated Vertices")
    plt.title(title)
    plt.ylabel("Vertices rate (%)")
    #plt.legend(loc = "upper left")


    for bar in labels:
        plt.text(bar, statistics[bar][1]/2, str(round(statistics[bar][1],1))+"%", color='black', fontweight='light', fontsize = "large")
        plt.text(bar, (statistics[bar][1]+statistics[bar][0])/2, str(round(statistics[bar][0],1))+"%", color='black', fontweight='light', fontsize = "large")
        plt.text(bar, (statistics[bar][0]), "("+str(round(statistics[bar][2],1))+"| "+str(statistics[bar][3])+")", color='black', fontweight='bold', fontsize = "small")

    
    if view:
        plt.show()

    if save:
        fig = plt.gcf()
        fig.set_size_inches((14, 11), forward=False)
        fig.savefig(SAVE_PATH + mainTitle, dpi=500)

    plt.clf()