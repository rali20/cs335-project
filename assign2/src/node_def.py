import pydot

global graph
global outputfile
global debug
debug = 0
id = 0

graph = pydot.Dot(graph_type='digraph')
debug = True
outputfile = "exp.ps"

def multiple_node_parent(child_labels, parent_label):
    '''childs is a lists'''
    global id
    id += 1
    parent = pydot.Node(id, label=parent_label)
    to_return  = id
    graph.add_node(parent)
    for i in child_labels:
        id += 1
        temp = pydot.Node(id, label=i)
        graph.add_node(temp)
        graph.add_edge(pydot.Edge(parent, temp))
    return to_return


def node(value_a):
    global id
    id += 1
    node_a = pydot.Node(id,label=value_a)
    if debug:
        print(id,value_a,"leaf_node")
        print("\n")
        print(node_a.obj_dict['attributes']['label'])
        print("\n")
    graph.add_node(node_a)
    return id

def one_child_node(a,value_b):
    if a is None :
        return
    global id
    id += 1
    a = pydot.Node(a)
    node_b = pydot.Node(id,label=value_b)
    # if(node_b.obj_dict['attributes']['label'] == 'empty'):
    #     return id
    if debug:
        print(id,value_b,"one_child_node")
        print("\n")
    graph.add_node(node_b)
    graph.add_edge(pydot.Edge(node_b,a))
    return id

def two_child_node(a,b,value_c):
    if a is None :
        return one_child_node(b,value_c)
    elif b is None :
        return one_child_node(a,value_c)
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    node_c = pydot.Node(id,label=value_c)
    if debug:
        print(id,value_c,"two_child_node")
        print("\n")
    graph.add_node(node_c)
    graph.add_edge(pydot.Edge(node_c,a))
    graph.add_edge(pydot.Edge(node_c,b))
    return id

def three_child_node(a,b,c,value_d):
    if a is None :
        return two_child_node(b,c,value_d)
    elif b is None :
        return two_child_node(a,c,value_d)
    elif c is None :
        return two_child_node(a,b,value_d)
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    c = pydot.Node(c)
    node_d = pydot.Node(id,label=value_d)
    if debug:
        print(id,value_d,"three_child_node")
        print("\n")
    graph.add_node(node_d)
    graph.add_edge(pydot.Edge(node_d,a))
    graph.add_edge(pydot.Edge(node_d,b))
    graph.add_edge(pydot.Edge(node_d,c))
    return id

def four_child_node(a,b,c,d,value_e):
    if a is None :
        return three_child_node(b,c,d,value_e)
    elif b is None :
        return three_child_node(a,c,d,value_e)
    elif c is None :
        return three_child_node(a,b,d,value_e)
    elif d is None :
        return three_child_node(a,b,c,value_e)
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    c = pydot.Node(c)
    d = pydot.Node(d)
    node_e = pydot.Node(id,label=value_e)
    if debug:
        print(id,value_e,"four_child_node")
        print("\n")
    graph.add_node(node_e)
    graph.add_edge(pydot.Edge(node_e,a))
    graph.add_edge(pydot.Edge(node_e,b))
    graph.add_edge(pydot.Edge(node_e,c))
    graph.add_edge(pydot.Edge(node_e,d))
    return id


def graph_plot():
    graph.write_ps(outputfile)
