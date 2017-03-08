'''
Created on Mar 11, 2016

@author: cesar
'''
import unittest
import sys

import json
from dhierachies.hNTuples.TreeAsDict import fromDictTreeToObjectTree
from dhierachies.hNTuples.ObjectTreeHandlers import setBranch, nodeNames
from dhierachies.hNTuples.TupleGenerator import generateNTuples
from dhierachies.hNTuples.tuplesStatistics import differentNTuplesForNode, numberDifferentNTuplesForNode, \
                                                  differentNodesForNode, numberDifferentNodesForNode, possibleTuples

from dhierachies.hNTuples.training import initialize                                               
import operator

class Test(unittest.TestCase):

    def setUp(self):
        self.dictTree = [json.load(open("../data/myTree.json"))]
        self.verbose = False
        self.objectTree = fromDictTreeToObjectTree(self.dictTree,self.verbose)
        setBranch(self.objectTree)
        self.numberOfTuples = 100
        self.tuples = generateNTuples(self.objectTree, self.numberOfTuples)
        self.nodesList = nodeNames(self.objectTree)
        
    def statsOfTuples(self):
        #----------------------------------OBTAIN THE STATS-------------------------------
        ntuplesPerNode = differentNTuplesForNode(self.tuples,self.nodesList)
        nDifferentNTuples =   numberDifferentNTuplesForNode(self.tuples,self.nodesList,ntuplesPerNode,self.verbose)
        differentNodesPN = differentNodesForNode(self.tuples,self.nodesList,verbose=self.verbose)
        nDifferentNodes = numberDifferentNodesForNode(self.tuples,self.nodesList,differentNodesPN,self.verbose)
        #----------------------------------------------------------------------------------
        
        print "Different ntuples"
        for a in sorted(nDifferentNTuples.iteritems(),key=operator.itemgetter(1),reverse=True):
            print a
        
        print "Different Nodes"
        for i,a in enumerate(sorted(nDifferentNodes.iteritems(),key=operator.itemgetter(1))):
            print i,a
        
        print differentNodesPN
        #nPossibleT = possibleTuples(nDifferentNodes)
        #print "Different Possible Tuples"
        #for a in sorted(nPossibleT.iteritems(),key=operator.itemgetter(1),reverse=True):
        #    print a
             
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.statsOfTuples']
    unittest.main()