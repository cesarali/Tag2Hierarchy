'''
Created on Mar 11, 2016

@author: cesar
'''
from tag2hierarchy.datatypes.hierarchies import Node  
from tag2hierarchy.hierarchy.ObjectTreeHandlers import transverseTree, setBranch
from tag2hierarchy.hierarchy.TupleGenerator import generateNTuples
from tag2hierarchy.hierarchy.structureTest import purityFromGroundTruth
from tag2hierarchy.hierarchy.training import obtainTreeNoise2
import numpy as np


def simpleBifurcation(bifurgationArguments):
    """
    """
    return np.random.randint(*bifurgationArguments)

def gaussianBifurcation(bifurgationArguments):
    """
    """
    return 2 + int(np.random.normal(*bifurgationArguments))
  
def simpleRandomBifurcations(numberOfLevels, maximumNumberOfNodes,
                             bifurcationsFunction=simpleBifurcation,
                             bifurcationFunctionArguments=(2, 6), verbose=False, gaussian=False):
    """
    Function which creates a nested tree of Node objects
    
    """
    if gaussian:
        bifurcationsFunction = gaussianBifurcation
        
    alreadyBifurcated = []
    objectTree = []
    nodeLabel = 0
    objectTree.append(Node(str(nodeLabel)))
    ready = False
    for level in range(numberOfLevels):
        if ready:
            break
        if verbose:
            print "Level: ", level
        nodesToModify = []
        for node in transverseTree(objectTree):
            if verbose:
                print node.name
            if node.name not in alreadyBifurcated:
                nodesToModify.append(node)
                alreadyBifurcated.append(node.name)
        
        if(len(nodesToModify) == 0):
            break
        else:
            for nodeToModify in nodesToModify:
                if verbose:
                    "Changing: ", nodeToModify.name
                numberOfNewNodes = bifurcationsFunction(bifurcationFunctionArguments)
                if numberOfNewNodes > 0:
                    nodeToModify.children = []
                for numb in range(numberOfNewNodes):
                    nodeLabel += 1
                    global newNode 
                    newNode = Node(str(nodeLabel))
                    nodeToModify.children.append(newNode)    
                    if(nodeLabel > maximumNumberOfNodes):
                        ready = True
                        break
                if ready:
                    break
                
    setBranch(objectTree)
    return objectTree

def generateAndTrain(generationParameters, trainingParameters,
                     resultsDir):
    """
    Creates a random tree, creates its tuples 
    and trains a tree from these tuples
    
    Return 
    
    generatedTree, trainedTree, purity
    """ 
    
    
    generatedObjectTree = simpleRandomBifurcations(generationParameters["numberOfLevels"],
                                                   generationParameters["maxNumberOfNodes"],
                                                   bifurcationFunctionArguments=generationParameters["bifurcationsParameter"],
                                                   gaussian=generationParameters["gaussian"])
    
    
    # ['BranchSizes', 'RootName', 'LevelSize', 'NumberOfNodes', 'NumberOfLevels']
    # print treeStats.allStats(generatedObjectTree)["NumberOfLevels"]
    
    tuples = generateNTuples(generatedObjectTree,
                             generationParameters["numberOfTuples"],
                             verbose=False,
                             withChildren=generationParameters["withChildren"],
                             withNoise=generationParameters["withNoise"])
    
    
    # trainedTree = obtainTree(tuples)
    allTrees, homeless, parentToDescendantStats, bestParentToDescendantStats = obtainTreeNoise2(tuples,
                                                                                               trainingParameters["threshold"],
                                                                    verbose=False)
    
    purity = purityFromGroundTruth(generatedObjectTree,
                            allTrees,
                            verbose=False)
      
    return generatedObjectTree, allTrees, purity 
