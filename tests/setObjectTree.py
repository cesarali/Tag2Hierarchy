'''
Created on Mar 11, 2016

@author: cesar
'''
import unittest
import sys

import json
from dhierachies.hNTuples.TreeAsDict import fromDictTreeToObjectTree
from dhierachies.hNTuples.ObjectTreeHandlers import setBranch, transverseTree, nodeNames

class Test(unittest.TestCase):

    def setUp(self):
        self.tree = json.load(open("../data/myTree.json"))
        self.verbose = False
        self.objectTree = fromDictTreeToObjectTree([self.tree],self.verbose)
        
    def createDict(self):
        setBranch(self.objectTree)
        for node in transverseTree(self.objectTree):
            print "Branch of node ",node.name
            print node.myBranch
        print "All names"
        print  nodeNames(self.objectTree)
        
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.createDict']
    unittest.main()