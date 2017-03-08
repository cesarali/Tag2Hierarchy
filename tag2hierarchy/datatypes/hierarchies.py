'''
Created on Marz 4, 2015

@author: cesar
'''


class Node:
    """
    This class represents the basic building unit of a tree **node**.
    
    Parameters:

    
    name -- the label of the node
    children -- list of node objects representing the children of this node,
    childrenSet -- True if the children is not None
    cargo -- list of objects assigned to a node
    
    """
    def __init__(self, name, children=None, childrenSet=False, cargo=None):
        self.name = name
        self.children = children
        self.myBranch = []
        self.childrenSet = childrenSet 
        self.cargo = cargo
