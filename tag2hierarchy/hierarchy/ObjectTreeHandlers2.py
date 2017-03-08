'''
Created on Mar 11, 2016

@author: cesar
'''


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
        #print [tree[0].children]

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
                descendants.append(node.cargo)
            else:
                descendants.append(node.name)
        except:
            pass
    
    return set(descendants).difference(set([nodeToStudy]))

def obtainLeavesFromNode(tree,nodeToStudy,verbose=False):
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
            if node.children == None and node.name != nodeToStudy:
                leaves.append(node.name)
        except:
            pass
    
    return leaves

def obtainSubTree(tree,nodeToStudy,verbose=False):
    """
    Returns an object tree which starts with 
    
    
    Returns
    -------
    subTree 
    """
    
    leaves = []
    for node in transverseTree(tree):
        try:
            if node.name == nodeToStudy:
                if verbose == True:
                    print "Node found: "
                subTree = [node]  
        except:
            pass
        
    
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