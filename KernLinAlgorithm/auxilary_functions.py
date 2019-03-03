import networkx as nx
import numpy as np
import random
import networkx as nx
from random_graph import *
import sys
import logging
import operator
import queue
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


def getMaxGainNodes(randomGraph, selectedNodesSet):
    """
    selectedNodes is set of nodes already selected and will not be considered in swapping.
    Returns maximum gain for the current partition and corresponding swap nodes as defined below.
    Kernighan, B. W., & Lin, S. (1970). An Efficient Heuristic Procedure for Partitioning Graphs.
    Bell System Technical Journal, 49(2), 291–307. https://doi.org/10.1002/j.1538-7305.1970.tb01770.x
    """
    maxGain = -sys.maxsize
    D = randomGraph.totalCost()
    C = nx.adjacency_matrix(randomGraph.G)
    maxGain = -sys.maxsize
    for i in set(randomGraph.partition[0]).difference(selectedNodesSet):
        for j in set(randomGraph.partition[1]).difference(selectedNodesSet):
            gain = D[i]+D[j]-2*C[i,j]
            if(maxGain < gain):
                maxGain = gain
                targetNodes = (i,j)
    return maxGain,targetNodes

def showPlots(randomGraph,k,partialGainSums, savefigures=False):
    fig, (axis1, axis2) =  plt.subplots(1,2,figsize=[5,5])
    history = np.array(randomGraph.history, dtype=np.float)
    axis1.plot(history[:, 0], ":r*", label='Component 0')
    axis1.plot(history[:, 1], ":g^", label='Component 1')
    axis1.axvline(k, color='b', label= 'Optimal Swaps')
    axis1.set_title("Variations of albegraic connectivity")
    axis1.set_xlabel("Number of swaps")
    axis1.set_ylabel("Algebraic Connectivity")
    axis1.legend()

    axis2.plot(partialGainSums,":g*")
    axis2.axvline(k,color='b',label='Max gain at swap {}'.format(k),linestyle=":")
    axis2.set_xlabel("Number of swaps")
    axis2.set_ylabel("Gain")
    axis2.legend()

    plt.show()
    if savefigures:
        fig.savefig("results.pdf")
