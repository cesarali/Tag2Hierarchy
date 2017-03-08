'''
Created on Mar 11, 2016

@author: cesar
'''
import unittest
import sys
import cPickle
import json
from dhierachies.hNTuples.TreeAsDict import fromDictTreeToObjectTree
from dhierachies.hNTuples.ObjectTreeHandlers import setBranch, transverseTree, nodeNames
from dhierachies.hNTuples.TupleGenerator import generateNTuples
from dhierachies.hNTuples.training import initialize

class Test(unittest.TestCase):

    def setUp(self):
        self.dictTree = [json.load(open("../data/myTree.json"))]
        self.verbose = False
        self.objectTree = fromDictTreeToObjectTree(self.dictTree,self.verbose)
        setBranch(self.objectTree)
        self.numberOfTuples = 250
        
    def createTuples(self):
        tuples = generateNTuples(self.objectTree, self.numberOfTuples,verbose=False)
        nodesList,Block,nodesObjectList = initialize(tuples)
        cPickle.dump(tuples, open("../data/moreTuples.json","w"))
        
        print tuples
        print len(tuples)
        for a in Block:
            print a
        
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.createTuples']
    unittest.main()