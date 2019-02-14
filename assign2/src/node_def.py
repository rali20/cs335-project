import pydot

global graph
global outputfile
global debug
debug = 0
id = 0

graph = pydot.Dot(graph_type='digraph')
debug = True
outputfile = "exp.ps"

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

def five_child_node(a,b,c,d,e,value_f):
    global id
    id += 1
    a = pydot.Node(a)
    b = pydot.Node(b)
    c = pydot.Node(c)
    d = pydot.Node(d)
    e = pydot.Node(e)
    node_f = pydot.Node(id,label=value_f)
    if debug:
        print(id,value_f,"five_child_node")
        print("\n")
    graph.add_node(node_f)
    graph.add_edge(pydot.Edge(node_f,a))
    graph.add_edge(pydot.Edge(node_f,b))
    graph.add_edge(pydot.Edge(node_f,c))
    graph.add_edge(pydot.Edge(node_f,d))
    graph.add_edge(pydot.Edge(node_f,e))
    return id

def graph_plot():
    graph.write_ps(outputfile)
