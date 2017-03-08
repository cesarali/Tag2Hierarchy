'''
Created on May 24, 2015

@author: cesar
'''

import unittest
import json
from dhierachies.hNTuples.TreeAsDict import fromDictTreeToObjectTree, fromObjectTreeToDictTree

from dhierachies.hNTuples import HTMLPLOT

class Test(unittest.TestCase):

    def setUp(self):
        self.tree = json.load(open("../data/myTree.json"))
        self.verbose = True
    def createDict(self):
        print self.tree["children"]
        objectTree = fromDictTreeToObjectTree([self.tree],self.verbose)
        dictTree = fromObjectTreeToDictTree(objectTree,self.verbose)
        
        print objectTree[0].children[0].name

if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.createDict']
    unittest.main()