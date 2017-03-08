'''
Created on Aug 25, 2016

@author: cesar
'''

import unittest
import sys
import numpy as np
import random
import json
from dhierachies.hNTuples.ObjectTreeHandlers import transverseTree
from dhierachies.hNTuples.TreeAsDict import fromObjectTreeToDictTree
from dhierachies.hierarchyEnsembles.generateTrees import simpleRandomBifurcations, generateAndTrain
from dhierachies.hNTuples.ObjectTreeHandlers import setOpenTreeDict, nodeNames
from dhierachies.hNTuples.TupleGenerator import generateNTuples
from dhierachies.analyse import treeStats
import operator
from dhierachies.hNTuples import HTMLPLOT
from dhierachies.hNTuples.training import initialize,obtainTree, obtainTreeNoise2
from dhierachies.hNTuples.structureTest import purityFromGroundTruth
from matplotlib import pyplot as plt
from IPython.kernel.zmq.serialize import cPickle

class Test(unittest.TestCase):

    def setUp(self):
        self.dictTree = [json.load(open("../data/myTree.json"))]
        self.verbose = False
        self.numberOfLevels = 5
        
        """
        self.maxNumberOfNodes = 100
        self.numberOfTrees = 50
        
        self.generationParameters = {"numberOfLevels":5,
                                     "maxNumberOfNodes":100,
                                     "numberOfTuples":1000,
                                     "bifurcationsParameter":(2,6)}
        
        self.trainingParameters = {"threshold":0.8}
        """
        self.resultsDir = "/home/cesar/Desktop/Doctorado/Projects/PopulationDynamics/Hierarchies/Results/FakeEnsembles/"
        
    def randomGenerationTest(self):
        
        #==================================================
        # PURITY MATRIX RANDOM LOOP
        #==================================================
        
        """
        #self.generationParameters["numberOfLevels"] = 5
        #self.generationParameters["maxNumberOfNodes"] = 100
        self.generationParameters["numberOfTuples"] = 1000
        self.generationParameters["bifurcationsParameter"] = (2,20)
        self.generationParameters["withChildren"] = (True,0.8,2)
        self.generationParameters["horizontalMixing"] = (True,0.8,2)
        self.generationParameters["withNoise"] = (True,0.8,4)
        #self.trainingParameters["threshold"] = 0.8
        
        
        bifurcationMax = np.arange(3,20,2)
        TH = np.arange(0.1,1.,0.1)
        numberOfTuples =  np.arange(100,2000,150)
        
        PuritiesMatrix = []
        PuritiesErr = []
        for bM in bifurcationMax:
            print "Bifurcation Max ",bM
            self.generationParameters["bifurcationsParameter"] = (2,bM)
            #print "Working with threshold ",th
            #self.trainingParameters = {"threshold":th}
            Purities = []
            for nT in numberOfTuples:
                print "Number Of Tuples ",nT   
                self.generationParameters["numberOfTuples"] = nT
                avPurity = []
                
                for i in range(self.numberOfTrees):
                    try:
                        generatedObjectTree, trainedTree, purity  = generateAndTrain(self.generationParameters,
                                                                                     self.trainingParameters,self.resultsDir)
                        avPurity.append(purity)
                    except:
                        print sys.exc_info()
                        pass 
                    
                    #treeStats.allStats(generatedObjectTree)
                    
                avPurity = np.asarray(avPurity)
                Purities.append(avPurity.mean())
            PuritiesMatrix.append(np.asarray(Purities))
        
        #np.savetxt(self.resultsDir+"puritiesLoop.txt", np.asarray([TH,Purities]))
        
        cPickle.dump((self.generationParameters,
                      bifurcationMax,numberOfTuples,PuritiesMatrix),
                     open(self.resultsDir+"10_branchingFactor_numberOfTuples.cpickle","w"))
        #plt.plot(TH,Purities,"ro")
        #plt.show()
        
        """
        #==================================================
        # ONE LOOP
        #==================================================
        
        
        #bifurcationMax = np.arange(3,20,2)
        TH = np.arange(0.0,0.9,0.025)
        
        self.generationParameters =  {}
        self.generationParameters["numberOfLevels"] = 5
        self.trainingParameters = {"threshold":0.8}
        self.numberOfTrees = 50
        
        simulationIndex = 0
        BRANCHING_FACTOR = [3,6,10,20]
        NUMBER_OF_NODES = [100,500,1000,2000]
        PERCENTAGE_OF_NOISE = [0.1,0.2,0.4,0.8]
        NUMBER_OF_TUPLES = [700,1000,5000,10000,20000]
        
        for branching_factor in BRANCHING_FACTOR:
            for number_of_nodes in NUMBER_OF_NODES:
                for percentage_of_noise in PERCENTAGE_OF_NOISE:
                    for number_of_tuples in NUMBER_OF_TUPLES:
                        
                        #
                        self.generationParameters["maxNumberOfNodes"] = number_of_nodes
                        self.generationParameters["numberOfTuples"] = number_of_tuples
                        self.generationParameters["bifurcationsParameter"] = (2,branching_factor)
                        self.generationParameters["withChildren"] = (True,percentage_of_noise,2)
                        self.generationParameters["horizontalMixing"] = (False,0.8,2)
                        self.generationParameters["withNoise"] = (True,percentage_of_noise,3)
                        
                        print self.generationParameters
                        
                        Purities = []

                        for th in TH:
                            print "Current threshold ",th
                            self.trainingParameters["threshold"] = th
                            avPurity = []
                            np.random.seed(1)
                            random.seed(1)
                            for i in range(self.numberOfTrees):
                                
                                generatedObjectTree, trainedTree, purity  = generateAndTrain(self.generationParameters,
                                                                                             self.trainingParameters,
                                                                                             self.resultsDir)
                                avPurity.append(purity)
                 
                                #treeStats.allStats(generatedObjectTree)
                                
                            avPurity = np.asarray(avPurity)
                            Purities.append(avPurity.mean())
                            
                        cPickle.dump((self.trainingParameters,
                                      self.generationParameters,TH,np.asarray(Purities)),
                                     open(self.resultsDir+"{0}_branching.cpickle".format(simulationIndex),"w"))
                        simulationIndex += 1
        
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.randomGenerationTest']
    unittest.main()
    
"""

cls=np.array(cooccuranceData[0])[randomIndexSample]
dat=np.array(cooccuranceData[1])[randomIndexSample] [:,randomIndexSample]#  [:30,:30]
plt.clf()
fig = plt.figure()
fig.set_size_inches(10, 10)
#plt.matshow(dat,cmap = plt.get_cmap('jet'))
plt.matshow(dat,cmap = plt.get_cmap('hot'))
plt.colorbar(shrink=.80)
plt.xticks(np.arange(len(cls)),cls, rotation=90)
plt.yticks(np.arange(len(cls)),cls)
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 7}

matplotlib.rc('font', **font)
plt.savefig("./plotsSaved/{0}_cooocuranceConfidence_{1}_{2}month.pdf".format(dbString,TAG_NAME,numberOfMonths),bbox_inches='tight')



%matplotlib inline
phaseNumber = 2
X,Y,Z0 = cPickle.load(open(diagram_folder+"phase_EPO_Diagram_{0}.cpickle".format(phaseNumber),"r"))

plt.figure(figsize=(8,10))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 11}

matplotlib.rc('font', **font)

xi = X[:]
yi = Y[:]
x = X[:]
y = Y[:]
plt.close("all")
zi = Z0[:]
# grid the data.
#zi = griddata(x, y, z, xi, yi, interp='linear')
# contour the gridded data, plotting dots at the nonuniform data points.
CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
img  = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.seismic,
                  vmax=abs(zi).max(), vmin=0.)

#r'$|D_1-D_3|$'
plt.xlabel(r'$\epsilon_{to}$',fontsize=30)
plt.ylabel(r'$\epsilon_{from}$',fontsize=30)
plt.colorbar(ticks=np.arange(0.,abs(zi).max()+15.,15.))  # draw colorbar
plt.tight_layout()

plt.savefig(diagram_folder+"phase_EPO_Diagram_{0}.pdf".format(phaseNumber))
plt.show()
plt.close("all")
"""