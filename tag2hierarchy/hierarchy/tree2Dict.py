'''
Created on Mar 11, 2016

@author: cesar
'''
from tag2hierarchy.datatypes.hierarchies import Node
from statsmodels.sandbox.distributions.sppatch import expect


#===============================================================================
# Generates the tree of objects from a dictionary tree 
#===============================================================================

def setObjects(nodes,Nodes):
    """
    Create List of objects which posses Non childrens but
    have their children flag set to True for none childrens since they are considered 
    leaves
    """
    if nodes is not None:
        for node in nodes:
            if(node["children"]==None):
                Nodes.append(Node(node["name"],childrenSet=True))
            else:
                Nodes.append(Node(node["name"]))
            yield node
            for child in setObjects(node['children'],Nodes):
                yield child
                
def startNodes(Nodes):
    toIntegrate = [node for node in Nodes if node.childrenSet==True]
    return toIntegrate

def setChildren(nodes,readyNodes,readyNodesStrings,readyNodes0,readyNodesStrings0,joined,verbose=False):
    """
    Fills the objects by joining buttom up. 
    """
    if nodes is not None:
        for node in nodes:
            
            #CHECKING IF ALL CHILDRENS ARE READY=================
            childrensReady = []
            l = []
            if node["children"] is not None:
                for cN in node["children"]:
                    if cN["name"] in readyNodesStrings0:
                        childrensReady.append(True)
                        for a in readyNodes0:
                            if a.name == cN["name"]:
                                l.append(a)
                    else:
                        childrensReady.append(False)
            #=====================================================
            
            
            #HERE WE JOIN KNOWING THAT ALL CHILDRENS ARE READY
            if(False not in childrensReady and childrensReady != []):
                readyNodes.append(Node(node["name"],l[:],childrenSet=True))
                readyNodesStrings.append(node["name"])
                joined.extend([n["name"] for n in node["children"]])
                if(verbose):
                    print "Node : ",node["name"]
                    print "Obtained Kids "
        
            #HERE WE KEEP SINCE IT WAS READY BEFORE
            elif(node["name"] in readyNodesStrings0 and node["name"] not in joined):
                for a in readyNodes0:
                    if a.name == node["name"]:
                        readyNodesStrings.append(node["name"])
                        readyNodes.append(a)
            for child in setChildren(node['children'],readyNodes,readyNodesStrings,readyNodes0,readyNodesStrings0,joined,verbose):
                yield child

def fromDictTreeToObjectTree(dictTree,verbose=False):
    """
    Parameters:
    ----------
    dictTree: list of dictionaries 
        which possees the strcuture {"name":string,"children":(again list of the same dictionaries)}
        if the node is a leaf children:None
    
    Returns:
    --------
    readyNodes0: list of Node objects
    """
    if type(dictTree) != list:
        raise Exception("The tree object most be a list of dictionaries") 
    
    Nodes = []
    for a in setObjects(dictTree,Nodes):
        pass
    
    
    readyNodes0 = startNodes(Nodes)
    initialNodesLabels = len(readyNodes0)
    readyNodesStrings0 = [n.name for n in startNodes(Nodes)]
    loop = 0
    
    while len(readyNodes0) > 0:
        readyNodes = []
        readyNodesStrings = []
        joined = []
        for a in setChildren(dictTree,readyNodes,readyNodesStrings,readyNodes0,readyNodesStrings0,joined,verbose):
            pass
    
        readyNodes0 = readyNodes[:]
        readyNodesStrings0 = readyNodesStrings[:]
        if(len(readyNodes0) == 1):
            break
        loop +=1
        if loop > initialNodesLabels:
            raise Exception("Nodes name might be repeated in the dictionary")
    return readyNodes0
    
#===============================================================================
# Generates the dictionary tree from the object tree
#===============================================================================

def setDictionary(nodes,initialDict,initialNames):
    """
    Creates empty list of dictionaries (for the leaves?)
    """
    if nodes is not None:
        for node in nodes:
            if node.children == None:
                initialDict.append({"name":node.name,"children":node.children})
                initialNames.append(node.name)
            yield node
            for child in setDictionary(node.children,initialDict,initialNames):
                yield child
                

def fillDictionary(nodes,initialDict0,initialNames0,initialDict,initialNames,joined,verbose=False):
    """
    Fills the dictionary by joining buttom up. 
    """
    if nodes is not None:
        for node in nodes:
            try:
                numberOfChildren = len(set(node.children))
                childrenNames = [a.name for a in node.children]
                if len(set(childrenNames).intersection(set(initialNames0))) == numberOfChildren:
                    if verbose:
                        print "Set children to: ", node.name
                
                    thisDict = []
                    for nodeDict in initialDict0:
                        if nodeDict["name"] in childrenNames:
                            thisDict.append(nodeDict)

                    initialDict.append({"name":node.name,"children":thisDict})
                    initialNames.append(node.name)
                    joined.extend(childrenNames)
                elif(node.name in initialNames0 and node["name"] not in joined):
                    for nodeDict in initialDict0:
                        if nodeDict["name"] == node.name:
                            initialDict.append(nodeDict)
                            initialNames.append(node.name)
            except:
                if(node.name in initialNames0 and node.name not in joined):
                    for nodeDict in initialDict0:
                        if nodeDict["name"] == node.name:
                            initialDict.append(nodeDict)
                            initialNames.append(node.name)
            yield node
            for child in fillDictionary(node.children,initialDict0,initialNames0,initialDict,initialNames,joined,verbose):
                yield child
                
def fromObjectTreeToDictTree(objectTree,verbose=False):
    """
    Parameters:
    ----------
    objectTree: list of Node objects
    
    Returns:
    --------
    dictTree: list of dictionaries 
        which possees the strcuture {"name":string,"children":(again list of the same dictionaries)}
        if the node is a leaf children:None
    """
    initialDict0 = []
    initialNames0 = []
    for a in setDictionary(objectTree,initialDict0,initialNames0):
        pass
    
    while len(initialDict0) > 0:
        joined = []
        initialDict = []
        initialNames = []
        for a in fillDictionary(objectTree,initialDict0,initialNames0,initialDict,initialNames,joined,verbose):
            pass
        initialDict0 = initialDict[:]
        initialNames0 = initialNames[:]
        
        if(len(initialDict) == 1):
            break
        
    return initialDict