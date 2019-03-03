import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from random_graph import RandomGraph
from auxilary_functions import *
import queue
sns.set_style("darkgrid")
"""
Don't worry about these line if you don't understand what they are doing.Just some helper functions for better
debugging experience.
"""

parser = ArgumentParser("CapsE", formatter_class=ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
logging.basicConfig(filename='errors.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
parser.add_argument("--savefigures", action='store_true', help='Specfiy if you want to save figures')
parser.add_argument("--nodes", default=50, type=int, help="Number of nodes in Erdos-Renyi Graph")
parser.add_argument("--p", default=0.25, type=float, help="Probability of edge being present in Erdos-Renyl Graph")
args = parser.parse_args()

def showPlots(randomGraph,k,partialGainSums):
    fig, (axis1, axis2) =  plt.subplots(1,2,figsize=[5,5])
    history = np.array(randomGraph.history, dtype=np.float)
    axis1.plot(history[:, 0], ":r*", label='Component 0')
    axis1.plot(history[:, 1], ":g^", label='Component 1')
    axis1.axvline(k, color='b', label= 'Optimal Swaps')
    axis1.set_title("Variations of albegriac connectivity during swapping")
    axis1.set_xlabel("Number of swaps")
    axis1.set_ylabel("Algebraic Connectivity")
    axis1.legend()

    axis2.plot(partialGainSums,":g*")
    axis2.axvline(k,color='b',label='Max gain at swap {}'.format(k),linestyle=":")
    axis2.set_xlabel("Number of swaps")
    axis2.set_ylabel("Gain")
    axis2.legend()
    
    plt.show()
    if args.savefigures:
        fig.savefig("results.pdf")


if __name__ == "__main__":
    randomGraph = RandomGraph(n_nodes=args.nodes, p=args.p)
    randomGraph.genRandomPartitions()
    randomGraph.calculateSpectrum()
    selectedNodes = queue.Queue(randomGraph.G.number_of_nodes()//2)
    selectedNodesSet = set()
    gainList = np.array([],dtype=np.float32)
    totalGain = 0
    while(len(selectedNodesSet) < randomGraph.G.number_of_nodes()):
        gain,(nodeX,nodeY) = getMaxGainNodes(randomGraph,selectedNodesSet)
        randomGraph.swapNodes(nodeX, nodeY,True)
        totalGain += gain
        gainList=np.append(gainList,gain)
        selectedNodesSet.add(nodeX)
        selectedNodesSet.add(nodeY)
        selectedNodes.put((nodeX,nodeY))
    assert np.isclose(totalGain,0), "Total Gain is not zero"
    del totalGain
    partialGainSums = [np.sum(gainList[:index]) for index,_ in enumerate(gainList)]
    k=np.argmax(partialGainSums)
    showPlots(randomGraph,k,partialGainSums)
