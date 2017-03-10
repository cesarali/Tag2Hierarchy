'''
Created on Mar 11, 2016

@author: cesar
'''
from random import choice,sample
from tag2hierarchy.hierarchy.treeHandlers import nodeNames, transverseTree
from tag2hierarchy.hierarchy import treeHandlers
import numpy as np
import copy

def randomSize(node):
    """
    """
    sizeOfBranch = len(node.myBranch) - 1 #the branch contains the node itself 
    if(sizeOfBranch <= 1):
        return 1
    else:
        return np.random.randint(0,min(4,sizeOfBranch))
    
def generateNTuples(tree,numberOfTuples,nFunction=randomSize,
                    verbose=False,
                    withChildren=(False,0.1,None),
                    horizontalMixing=(False,None,None),
                    withNoise=(False,0.1)):
    """
    For a given number of tuples this algorithm picks any node at random 
    and selects a random Ntuple from the nodes branch, the selection 
    depends on the function defined for nFunction
    
    Parameters:
    -----------
    
    withChildren=(False,0.1,None),
    horizontalMixing=(False,None,None),
    withNoise=(False,0.1)
    
    These are different possibilities of noise in the system
    each ntuple defines in order (Bool (a),Float (b), Int (c))
        (a) The use of the noise
        (b) The percentage of the tuples which are created with the noise
        (c) The number of nodes selected from this sample to be included in the 
            the selection
            
    1. children he selects among the childrens
    2. horizontal mixing he selects nodes at his level
    3. with noise he chooses by random from all nodes above him (all
        siblings of his ascedants)
    
    Parameters:
    -----------
    tree: list of myTree objects
    numberOfTuples: int
    nFunction: function which accepts branch and node to generate
                  the size of the ntuple obtained
    Returns:
    --------
    tupleList
    """
    nodesPerLevel = treeHandlers.obtainNodesPerLevel(tree)
    namesList = nodeNames(tree)
    ntuples = []
    for ik in range(numberOfTuples):
        #TRANSVERSE TREE
        selectedNode = choice(namesList)
        
        if verbose:
            print "Node Selected ",selectedNode
            
        for node in transverseTree(tree):
            myLevel = treeHandlers.obtainMyLevel(node)
            if node.name == selectedNode:
                if verbose:
                    print "Tuple from branch"
                    print node.myBranch
                try:
                    whoToTake = copy.copy(node.myBranch[:-1])
                    if withChildren and node.children != None and node.children != []:
                        if np.random.rand() < withChildren[1]:
                            mySiblings = sample(node.children,min(len(node.children),withChildren[2]))
                            whoToTake.extend(mySiblings)
                    if horizontalMixing[0]:
                        if np.random.rand() < horizontalMixing[1]:
                            neigh= treeHandlers.obtainsNodesAtMyLevel(tree, node.name, nodesPerLevel)
                            whichNeigh = sample(neigh,min(len(neigh,horizontalMixing[2])))
                            whoToTake.extend(whichNeigh)
                    if withNoise[0]:
                        if np.random.rand() < withNoise[1]:
                            nodesAbove = []
                            for l in range(0,myLevel):
                                nodesAbove.extend(nodesPerLevel[l])
                            randomGuys = sample(nodesAbove,withNoise[2])
                    #Here we do the selection
                    ntuple = sample(whoToTake,nFunction(node))
                    ntuple.append(node.name)#you take him for sure
                    ntuples.append(ntuple)
                except:
                    ntuple = [node.name]
                    ntuples.append(ntuple)
                
                break
    return ntuples

