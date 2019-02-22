import networkx as nx
import numpy as np
import random
from random_graph import *
import sys
import logging
import operator

logging.basicConfig(filename='erros.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.WARNING)
"""
PartitionID is just unique index for each partiton.For two partitions partitionID are just 0,1 only
"""
def minimum_EdgeWeights_Node(randomGraph,partitionId):
    if randomGraph.partition is None:
        logging.error("Partitions must be done before calling this function.")
    min_weight=sys.maxsize
    minweight_node=0
    for node in randomGraph.partition[partitionId]:
        sum_weights=0
        for neighbor in randomGraph.G[node]:
            sum_weights += randomGraph.G[node][neighbor]['weight']
        if(sum_weights<min_weight):
            minweight_node=node
    return  partitionId,minweight_node


#get_ExternalNeighbors reutrns a list of all neighbors in external component
def getExternalNeighbors(randomGraph,nodeId):
    if nodeId in randomGraph.partition[0]:
        external_partitionID=1
    else:
        external_partitionID=0
    neighbors=set(randomGraph.G[nodeId].keys())
    externalNeighbors= set(randomGraph.partition[external_partitionID])
    externalNeighbors= list(externalNeighbors.intersection(neighbors))
    return externalNeighbors

def getInternalNeighbors(randomGraph,nodeId):
    if nodeId in randomGraph.partition[0]:
        internal_partitionID=0
    else:
        internal_partitionID=1
    neighbors=set(randomGraph.G[nodeId].keys())
    internalNeighbors=set(randomGraph.partition[internal_partitionID])
    internalNeighbors=list(internalNeighbors.intersection(neighbors))
    return internalNeighbors

def externalCost(randomGraph,nodeId):
    externalNeighbors=getExternalNeighbors(randomGraph,nodeId)
    cost=0
    for neighbor in externalNeighbors:
        cost+=randomGraph.G[nodeId][neighbor]['weight']
    return cost

def internalCost(randomGraph,nodeId):
    internalNeighbors=getInternalNeighbors(randomGraph,nodeId)
    cost=0
    for neighbor in internalNeighbors:
        cost+=randomGraph.G[nodeId][neighbor]['weight']
    return cost

def getSwapNodes(randomGraph):
    visitedNodes=set()
    swapNodes=[] #swap nodes in list of tuples of nodes maintained in the same order as they are found.
    for i in range(len(randomGraph.partition[0])):
        maxCost=-sys.maxsize
        targetNodes=[]
        for node in set(randomGraph.partition[0]).difference(visitedNodes):
            totalCost=externalCost(randomGraph,node)-internalCost(randomGraph,node)
            if(totalCost>maxCost):
                targetNode=node
        targetNodes.append(targetNode)
        maxCost=-sys.maxsize
        for node in set(randomGraph.partition[1]).difference(visitedNodes):
            totalCost=externalCost(randomGraph,node)-internalCost(randomGraph,node)
            if(totalCost>maxCost):
                targetNode=node
        targetNodes.append(targetNode)
        visitedNodes.update(targetNodes)
        swapNodes.append(tuple(targetNodes))
    return swapNodes
