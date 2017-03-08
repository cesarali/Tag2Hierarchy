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

sys.path.append("../")
from dhierachies.hNTuples.TreeAsDict import fromDictTreeToObjectTree, fromObjectTreeToDictTree
from dhierachies.hNTuples.ObjectTreeHandlers import setBranch, nodeNames, setOpenTreeDict, setEmptyListToNone
from dhierachies.hNTuples.TupleGenerator import generateNTuples
from dhierachies.hNTuples.tuplesStatistics import cooccuranceBlock
from dhierachies.hNTuples.training import initialize,obtainTree, obtainTreeNoise, obtainTreeNoise2
from dhierachies.hNTuples.structureTest import blockCoocurrances
from dhierachies.analyse import dynamics
from dhierachies.analyse import treeStats
from dhierachies.MongoDB import obtainTags
from dhierachies.hNTuples import HTMLPLOT
from dhierachies.hNTuples import ObjectTreeHandlers
import datetime
import pymongo
import cPickle


dbBases = ['Biology','English','Finance','MathOverflow','Physics','Statistics']
 
class Test(unittest.TestCase):

    def setUp(self):
        
        date0 = datetime.datetime(2006,1,1)
        datef = datetime.datetime(2016,1,1)
        
        self.dbString = dbBases[0]
        client = pymongo.MongoClient("129.26.78.128",27017)
        client[self.dbString].authenticate("Cesar","gaussianprocess")
        self.dataBase = client[self.dbString]

        self.verbose = False
        self.resultsDir = "/home/cesar/Desktop/Doctorado/Projects/PopulationDynamics/Hierarchies/Results/TrainingComparison3/"
        self.stackExchangeTuples = obtainTags.obtainTuples(date0,datef,self.dataBase,yearlyPosts=True) 
        nodesList,Block,nodesObjectList = initialize(self.stackExchangeTuples)
        
    def trainingTest(self):
        
        date0 = datetime.datetime(2006,1,1)
        datef = datetime.datetime(2016,1,1)
        
        for dbHey in dbBases:
            self.dbString = dbHey
            client = pymongo.MongoClient("129.26.78.128",27017)
            client[self.dbString].authenticate("Cesar","gaussianprocess")
            self.dataBase = client[self.dbString]
    
            self.verbose = False
            self.resultsDir = "/home/cesar/Desktop/Doctorado/Projects/PopulationDynamics/Hierarchies/Results/TrainingComparison3/"
            self.stackExchangeTuples = obtainTags.obtainTuples(date0,datef,self.dataBase,yearlyPosts=True) 
            nodesList,Block,nodesObjectList = initialize(self.stackExchangeTuples)
            
            #----------------------------------OBTAIN THE STATS-------------------------------
            nodesList,Block,nodesObjectList = initialize(self.stackExchangeTuples)
            #print Block
            #print "Number of nodes: "
            #open(self.resultsDir+"classical-mechanics_TuplesStats.txt","w").write("\n\n".join(map(str,Block)))
            
            noiseValues = [0.5,0.6]
            
            print "Training for {0}".format(self.dbString)
            for noise in noiseValues:
                print "Training Noise {0}".format(noise)
            #---------------------------------TRAIN THE TREE------------------------------------
                #stackExchangeTree,parentToDescendantStats = obtainTreeNoise(self.stackExchangeTuples,parentToDescendantBound=noise)
                stackExchangeRoots, homeless, parentToDescendantStats, bestParentStats = obtainTreeNoise2(self.stackExchangeTuples,parentToDescendantBound=noise)
                detectionsData = {root.name:{} for root in stackExchangeRoots}
                print "Homeless Tags ",homeless
                for k, nodeObject in enumerate(stackExchangeRoots):
                    
                    #Dump Trees----------------------------------------
                    stackExchangeTree = [nodeObject]
                    setBranch(stackExchangeTree)
                    cPickle.dump(stackExchangeTree, open(self.resultsDir+"TupleTree_{0}_{1}.cpickle".format(self.dbString,noise),"w"))
                    HTMLPLOT.vizualizeObjectTree(stackExchangeTree,
                                                 plotName=self.dbString+"_{0}_{1}".format(noise,stackExchangeTree[0].name),
                                                 whereToPlot=self.resultsDir,
                                                 dynamic=False)
                    #Obtain Statistics-----------------------------------
                    names = ObjectTreeHandlers.nodeNames(stackExchangeTree)
                    numberOfNodes = len(names)
        
                    branchSizes = treeStats.obtainBranchDistributions(stackExchangeTree)
                    sizeAndLevel = treeStats.sizeAndLevel(stackExchangeTree)
                    maxDepth = len(sizeAndLevel)
                    print sizeAndLevel
                    branches = np.zeros(maxDepth)
                    for k,v in sizeAndLevel.iteritems():
                        branches[k] = v
        
                    detectionsData[nodeObject.name]["NumberOfNodes"] = numberOfNodes
                    detectionsData[nodeObject.name]["BranchSizes"] = branchSizes
                    detectionsData[nodeObject.name]["LevelSize"] = branches
                    
                    #Set cargo
                    dynamics.setTagsCargo(stackExchangeTree,self.dataBase,True)
                    cPickle.dump(stackExchangeTree,open(self.resultsDir+"CargoTupleTree_{0}_{1}_{2}.cpickle".format(self.dbString,stackExchangeTree[0].name,noise),"w"))
        
                cPickle.dump(detectionsData,open(self.resultsDir+"detectionsData_{0}_{1}.cpickle".format(self.dbString,noise),"w"))
                    
                
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.trainingTest']
    unittest.main()