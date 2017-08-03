'''
Created on Aug 3, 2017

@author: cesar
'''
import unittest
import json
import matplotlib.pyplot as plt

from tag2hierarchy.hierarchy import HTMLPLOT
from tag2hierarchy.hierarchy import tree2Dict
from tag2hierarchy.hierarchiesEnsembles import generateTrees

class Test(unittest.TestCase):
    
    def generateTree(self):
        objectTree = generateTrees.simpleRandomBifurcations(3, 
                                                            1000,
                                                            bifurcationFunctionArguments=(2, 6), 
                                                            verbose=False, 
                                                            gaussian=False)
        HTMLPLOT.vizualizeObjectTree("../../visualization/",objectTree, "generated")
        
if __name__ == '__main__':
    import sys;sys.argv = ['', 'Test.generateTree']
    unittest.main()