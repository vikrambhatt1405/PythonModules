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

if __name__ == "__main__":
    randomGraph = RandomGraph(n_nodes=args.nodes, p=args.p)
    randomGraph.genRandomPartitions()
    randomGraph.calculateSpectrum()
    if args.savefigures:
        showPartitions(randomGraph,args.savefigures)
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
    showPlots(randomGraph,k,partialGainSums,args.savefigures)
