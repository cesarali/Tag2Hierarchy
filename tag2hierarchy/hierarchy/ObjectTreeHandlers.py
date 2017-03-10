'''
Created on Mar 11, 2016

@author: cesar
'''
import sys
import copy
    
def transverseTree(tree):
    """
    Just applies the depth first search creating a
    generator
    
    Parameters:
    ----------
    tree: list of myTree objects
    
    """
    if tree is not None:
        for node in tree:
            yield node
            for child in transverseTree(node.children):
                yield child
                
def obtainBranch(tree,nodeToStudy):
    """
    """
    for node in transverseTree(tree):
        try:
            if node.name == nodeToStudy:
                return node.myBranch  
        except:
            pass
    
    print "None not found"
    return None

def obtainDescendantsFromNode2(tree,nodeToStudy,verbose=False,cargo=False):
    """
    Obtain childrens and the childrens of the childrens of a given node
    
    Returns:
    -------
    descendants: list of node names
    """
    descendants = []
    for node in transverseTree(tree):
        try:
            if node.name == nodeToStudy:
                if verbose == True:
                    print "Node found: "
                subTree = [node]  
        except:
            pass
    
    for node in transverseTree(subTree):
        try:
            if cargo:
                descendants.append(node.cargo)
            else:
                descendants.append(node.name)
        except:
            pass
    
    return set(descendants).difference(set([nodeToStudy]))

def obtainDescendantsFromNode(tree,nodeToStudy,verbose=False,cargo=False):
    """
    Obtain childrens and the childrens of the childrens of a given node
    
    Returns:
    -------
    descendants: list of node names
    """
    descendants = []
    for node in transverseTree(tree):
        try:
            if node.name == nodeToStudy:
                if verbose == True:
                    print "Node found: "
                subTree = [node]  
        except:
            pass
    
    for node in transverseTree(subTree):
        try:
            if cargo:
                descendants.append({"name":node.name,"cargo":node.cargo})
            else:
                descendants.append(node.name)
        except:
            pass
    if cargo:
        return descendants
    else:
        return set(descendants).difference(set([nodeToStudy])) 

def obtainNodesPerLevel(tree):
    """
    obtains all the nodes per level as a dictionary of list
    
    Parameters:
    ----------
    tree: list of myTree objects
    nodeToStudy: string
    verbose: bool
    cargo: bool if set to true only cargo will be returned
    
    Return:
    -------
    dictionary of list (if cargo True we return the list with just cargo)
        keys : levels, values: list with the nodes per level
    """
    
    
    return   obtainDescendantsPerLevel(tree)

def obtainsNodesAtMyLevel(tree,nodeName,nodesPerLevel=None):
    """
    obtains all the nodes with the same level
    
    Parameters:
    
    tree: list of objects myTree
    node: myTree object
    
    """
    node = obtainSubTree(tree, nodeName)
    myLevel = obtainMyLevel(node[0])
    if nodesPerLevel == None:
        nodesAtMyLevel = [] 
        for nodeE in transverseTree(tree):
            if obtainMyLevel(nodeE) == myLevel and nodeE.name != nodeName: 
                nodesAtMyLevel.append(nodeE.name)
        return nodesAtMyLevel
    else:
        myNeighbors = copy.copy(nodesPerLevel[myLevel])
        myNeighbors.remove(nodeName)
        return myNeighbors
     
def obtainDescendantsPerLevel(tree,nodeToStudy=None,verbose=False,cargo=False):
    """
    obtains all the nodes per level as a list of list
    
    Parameters:
    ----------
    tree: list of myTree objects
    nodeToStudy: string
    verbose: bool
    cargo: bool if set to true only cargo will be returned
    
    Return:
    -------
    dictionary of list (if cargo True we return the list with just cargo)
        keys : levels, values: list with the nodes per level
    """
    descendants = []
    if nodeToStudy != None:
        for node in transverseTree(tree):
            try:
                if node.name == nodeToStudy:
                    if verbose == True:
                        print "Node found: "
                    subTree = [node]  
            except:
                pass
    else:
        subTree = tree
        
    maxLevel = 0 
    for node in transverseTree(subTree):
        try:
            myLevel = len(node.myBranch)-1
            if myLevel > maxLevel:
                maxLevel = myLevel
            if cargo:
                descendants.append({"level":myLevel,"name":node.name,"cargo":node.cargo})
            else:
                descendants.append({"level":myLevel,"name":node.name})
        except:
            pass
        
    if cargo:
        distinctLevels = {levelD["level"]:[] for levelD in descendants}
        for levelD in descendants:
            distinctLevels[levelD["level"]].append({"name":levelD["name"],"cargo":levelD["cargo"]})
        return distinctLevels
    else:
        distinctLevels = {levelD["level"]:[] for levelD in descendants}
        for levelD in descendants:
            distinctLevels[levelD["level"]].append(levelD["name"])
        return distinctLevels
    
def obtainMyLevel(node):
    """
    """
    return len(node.myBranch) - 1
    
def obtainLeavesFromNode(allTrees,nodeToStudy,nodes=False,verbose=False):
    """
    Obtain all the leaves below a given node
    
    Parameters:
    -----------
    tree: list of myTree objects
    node: id of node from whom we wish to find all its leaves
    
    Returns:
    -------
    leaves: list of ids with the leave nodes
    """
    leaves = []
    for tree in allTrees:
        for node in transverseTree([tree]):
            try:
                if node.name == nodeToStudy:
                    if verbose == True:
                        print "Node found: "
                    subTree = [node]  
            except:
                pass
    try:
        for node in transverseTree(subTree):
            try:
                if node.children == None and node.name != nodeToStudy:
                    if nodes:
                        leaves.append(node)
                    else:
                        leaves.append(node.name)
            except:
                pass
    except:
        leaves = [None]
    return leaves

def obtainSubTree(tree,nodeToStudy,verbose=False):
    """
    Returns an object tree which starts with 
    
    
    Returns
    -------
    subTree 
    """
    subTree = None
    for node in transverseTree(tree):
        try:
            if node.name == nodeToStudy:
                if verbose == True:
                    print "Node found: "
                subTree = [node]  
        except:
            print sys.exc_info()
        
    
    return subTree

def obtainNonLeaves(tree,verbose=False):
    """
    Obtain all the nodes which are not a leaf
    
    Parameters:
    -----------
    tree: list of myTree objects
    
    Returns:
    -------
    nonLeaves: list of ids with the leave nodes
    """
    nonLeaves = []
    for node in transverseTree(tree):
        try:
            if node.children != None and len(node.children) > 0:
                nonLeaves.append(node.name)
        except:
            pass

    return nonLeaves

def obtainLeavesAndNonLeaves(tree,verbose=False):
    """
    Obtain all the nodes which are not a leaf
    
    Parameters:
    -----------
    tree: list of myTree objects
    
    Returns:
    -------
    nonLeaves, Leaves: list of ids with the non leaves nodes, list of ids with the leave nodes
    """
    nonLeaves = []
    Leaves = []
    for node in transverseTree(tree):
        try:
            if node.children != None and len(node.children) > 0:
                nonLeaves.append(node.name)
            else:
                Leaves.append(node.name)
        except:
            pass

    return nonLeaves,Leaves
    
def modifyTree(tree,nodeNameToChange):
    """
    Just applies the depth first search creating a
    generator
    
    Parameters:
    ----------
    tree: list of myTree objects
    
    """
    if tree is not None:
        for node in tree:
            yield node
            if(node.name == nodeNameToChange):
                break
            for child in modifyTree(node.children,nodeNameToChange):
                yield child
                
def setBranch(nodes):
    """
    Modifies the tree by defining their branch UP
    all the parents up to the root
    
    Parameters:
    ----------
    nodes: list of my tree objects
    """
    for node in transverseTree(nodes):
        try:
            nodeChildrens = [n.name for n in node.children]
            branch = node.myBranch[:]
            branch.append(node.name)
            for n in node.children:
                n.myBranch.extend(branch)
        except:
            pass
        node.myBranch.append(node.name)

def setEmptyListToNone(tree):
    for node in transverseTree(tree):
        try:
            if( len(node.children) == 0):
                node.children = None
        except:
            pass
            
def nodeNames(tree):
    """
    Stores the tree names
    
    Parameters:
    ----------
    tree: list of myTree objects
    
    Returns:
    -------
    names: list of strings
    """
    names = []
    for node in transverseTree(tree):
        names.append(node.name)
    return names

def setOpenTreeDict(tree):
    """
    This function creates a list of myOpenTree objects 
    as well as the dict of list for all the childrens
    
    """
    openTreeDict = {}
    for node in transverseTree(tree):
        if node.children != None:
            openTreeDict[node.name] = [child.name for child in node.children]
        else:
            openTreeDict[node.name] = None
            
    return openTreeDict

def obtainNodeCargo(tree,nodeName):
    for node in transverseTree(tree):
        if node.name == nodeName:
            return node.cargo
        
def descendantsPerNode(tree):
    """
    """
    names = nodeNames(tree)
    descendantPerNode = {}
    for name in names:
        all_descendants = obtainDescendantsFromNode(tree,name)
        descendantPerNode[name] = (all_descendants,len(all_descendants)) 
    return descendantPerNode

def descendantRankings(descendantsPN):
    """
    """
    numberOfDescendats = []
    for descendant,who_descendants in descendantsPN.iteritems():
        numberOfDescendats.append((who_descendants[1], descendant))
    numberOfDescendats.sort()
    return numberOfDescendats[::-1]

def cutDownTree(oldTree,l):
    """
    This function cuts tree below that level
    
    Parameters
    ----------
    
    oldTree
    l 
    """
    print "WARNING THIS FUNCTION PERMANENTLY DELETES THE TREE"
    nodesPerLevel = obtainNodesPerLevel(oldTree)
    minimunLevel = min(nodesPerLevel.keys())
    maxLevel = minimunLevel + l

    toDelete = []
    for node in transverseTree(oldTree):
        if node.name in nodesPerLevel[maxLevel]:
            toDelete.append(node)
    
    for n in toDelete:
        try:
            del n.children
            n.children = None
        except:
            pass
    
    return oldTree