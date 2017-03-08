'''
Created on Mar 11, 2016

@author: cesar
'''

import unittest
import sys

import json
from dhierachies.hNTuples.ObjectTreeHandlers import transverseTree
from dhierachies.hNTuples.TreeAsDict import fromObjectTreeToDictTree
from dhierachies.hierarchyEnsembles.generateTrees import simpleRandomBifurcations
from dhierachies.hNTuples.ObjectTreeHandlers import setOpenTreeDict, nodeNames
import operator
from dhierachies.hNTuples import HTMLPLOT
from dhierachies.analyse import treeStats
import cPickle

class Test(unittest.TestCase):

    def setUp(self):
        self.dictTree = [json.load(open("../data/myTree.json"))]
        self.verbose = False
        self.numberOfLevels = 7
        self.maxNumberOfNodes = 500
        self.bifurcationFunctionArguments = (1,4)
        self.resultsDir = "/home/cesar/Desktop/Doctorado/Projects/PopulationDynamics/Hierarchies/Results/FakeEnsembles/"
        
    def randomGenerationTest(self):
        generatedObjectTree = simpleRandomBifurcations(self.numberOfLevels,
                                                       self.maxNumberOfNodes,
                                                       bifurcationFunctionArguments=self.bifurcationFunctionArguments)
        
        print "Number of nodes: ",len(nodeNames(generatedObjectTree))
        print "Open object Tree: ",setOpenTreeDict(generatedObjectTree)
        dictTree = fromObjectTreeToDictTree(generatedObjectTree)
        
        
        statsDict = treeStats.allStats(generatedObjectTree)
        print statsDict['NumberOfNodes']
        HTMLPLOT.vizualizeObjectTree(generatedObjectTree,
                                     plotName="randomTree",
                                     whereToPlot=self.resultsDir,
                                     dynamic=False)
        
        json.dump(dictTree[0],open(self.resultsDir+"randomTree.txt","w"))
        cPickle.dump(generatedObjectTree,open(self.resultsDir+"randomTreeObject.cpickle","w"))
        
        

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.randomGenerationTest']
    unittest.main()