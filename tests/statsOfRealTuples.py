'''
Created on May 27, 2016

@author: cesar
'''
import numpy as np
import unittest
import sys
from matplotlib import pyplot as plt
import matplotlib
import json
from dhierachies.hNTuples.TreeAsDict import fromDictTreeToObjectTree, fromObjectTreeToDictTree
from dhierachies.hNTuples.ObjectTreeHandlers import setBranch, nodeNames, setOpenTreeDict, setEmptyListToNone
from dhierachies.hNTuples.TupleGenerator import generateNTuples
from dhierachies.hNTuples.tuplesStatistics import cooccuranceBlock
from dhierachies.hNTuples.training import initialize,obtainTree, obtainTreeNoise
from dhierachies.hNTuples.structureTest import blockCoocurrances
from dhierachies.MongoDB import obtainTags
from dhierachies.hNTuples import HTMLPLOT
import datetime
import pymongo
import cPickle

dbBases = ['Biology',
           'English',
           'Finance',
           'MathOverflow',
           'Physics',
           'Statistics']
 
class Test(unittest.TestCase):

    def setUp(self):
        
        date0 = datetime.datetime(2006,1,1)
        datef = datetime.datetime(2016,1,1)
        
        self.dbString = dbBases[0]
        client = pymongo.MongoClient("129.26.78.128",27017)
        client[self.dbString].authenticate("Cesar","gaussianprocess")
        self.dataBase = client[self.dbString]

        self.verbose = False
        self.resultsDir = "/home/cesar/Desktop/Doctorado/Projects/PopulationDynamics/Hierarchies/Results/Trees/"
        self.stackExchangeTuples = obtainTags.obtainTuples(date0,datef,self.dataBase,yearlyPosts=True) 
        
    def trainingTest(self):
        
        #----------------------------------OBTAIN THE STATS-------------------------------
        nodesList,Block,nodesObjectList = initialize(self.stackExchangeTuples)
        #print Block
        #print "Number of nodes: "
        #open(self.resultsDir+"classical-mechanics_TuplesStats.txt","w").write("\n\n".join(map(str,Block)))
        
        #---------------------------------TRAIN THE TREE------------------------------------
        stackExchangeTree,parentToDescendantStats = obtainTreeNoise(self.stackExchangeTuples,parentToDescendantBound=0.7)
        cPickle.dump(stackExchangeTree, open(self.resultsDir+"TupleTree_{0}.cpickle".format(self.dbString),"w"))
        
        #plt.hist(parentToDescendantStats,bins=30)
        #plt.show()
        
        HTMLPLOT.vizualizeObjectTree(stackExchangeTree,plotName=self.dbString+"_07_",dynamic=False)
        
        print len(nodesList)
        
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.trainingTest']
    unittest.main()