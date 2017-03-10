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

from tag2hierarchy.inference import tupleGenerator
from tag2hierarchy.inference import training

class Test(unittest.TestCase):
    
    def setUp(self):
        self.dictTree = [{"name":"A","children":[{"name":"B","children":[{"name":"D","children":None},
                                                                         {"name":"E","children":None},
                                                                         {"name":"F","children":[{"name":"G","children":None},
                                                                                                 {"name":"H","children":None}]}]},
                                                 {"name":"C","children":None}]}]
        
        self.objectTree = tree2Dict.fromDictTreeToObjectTree(self.dictTree)
        treeHandlers.setBranch(self.objectTree)
        
    def treeToTuples(self):
        tupleSet = tupleGenerator.generateNTuples(self.objectTree,100)
        allTrees,homeless, parentToDescendantStats, bestParentToDescendantStats = training.obtainTreeNoise2(tupleSet, 0.2)
        print parentToDescendantStats
        print homeless
        HTMLPLOT.vizualizeObjectTree("../../visualization/",allTrees, "inferredTree")
        
if __name__ == '__main__':
    import sys;sys.argv = ['', 'Test.treeToTuples']
    unittest.main()