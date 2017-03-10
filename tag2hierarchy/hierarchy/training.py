'''
Created on Mar 11, 2016

@author: cesar
'''

from tag2hierarchy.datatypes.hierarchies import Node
from tag2hierarchy.hierarchy.tuplesStatistics import cooccuranceBlock,nodesInTuples
from tag2hierarchy.hierarchy.TupleGenerator import generateNTuples
from tag2hierarchy.hierarchy.treeHandlers import nodeNames, setBranch, obtainDescendantsFromNode, obtainDescendantsFromNode2

def initialize(tupleSet):
    """
    Obtain the initial structures needed for the 
    tuplesToTree algorithm
    
    Return:
    ------
    nodesList,Block,nodesObjectList
    """
    #tupleSet = set(tupleSet)
    nodesList = nodesInTuples(tupleSet)
    Block = cooccuranceBlock(tupleSet, nodesList)[::-1]
    nodesObjectList = [Node(name[0],[],cargo=i) for i,name in enumerate(Block)]
    
    return nodesList,Block,nodesObjectList

def obtainTree(tupleSet,verbose=False):
    """
    This algorithms aims at obtaining a tree structure from a set of tuples
    if follows:
        1. Obtain all nodes in the list of tuples
        2. Initialize NodeList: this list contains all the nodes with empty children
        While len(NodeList) > 1:
            take smallest node in cooccurance block
                insert this node as a children in the next node in the block which contains the selected node as coocurring
    """    
    nodesList,Block,nodesObjectList = initialize(tupleSet)
    if verbose:
        print "Number of nodes: ",len(nodesList)
        
    while(len(Block) > 1):
        smallestNodeBlock = Block.pop()
        smallestNode = nodesObjectList.pop()
        for block, node in zip(Block[::-1],nodesObjectList[::-1]):
            if verbose:
                print  "Looking for parent of {0}".format(smallestNode.name)
            if smallestNode.name in block[1][1]:
                if verbose:
                    print "Inserting node {0} in node {1}".format(smallestNode.name,node.name)
                if smallestNode.children == []:
                    smallestNode.name
                    smallestNode.children = None
                node.children.append(smallestNode)
                break
        
    return nodesObjectList

def obtainParentToDescendantsRatio(smallestNode,node,Block):
    """
    Obtains how many of the descendants of a given node to merge coccur with the parent to insert
    
    """
    blockPlacesOfDescendants = obtainDescendantsFromNode2([smallestNode],smallestNode.name,cargo=True)
    parentToDescendants = 0.
    for b in blockPlacesOfDescendants:
        if node.name in Block[b][1][1]:
            parentToDescendants += 1.
    parentToDescendants = parentToDescendants/len(blockPlacesOfDescendants)
    return  parentToDescendants
                
def obtainTreeNoise(tupleSet,parentToDescendantBound=0.4,verbose=False):
    """
    This algorithms aims at obtaining a tree structure from a set of tuples
    if follows:
        1. Obtain all nodes in the list of tuples
        2. Initialize NodeList: this list contains all the nodes with empty children
        While len(NodeList) > 1:
            take smallest node in cooccurance block
                insert this node as a children in the next node in the block which contains the selected node as coocurring
        3. Upon mergin it checks that the parent also coocurs with the children
    """    
    nodesList,Block,nodesObjectList = initialize(tupleSet)
    if verbose:
        print "Number of nodes: ",len(nodesList)
    
    parentToDescendantStats = []
    k = len(Block) - 1 
    while(k >=0):
        smallestNodeBlock = Block[k]
        smallestNode = nodesObjectList[k]
        
        backCount = 0
        included = False
        bestParentToDescendant = 0.
        smallestFound = None
        for block, node in zip(Block[:k][::-1],nodesObjectList[:k][::-1]):
            if verbose:
                print  "Looking for parent of {0}".format(smallestNode.name)
                
            if smallestNode.name in block[1][1]:
                #CHECK COOCURRANCE OF THIS CHILDREN NODES WITH THE PARENT
                parentToDescendants = obtainParentToDescendantsRatio(smallestNode,node,Block)
                parentToDescendantStats.append(parentToDescendants)
                
                if parentToDescendants > parentToDescendantBound:
                    if verbose:
                        print "Inserting node {0} in node {1}".format(smallestNode.name,node.name)
                    if smallestNode.children == []:
                        smallestNode.name
                        smallestNode.children = None
                    node.children.append(smallestNode) #Here is where we make the insertion
                    included = True
                    break
                else:
                    if parentToDescendants > bestParentToDescendant:
                        smallestFound = backCount
                        bestParentToDescendant = parentToDescendants
                        
            backCount +=1 # index to follow the possible parents
        
        if not included and smallestFound != None:
            blockSection = Block[:k][::-1][smallestFound]
            node = nodesObjectList[:k][::-1][smallestFound]
        k-=1
    return [nodesObjectList[0]], parentToDescendantStats


def obtainTreeNoise2(tupleSet,parentToDescendantBound=0.4,verbose=False):
    """
    This algorithms aims at obtaining a tree structure from a set of tuples
    if follows:
        1. Obtain all nodes in the list of tuples
        2. Initialize NodeList: this list contains all the nodes with empty children
        While len(NodeList) > 1:
            take smallest node in cooccurance block
                insert this node as a children in the next node in the block which contains the selected node as coocurring
        3. Upon mergin it checks that the parent also coocurs with the children
    """    
    nodesList,Block,nodesObjectList = initialize(tupleSet)
    if verbose:
        print "Number of nodes: ",len(nodesList)
    
    rootsSet = []
    parentToDescendantStats = []
    bestParentToDescendantStats = []
    k = len(Block) - 1 
    while(k >=0):
        smallestNodeBlock = Block[k]
        smallestNode = nodesObjectList[k]
        
        bestParentToDescendant = 0.
        for j,block, node in zip(range(len(Block[:k][::-1])),Block[:k][::-1],nodesObjectList[:k][::-1]):
            if verbose:
                print  "Looking for parent of {0}".format(smallestNode.name)
                
            if smallestNode.name in block[1][1]:
                #CHECK COOCURRANCE OF THIS CHILDREN NODES WITH THE PARENT
                parentToDescendants = obtainParentToDescendantsRatio(smallestNode,node,Block)
                parentToDescendantStats.append(parentToDescendants)
                
                if parentToDescendants > bestParentToDescendant:
                    bestParentToDescendant = parentToDescendants
                    bestIndexFound = j
        
        bestParentToDescendantStats.append(bestParentToDescendant)
        if bestParentToDescendant > parentToDescendantBound:
            if verbose:
                print "Inserting node {0} in node {1}".format(smallestNode.name,node.name)
            if smallestNode.children == []:
                smallestNode.name
                smallestNode.children = None
            node = nodesObjectList[:k][::-1][bestIndexFound]
            node.children.append(smallestNode) #Here is where we make the insertion
        else:
           rootsSet.append(k) 
        k-=1
    
    allTrees = []
    homeless = []
    for k in rootsSet:
        rootNode = nodesObjectList[k]
        if rootNode.children == []:
            homeless.append(rootNode.name)
        else:
            allTrees.append(rootNode)
             
    return allTrees,homeless, parentToDescendantStats, bestParentToDescendantStats

def treeToTupleAndBack(objectTree,numberOfTuples):
    """
    This generates tuples from a tree and then trains from those tuples 
    
    """
    tupleSet = generateNTuples(objectTree,numberOfTuples)
    return obtainTree(tupleSet)
    
def calculatePurity(truthTree,trainedTree,setTheBranches=True):
    """
    """
    if setTheBranches:
        setBranch(truthTree)
        setBranch(trainedTree)
    
