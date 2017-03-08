'''
Created on Mar 18, 2016

@author: cesar
'''
import unittest


import json
from dhierachies.hNTuples.ObjectTreeHandlers import transverseTree, nodeNames, obtainLeavesFromNode, obtainNonLeaves, setBranch
from dhierachies.hNTuples.TreeAsDict import fromObjectTreeToDictTree
from dhierachies.hierarchyEnsembles.generateTrees import simpleRandomBifurcations
from dhierachies.hNTuples.ObjectTreeHandlers import setOpenTreeDict, nodeNames, setEmptyListToNone
from dhierachies.hNTuples.training import treeToTupleAndBack
from dhierachies.hNTuples.TreeAsDict import fromDictTreeToObjectTree, fromObjectTreeToDictTree
from dhierachies.hNTuples import HTMLPLOT
from dhierachies.hNTuples.TupleGenerator import generateNTuples
from dhierachies.hNTuples.training import initialize,obtainTree
from dhierachies.hNTuples.structureTest import purityFromGroundTruth

class Test(unittest.TestCase):

    def setUp(self):

        self.verbose = False
        self.numberOfLevels = 7
        self.maxNumberOfNodes = 100
        self.numberOfTuples = 20000
        
        self.dictTree = [json.load(open("../visualization/randomTree.json","r"))]
        self.objectTree = fromDictTreeToObjectTree(self.dictTree,self.verbose)
        setBranch(self.objectTree)
        
    def purityTest(self):
        
        #print nodeNames(self.objectTree)
        #print obtainLeavesFromNode(self.objectTree,"5",False)
        
        tuples = generateNTuples(self.objectTree, self.numberOfTuples)
        trainedTree = obtainTree(tuples)
        HTMLPLOT.vizualizeObjectTree(trainedTree,plotName="trainedRandomTree",whereToPlot="../visualization/",dynamic=False)
        
        print purityFromGroundTruth(self.objectTree,trainedTree,True)
        #print obtainNonLeaves(self.objectTree,verbose=False)
        
        
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.purityTest']
    unittest.main()