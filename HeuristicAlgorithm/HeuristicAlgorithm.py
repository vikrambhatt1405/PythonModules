import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from random_graph import RandomGraph
from auxilary_functions import *

"""
Don't worry about these lines if you don't understand what they are doing.Just some helper functions for better
debugging experience.
"""

parser = ArgumentParser("CapsE", formatter_class=ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
logging.basicConfig(filename='errors.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.WARNING)
parser.add_argument("--savefigures",action='store_true',help='Specfiy if you want to save figures')
parser.add_argument("--nodes",default=50,type=int,help="Number of nodes in Erdos-Renyi Graph")
parser.add_argument("--p",default=0.25,type=float,help="Probability of edge being present in Erdos-Renyl Graph")
parser.add_argument("--n_iter",default=1000,type=int,help="Number of iterations for simulation to run")
args=parser.parse_args()


if __name__ == "__main__":
    randomGraph=RandomGraph(n_nodes=args.nodes,p=args.p)
    randomGraph.gen_RandomPartitions()
    randomGraph.calculateSpectrum()
    randomGraph.showPartitions(args.savefigures)
    randomGraph.SwapNodes(getSwapNodes(randomGraph))

    fig, [[axis1, axis2],[axis3, axis4]]=plt.subplots(2,2,figsize=(16,16))
    history=np.array(randomGraph.history,dtype=np.float)
    axis1.plot(history[1:,1],":r*",label='Component 0')
    axis1.axhline(y=history[0][1],color='r',label='Initial value(Component 0)',linestyle="-")
    axis1.plot(history[1:,2],":g^",label='Component 1')
    axis1.axhline(y=history[0][2],color='g',label='Initial value(Component 1)',linestyle="-")
    axis1.set_title("Variations of eigenvalues during swapping")
    axis1.set_xlabel("Number of swaps")
    axis1.set_ylabel("Algebraic Connectivity")
    axis1.legend()

    change_ac=(history[1:,1:]-history[0,1:])/history[0,1:]
    axis2.plot(change_ac[:,0],":r*",label='Component 0')
    axis2.plot(change_ac[:,1],":g^",label='Component 1')
    axis2.set_title("Fraction of change in Fiedler values after each swap")
    axis2.set_xlabel("Swaps")
    axis2.set_ylabel("Algebraic Connectivity")
    axis2.legend()

    axis3.plot(change_ac[:,0]+change_ac[:,1],"--g.",label='Total Change')
    xmax=np.argmax(change_ac[:,0]+change_ac[:,1])
    ymax=np.max(change_ac[:,0]+change_ac[:,1])
    axis3.plot(xmax,ymax,"bH",markersize=10,label='Max Value')
    axis3.axvline(xmax,color='b')
    axis3.set_title("Total fractional  change in Fiedler values for both components")
    axis3.set_xlabel("Swaps")
    axis3.set_ylabel("Algebraic Connectivity")
    x_ticks=np.append(axis3.get_xticks(),xmax)
    axis3.set_xticks(x_ticks)
    axis3.legend()

    axis4.boxplot(change_ac)
    axis4.set_xticklabels(["Component0","Component1"])
    axis4.set_ylabel("Fraction of change w.r.t initial value")
    axis4.set_title("Variations of Feidler values for each components")
    axis4.legend()

    plt.show()
    if args.savefigures:
        fig.savefig("results.pdf")
