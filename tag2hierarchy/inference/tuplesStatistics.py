'''
Created on Mar 11, 2016

@author: cesar
'''

from scipy.special import comb
import operator

#===============================================================================
# Simple Stats
#===============================================================================

def nodesInTuples(setOfTuples):
    """
    Show which nodes appear
    """
    nodesList = []
    for tupl in setOfTuples:
        nodesList.extend(tupl)
    return list(set(nodesList))
#===============================================================================
#  NODES WHICH COOCCUR WITH NODE STATS
#===============================================================================

def cooccuranceBlock(ntupleSet,nodeList):
    """
    Obtains how many different nodes coocuurs as well who coocuur
    this is the main object required for the learning
    """
    nodesPerNode = dict(zip(nodeList,[[] for n in range(len(nodeList))]))
    for ntuple in ntupleSet:
        for nodeInTuple in ntuple:
            nodesPerNode[nodeInTuple].extend(ntuple)
    
    for a,v in nodesPerNode.iteritems():
        differentNodes = set(v).difference(set([a]))
        NumberdifferentNodes = len(differentNodes) 
        nodesPerNode[a] = (NumberdifferentNodes,differentNodes)
    
    return sorted(nodesPerNode.iteritems(),key=operator.itemgetter(1))

def differentNodesForNode(ntupleSet,nodeList,verbose=False):
    """
    For each node obtain the different tuples in which he participates
    
    Parameter:
    ----------
    
    Return:
    -------
    nodesPerNodes dict with the sets of nodes with which the node occurs
    """
    nodesPerNode = dict(zip(nodeList,[[] for n in range(len(nodeList))]))
    for ntuple in ntupleSet:
        for nodeInTuple in ntuple:
            nodesPerNode[nodeInTuple].extend(ntuple)
    
    for a,v in nodesPerNode.iteritems():
        nodesPerNode[a] = set(v)
    
    return nodesPerNode

def numberDifferentNodesForNode(ntupleSet,nodeList,differentNodesPN=None,verbose=False):
    """
    For each node obtain the number of different tuples in which he participates
    
    Parameter:
    ----------
    Return:
    -------
    nNodesPerNode: dict with the number of nodes with which the node co-occurs
    """
    if(differentNodesPN == None):
        differentNodesPN = differentNodesForNode(ntupleSet,nodeList)
    
    numberOfNodesPerNode = {}
    for node, nTupleSet in differentNodesPN.iteritems():
        numberOfNodesPerNode[node] = len(nTupleSet)
        if verbose:
            print "Node {0} has {1} n nodes".format(node,len(nTupleSet)) 
    
    return numberOfNodesPerNode


#===============================================================================
#  TUPLES STATS
#===============================================================================

def differentNTuplesForNode(ntupleSet,nodeList,verbose=False):
    """
    For each node obtain the different tuples in which he participates
    
    Parameter:
    ----------
    
    Return:
    -------
    ntuplesPerNode: dict with the sets of ntuples in which each node occurs
    """
    ntuplesPerNode = dict(zip(nodeList,[[] for n in range(len(nodeList))]))
    for ntuple in ntupleSet:
        ntuple.sort()
        joinedTuple = "".join(ntuple)
        for nodeInTuple in ntuple:
            ntuplesPerNode[nodeInTuple].append(joinedTuple)
    
    for a,v in ntuplesPerNode.iteritems():
        ntuplesPerNode[a] = set(v)
    
    return ntuplesPerNode

def numberDifferentNTuplesForNode(ntupleSet,nodeList,ntuplesPerNode=None,verbose=False):
    """
    
    Parameters:
    ----------
    nTupleSet: list of tuples
    nodeList: list of nodes names
    ntuplesPerNode: dict with the sets of ntuples in which each node occurs
    
    Returns:
    --------
    numberOfnTuplesPerNode: dict of number of different tuples per node
    """
    if(ntuplesPerNode == None):
        ntuplesPerNode = differentNTuplesForNode(ntupleSet,nodeList)
    
    numberOfnTuplesPerNode = {}
    for node, nTupleSet in ntuplesPerNode.iteritems():
        numberOfnTuplesPerNode[node] = len(nTupleSet)
        if verbose:
            print "Node {0} has {1} nTuples".format(node,len(nTupleSet)) 
    
    return numberOfnTuplesPerNode

    
def possibleTuples(nDifferentNodes):
    """
    Calculates the possible number of tuples for a given set of
    
    Parameters:
    ----------
    nDifferentNodes: dictionary with the number of different nodes observed along this node
    
    Returns:
    -------
    numberOfPossibleTuples: dict 
    """
    numberOfPossibleTuples = {}
    for nodeName, numberOfDifferent in nDifferentNodes.iteritems():
        numberOfPossibleTuples[nodeName] = sum([comb(numberOfDifferent,i,exact=True)for i in range(0,4)])
    return numberOfPossibleTuples



def nodesToTuplesRatio(tuples,nodesList):
    """
    """
    nDifferentNTuples =   numberDifferentNTuplesForNode(tuples,nodesList)
    nDifferentNodes = numberDifferentNodesForNode(tuples,nodesList)
    return None