'''
Created on Aug 31, 2016

@author: cesar
'''

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
from dhierachies.hNTuples import ObjectTreeHandlers
import operator
from dhierachies.hNTuples import HTMLPLOT
from dhierachies.analyse import treeStats
import cPickle

class Test(unittest.TestCase):

    def setUp(self):
        self.dictTree = [json.load(open("../data/myTree.json"))]
        self.verbose = False
        self.numberOfLevels = 7
        self.maxNumberOfNodes = 300
        self.resultsDir = "/home/cesar/Desktop/Doctorado/Projects/PopulationDynamics/Hierarchies/Results/FakeEnsembles/"
        
    def randomGenerationTest(self):
        
        generatedObjectTree = cPickle.load(open(self.resultsDir+"randomTreeObject.cpickle","r"))
        print ObjectTreeHandlers.obtainNodesPerLevel(generatedObjectTree)
        
        
        
        

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.randomGenerationTest']
    unittest.main()