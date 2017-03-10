'''
Created on May 25, 2016

@author: cesar
'''
import json
import sys
from tag2hierarchy.hierarchy.ObjectTreeHandlers import transverseTree, nodeNames, obtainLeavesFromNode, obtainNonLeaves
import numpy as np

def purityFromGroundTruth(groundTree, trainedTree, verbose=False):
    """
    Obtains the purity by cheking the average fraction of common leaves 
    from all nonleaves nodes in the ground true hierarchy
    
    Parameters
    ----------
    groundTree: list of myTree objects accounting for the original tree
    trainedTree: list of myTree objects accounting for the tree created 
    out of the tuple occurrances and our algorithm
    
    Returns
    -------
    purityValue: float
    """
    nonLeaves = obtainNonLeaves(groundTree)
    averagePurity = 0.
    numberOfLeaves = len(nonLeaves)
    for nonLeafNode in nonLeaves:
        groundTruthLeaves = obtainLeavesFromNode(groundTree, nonLeafNode)
        trainedLeaves = obtainLeavesFromNode(trainedTree, nonLeafNode)
        
        purity = len(set(groundTruthLeaves).intersection(set(trainedLeaves))) / len(set(groundTruthLeaves))
        if verbose == True:
            if purity == 1.:
                print nonLeafNode
        averagePurity += purity     
    return averagePurity / float(numberOfLeaves)

def blockCoocurrances(Block, numberOfTags=100):
    """
    Obtains the coocurrance matrix of the tags which coocur with each tag
    
    Parameters
    ----------
    Block : (tag1,(N coocurrance tags, set([tag1,tag2,tag3,tag4,...])),
            (tag2,(M coocurrance tags, set([tag1,tag2,tag3,tag4,...]))
    
    Returns
    -------
    Coocurance matrix
    """
    listOfNodes = []
    numberOfNodes = len(Block[:numberOfTags])
    coocurranceMatrix = np.zeros((numberOfNodes, numberOfNodes))
    for i in range(numberOfNodes):
        listOfNodes.append(Block[:numberOfTags][i][0])
        for j in range(numberOfNodes):
            coocurranceMatrix[i, j] = len(Block[i][1][1].intersection(Block[j][1][1])) / float(len(Block[i][1][1].union(Block[j][1][1])))
    return coocurranceMatrix, listOfNodes 
