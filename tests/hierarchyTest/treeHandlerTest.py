'''
Created on Mar 10, 2017

@author: cesar
'''
import json
import unittest
import matplotlib.pyplot as plt
import numpy as np

from tag2hierarchy.hierarchy import HTMLPLOT, treeHandlers
from tag2hierarchy.hierarchy import tree2Dict
from tag2hierarchy.hierarchy import treeHandlers
from IPython.html.tree.handlers import TreeHandler

class Test(unittest.TestCase):
    
    def setUp(self):
        self.dictTree = [{"name":"A","children":[{"name":"B","children":[{"name":"D","children":None},
                                                                         {"name":"E","children":None},
                                                                         {"name":"F","children":[{"name":"G","children":None},
                                                                                                 {"name":"H","children":None}]}]},
                                                 {"name":"C","children":None}]}]
        
        self.objectTree = tree2Dict.fromDictTreeToObjectTree(self.dictTree)
        treeHandlers.setBranch(self.objectTree)
        
        HTMLPLOT.vizualizeObjectTree("../../visualization/",self.objectTree, "handlerTest")
        
    def treeToNodes(self):
        #test names
        expected = ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'C']
        actual = treeHandlers.nodeNames(self.objectTree)
        np.testing.assert_equal(actual, expected) 
        #test branch
        branchesExpected = {"A":["A"],
                            "B":["A","B"],
                            "C":["A","C"],
                            "F":["A","B","F"],
                            "E":["A","B","E"],
                            "H":["A","B","F","H"],
                            "G":["A","B","F","G"],
                            "D":["A","B","D"]}
        
        branchesActual = {}
        for n in treeHandlers.transverseTree(self.objectTree):
            branchesActual[n.name] = n.myBranch
            
        assert branchesActual == branchesExpected
        
        #descendants
        descendantsExpected = set(['H', 'E', 'D', 'G', 'F'])
        descendantsActual = treeHandlers.obtainDescendantsFromNode(self.objectTree,"B")
        
        #treeHandlers.descendantsPerNode
        #all descendants
        
        assert descendantsExpected == descendantsActual
           
        #level studies
        nodesPerLevelExpected = {0:["A"],1:["B","C"],2:["D","E","F"],3:["G","H"]}
        nodesPerLevelActual = treeHandlers.obtainNodesPerLevel(self.objectTree)
        assert nodesPerLevelExpected == nodesPerLevelActual
        
        nodesAtMyLevelExpected = ["D","E"] 
        nodesAtMyLevelActual = treeHandlers.obtainsNodesAtMyLevel(self.objectTree,"F",nodesPerLevel=None)
        assert nodesAtMyLevelActual == nodesAtMyLevelExpected
        
        descendantsPerLevelExpected = {2: ['F'], 3: ['G', 'H']}
        descendantsPerLevelActual = treeHandlers.obtainDescendantsPerLevel(self.objectTree,"F")
        assert descendantsPerLevelExpected == descendantsPerLevelActual
        
        #leaves studies
        leavesExpected = ["G","H"]
        leavesActual =  treeHandlers.obtainLeavesFromNode(self.objectTree,"F")  
        assert leavesExpected == leavesActual
        
        nonLeavesExpected = ["A","B","F"]
        nonLeavesActual =  treeHandlers.obtainNonLeaves(self.objectTree)
        assert nonLeavesActual == nonLeavesExpected
        
if __name__ == '__main__':
    import sys;sys.argv = ['', 'Test.treeToNodes']
    unittest.main()