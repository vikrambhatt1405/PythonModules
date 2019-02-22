import networkx as nx
import numpy as np
import logging
import random
import time
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import linalg as LA
from numpy.linalg import LinAlgError
sns.set_style("darkgrid")
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s -%(name)s - %(levelname)s - %(message)s')

"""
Helper class for generating graph object with Erdos-Renyi graph with specififed number of nodes and
probability.Note that the returned graph will have weights on edges randomly distributed.
We manintain a history dictionary which contains algebraic_connectivity for the graph and componets for every change we made to the
graph.
"""

class RandomGraph(object):
    def __init__(self,n_nodes=50,p=0.25,seed=1234):
        self.G=nx.erdos_renyi_graph(n=n_nodes,p=p,seed=seed)
        for edge in self.G.edges():
            self.G[edge[0]][edge[1]]['weight']=np.random.random_sample()
        logging.info("Random graph created with {} nodes".format(self.G.number_of_edges()))
        logging.info('Weights added to the graph succesfully')
        self.history=[]
        self.amends=0
        logging.info("History object created succesfully")

    def __repr__(self):
        return "Number of nodes:{0}\nNumber of edges:{1}\nPartions:{2}\nEigen Values of Laplacian Matrix:\n{3}\n".format(
        self.G.number_of_nodes(),self.G.number_of_edges(),self.partition,self.spectrum)

    def gen_RandomPartitions(self):
        self.partition={}
        self.components={}
        nodes=np.arange(self.G.number_of_nodes())
        np.random.shuffle(nodes)
        component_1=random.sample(list(nodes),self.G.number_of_nodes()//2)
        component_2=np.delete(np.arange(self.G.number_of_nodes()),component_1)
        logging.debug("Size of components:{},{}".format(len(component_1),len(component_2)))
        self.partition[0]=list(component_1)
        self.partition[1]=list(component_2)
        logging.info("Random partition created successfully.")
        self.components[0]=self.G.subgraph(self.partition[0]).copy()
        self.components[1]=self.G.subgraph(self.partition[1]).copy()

    def calculateSpectrum(self):
        self.components_spectrum={}
        self.components_ac={}
        self.spectrum=None
        self.algebraic_connectivity=0
        self.spectrum=nx.laplacian_spectrum(self.G)
        self.algebraic_connectivity=nx.algebraic_connectivity(self.G)
        self.components_spectrum[0]=nx.laplacian_spectrum(self.components[0])
        self.components_spectrum[1]=nx.laplacian_spectrum(self.components[1])
        self.components_ac[0]=nx.algebraic_connectivity(self.components[0])
        self.components_ac[1]=nx.algebraic_connectivity(self.components[1])
        logging.info("Spectrum and algebraic connectivity values calculated.")
        self.history.append([self.algebraic_connectivity,self.components_ac[0],self.components_ac[1]])
        logging.info("Appened to history succesfully.")

    def SwapNodes(self,swapNodes):
        for (nodeX,nodeY) in swapNodes:
            self.amends +=1
            self.partition[0].remove(nodeX)
            self.partition[0].append(nodeY)
            self.partition[1].remove(nodeY)
            self.partition[1].append(nodeX)
            #print(self.partition)
            #time.sleep(20)
            #self.G=nx.relabel_nodes(self.G,
                        #mapping={nodeX:nodeY,nodeY:nodeX})
            self.components[0]=self.G.subgraph(self.partition[0]).copy()
            self.components[1]=self.G.subgraph(self.partition[1]).copy()
            self.spectrum=nx.laplacian_spectrum(self.G)
            self.algebraic_connectivity=nx.algebraic_connectivity(self.G)
            self.components_spectrum[0]=nx.laplacian_spectrum(self.components[0])
            self.components_spectrum[1]=nx.laplacian_spectrum(self.components[1])
            self.components_ac[0]=nx.algebraic_connectivity(self.components[0])
            self.components_ac[1]=nx.algebraic_connectivity(self.components[1])
            self.history.append([self.algebraic_connectivity,self.components_ac[0],self.components_ac[1]])
            logging.info("Changes appended to history succesfully.")

    def showPartitions(self,savefig=False):
        colormap=['green']*self.G.number_of_nodes()
        for node in self.partition[0]:
            colormap[node]='blue'
        options = {
            'node_size': 250,
            'width': 1,'with_labels':True}
        plt.figure(figsize=(12,12))
        plt.subplot(221)
        nx.draw_circular(self.G,**options,node_color=colormap)
        plt.title("Erdos-Renyi graph:Algebraic Connectivity {:.3f}".format(self.algebraic_connectivity))

        plt.subplot(222)
        plt.plot(np.sort(self.spectrum),'g^',label='Graph Spectrum')
        plt.plot(np.sort(self.components_spectrum[0]),'r*',label='Component 1 spectrum')
        plt.plot(np.sort(self.components_spectrum[1]),'b.',label='Component 2 spectrum')
        plt.xlabel('Index')
        plt.ylabel("Eigen Values")
        plt.legend()
        plt.title("Spectrum")

        plt.subplot(223)
        colormap=['blue']*len(self.partition[0])
        nx.draw_circular(self.components[0],node_color=colormap,**options)
        plt.title("Component 1:Algebraic Connectivity {:.3f}".format(self.components_ac[0]))

        plt.subplot(224)
        colormap=['green']*len(self.partition[1])
        nx.draw_circular(self.components[1],node_color=colormap,**options)
        plt.title("Component 2:Algebraic Connectivity {:.3f}".format(self.components_ac[1]))

        if savefig:
            plt.savefig("Erdos-Renyi_"+str(self.amends)+".pdf")
        plt.show()
