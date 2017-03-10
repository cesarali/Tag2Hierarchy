'''
Created on Mar 10, 2017

@author: cesar
'''
import unittest
import matplotlib.pyplot as plt
import json

from tag2hierarchy.hierarchy import TreeAsDict, HTMLPLOT
from tag2hierarchy.hierarchy import ObjectTreeHandlers

class Test(unittest.TestCase):
    
    def jsonToTree(self):
        dictTree = json.load(open("../../data/myTree.json"))
        objectTree = TreeAsDict.fromDictTreeToObjectTree([dictTree])
        names = ObjectTreeHandlers.nodeNames(objectTree)
        backDictTree = TreeAsDict.fromObjectTreeToDictTree(objectTree)        
        print names
        print backDictTree[0]
    
    def jsonToHtml(self):
        dictTree = [{"name":"A","children":[{"name":"B","children":None},{"name":"C","children":None}]}]
        objectTree = TreeAsDict.fromDictTreeToObjectTree(dictTree)
        HTMLPLOT.vizualizeObjectTree("../../visualization/",objectTree, "twoNodes")
    
    
    
if __name__ == '__main__':
    import sys;sys.argv = ['', 'Test.jsonToTree','Test.jsonToHtml']
    unittest.main()