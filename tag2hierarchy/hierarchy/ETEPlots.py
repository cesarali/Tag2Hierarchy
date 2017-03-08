'''
Created on Sep 23, 2016

@author: cesar
'''
from ete3 import Tree, TreeStyle, TextFace, add_face_to_node

def generate_node_string(jason_object):
    first = True
    children = ""
    if not jason_object['children'] is None:
        for c in jason_object['children']:
            if not first == True:
                children += ","
            children = children + generate_node_string(c) 
            first = False
        return "({0}){1}".format(children, jason_object['name'])
    else:        
        return jason_object['name']

def plotTree(json_object):
    tree = generate_node_string(json_object)
    t = Tree('{0};'.format(tree), format=1)

    ts = TreeStyle()
    ts.show_leaf_name = False

    ts.layout_fn = my_layout
    ts.branch_vertical_margin = 10  # 10 pixels between adjacent branches

    t.show(tree_style=ts)
    
def my_layout(node):
        F = TextFace(node.name, tight_text=True)        
        if node.is_leaf():
            add_face_to_node(F, node, column=0, position="branch-right")
        else:
            add_face_to_node(F, node, column=0, position="branch-top")
            
def saveTree(json_object, location):
    tree = generate_node_string(json_object)
    t = Tree('{0};'.format(tree), format=1)

    ts = TreeStyle()
    ts.show_leaf_name = False

    ts.layout_fn = my_layout
    ts.branch_vertical_margin = 10  # 10 pixels between adjacent branches

    # t.show(tree_style=ts)
    t.render(file_name=location, w=283, units="mm", tree_style=ts)
    
