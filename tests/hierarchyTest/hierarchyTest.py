'''
Created on Mar 10, 2017

@author: cesar
'''
import unittest
import json
import matplotlib.pyplot as plt

from tag2hierarchy.hierarchy import HTMLPLOT
from tag2hierarchy.hierarchy import tree2Dict
from tag2hierarchy.hierarchy import treeHandlers

class Test(unittest.TestCase):
    
    def jsonToTree(self):
        dictTree = json.load(open("../../data/myTree.json"))
        objectTree = tree2Dict.fromDictTreeToObjectTree([dictTree])
        names = treeHandlers.nodeNames(objectTree)
        backDictTree = tree2Dict.fromObjectTreeToDictTree(objectTree)        
        print names
        print backDictTree[0]
    
    def jsonToHtml(self):
        dictTree = [{"name":"A","children":[{"name":"B","children":None},{"name":"C","children":None}]}]
        objectTree = tree2Dict.fromDictTreeToObjectTree(dictTree)
        HTMLPLOT.vizualizeObjectTree("../../visualization/",objectTree, "twoNodes")
    
    
    
if __name__ == '__main__':
    import sys;sys.argv = ['', 'Test.jsonToTree','Test.jsonToHtml']
    unittest.main()