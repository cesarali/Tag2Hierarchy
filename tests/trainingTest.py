'''
Created on Mar 11, 2016

@author: cesar
'''
import unittest
import sys

import json
from dhierachies.hNTuples.TreeAsDict import fromDictTreeToObjectTree
from dhierachies.hNTuples.ObjectTreeHandlers import setBranch, nodeNames, obtainDescendantsFromNode
from dhierachies.hNTuples.TupleGenerator import generateNTuples
from dhierachies.hNTuples.training import  obtainTreeNoise
from dhierachies.hNTuples import HTMLPLOT
import datetime
import pymongo

class Test(unittest.TestCase):

    def setUp(self):
        
        dataBaseString = 'Gaming'
        date0 = datetime.datetime(2008,1,1)
        datef = datetime.datetime(2016,1,1)
        client = pymongo.MongoClient()
        self.dataBase = client[dataBaseString]
        self.dictTree = [json.load(open("../data/myTree.json"))]
        self.verbose = False
        
        self.objectTree = fromDictTreeToObjectTree(self.dictTree,self.verbose)
        setBranch(self.objectTree)
        self.numberOfTuples = 1000
        self.tuples = generateNTuples(self.objectTree, self.numberOfTuples)
        self.nodesList = nodeNames(self.objectTree)
        
    def trainingTest(self):
        #----------------------------------OBTAIN THE STATS-------------------------------
        
        print "Number of nodes ",len(self.nodesList)
        myTreeFromTuples, parentToDescendantsStats = obtainTreeNoise(self.tuples, verbose=True)
        
        print obtainDescendantsFromNode(myTreeFromTuples,"C",verbose=False)
        #setEmptyListToNone(mathObjectTree)
        #print setOpenTreeDict(mathObjectTree)
        HTMLPLOT.vizualizeObjectTree(myTreeFromTuples,plotName="myTreeFromTuples")
        
        
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.trainingTest']
    unittest.main()