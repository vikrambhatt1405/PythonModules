import networkx as nx
import numpy as np
import random
from random_graph import *
import sys
import logging
import operator
errors.log
logging.basicConfig(filename='errors.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)

def showPartitions(randomGraph, savefig=False):
    colormap = ['green'] * randomGraph.G.number_of_nodes()
    for node in randomGraph.partition[0]:
        colormap[node] = 'blue'
    options = {'node_size': 250,'width': 1, 'with_labels': True}
    plt.figure(figsize=(12, 12))
    plt.subplot(221)
    nx.draw_circular(randomGraph.G, **options, node_color=colormap)
    plt.title("Erdos-Renyi graph:Algebraic Connectivity {:.3f}".format(randomGraph.algebraic_connectivity))

    plt.subplot(222)
    plt.plot(np.sort(randomGraph.spectrum), 'g^', label='Graph Spectrum')
    plt.plot(np.sort(randomGraph.components_spectrum[0]), 'r*', label='Component 1 spectrum')
    plt.plot(np.sort(randomGraph.components_spectrum[1]), 'b.', label='Component 2 spectrum')
    plt.xlabel('Index')
    plt.ylabel("Eigen Values")
    plt.legend()
    plt.title("Spectrum")

    plt.subplot(223)
    colormap = ['blue'] * len(randomGraph.partition[0])
    nx.draw_circular(randomGraph.components[0], node_color=colormap, **options)
    plt.title("Component 1:Algebraic Connectivity {:.3f}".format(randomGraph.components_ac[0]))

    plt.subplot(224)
    colormap = ['green'] * len(randomGraph.partition[1])
    nx.draw_circular(randomGraph.components[1], node_color=colormap, **options)
    plt.title("Component 2:Algebraic Connectivity {:.3f}".format(randomGraph.components_ac[1]))

    if savefig:
        plt.savefig("Erdos-Renyi_" + str(randomGraph.amends) + ".pdf")
    plt.show()

def maxGainNodes(randomGraph, D, xPartition, yPartition, xNode, yNode):
    """
    Return two nodes which maximize the gain as defined in Kerningham Lin Algorithm.
    D is list of external-internal cost for all nodes calculated for the previous partitions before swapping.
    xPartition is set of current nodes in first components
    yPartition is set of current nodes in second componets
    xSelected is list of selected indices in xPartition for the swapping
    ySelected is list of selected indices in yPartition for the swapping
    """
    maxGain = -sys.maxsize
    # D represents external cost-internal cost for all nodes. Following the notation from
    # Kernighan, B. W., & Lin, S. (1970). An Efficient Heuristic Procedure for Partitioning Graphs.
    # Bell System Technical Journal, 49(2), 291–307. https://doi.org/10.1002/j.1538-7305.1970.tb01770.x
    for i in randomGraph.G.nodes():
        D.append(randomGraph.externalCost(i)-randomGraph.internalCost(i))
        targetNodes = None
    for xNode in xPartition:
        for yNode in yPartition:
            gain = D[x]+D[y]-2*randomGraph.G[xNode][yNode]['weight']
            if(maxGain < gain):
                targetNodes = (xNode,yNode)

def getSwapNodes(randomGraph):
    visitedNodes = set()
    swapNodes = []  # swap nodes in list of tuples of nodes maintained in the same order as they are found.
    for i in randomGraph.G.nodes():
        totalCosts = []
        totalCosts.append(randomGraph.externalCost(i)-randomGraph.internalCost(i))
