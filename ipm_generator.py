import re
import numpy as np
import networkx as nx
import pynetgen # see: https://pypi.org/project/pynetgen/


# Max flow problem
def parse_dimacs(filename):
    with open(filename, 'r') as f:
        for l in f:
            x, *y = l.split()
            
            if x.startswith('p'):
                # problem, nodes, edges
                m, n = re.findall('\d+', l)
                # m number of nodes (r = regular)
                nodes = ["r" for i in range(int(m))]
                # n number of edges
                edges = []
                
            elif x.startswith('n'):
                _, m , n = l.split()
                # set node to target / sink
                nodes[int(m)-1] = n
           
            elif x.startswith('a'):
                # start, end, capacity
                s, e, c = re.findall('\d+', l )
                edges.append([int(s)-1, int(e)-1, int(c)])
    
    # create graph
    g = nx.DiGraph()
    # add nodes
    for i in range(len(nodes)):
        g.add_node(i, name=nodes[i])
    # add edges
    for i, e in enumerate(edges):
        g.add_edge(e[0], e[1], capacity=e[2], idx=i)
    # return the graph
    return g


def generate_graph(seed):
    # maxcost = mincost = 1 forces max cut problem
    # rng = 1 uses the random number generator from python
    
    rng = np.random.RandomState(seed)
    num_edges = rng.randint(1_000, 10_000)
    num_nodes = rng.randint(1000, 2500)
    num_sinks = rng.randint(1, 5)
    num_sources = rng.randint(1, 5)
    
    pynetgen.netgen_generate(seed=seed, nodes=num_nodes, density=num_edges, sinks=num_sinks, sources=num_sources, 
                             rng=1, maxcost=1, mincost=1, supply=100, mincap=1, maxcap=100, fname="problem.txt")
    return "problem.txt"


def graph_to_lp(g):
    # TODO: convert the graph to a linear program
    # RETURNS: (A, b, c)
    for node, data in g.nodes(data=True):
        # you can check if a node is a source or sink by checking the name
        # data['name'] == 's' or data['name'] == 't'
        
        # get the edges of the node
        # g.edges(node, data=True)
        pass


if __name__ == "__main__":
    # generate a graph
    fname = generate_graph(0)
    # parse the graph
    g = parse_dimacs(fname)
    
    # convert the graph to a linear program
    A, b, c = graph_to_lp(g)
    