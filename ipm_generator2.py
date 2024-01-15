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


def generate_graph(seed,fname="problem.txt"):
    # maxcost = mincost = 1 forces max cut problem
    # rng = 1 uses the random number generator from python
    
    rng = np.random.RandomState(seed)
    num_edges = rng.randint(1_000, 10_000)
    num_nodes = rng.randint(1000, 2500)
    num_sinks = rng.randint(1, 5)
    num_sources = rng.randint(1, 5)
    
    pynetgen.netgen_generate(seed=seed, nodes=num_nodes, density=num_edges, sinks=num_sinks, sources=num_sources, 
                             rng=1, maxcost=1, mincost=1, supply=100, mincap=1, maxcap=100, fname=fname)
    return 0


def graph_to_lp(g:nx.DiGraph):
    # TODO: convert the graph to a linear program
    # RETURNS: (A, b, c)
    E = g.number_of_edges()
    V = g.number_of_nodes()
    S = 0
    T = 0
    sink_set = set()
    for node,data in g.nodes(data=True):
        edge_list = list(g.edges(node,data=True))
        if data['name'] == "s" :
            S += 1
        elif data['name'] == 't':
            T += 1
            sink_set.add(node)
    # print(S,T)
    length_of_y = E+V-S-T #this is the number of yv and y uv
    
    #length of x of the orignal form is the yv + yuv
    #for the normal form, each free variable should be substitude by two variables minus like a - b
    # while all y_uv are non negative and all y_v are free, the length should be length of y + V-S-T
    # then we should add all relax variable for these so the final should be 
    #length_of_y + V-S-T +E = length_of_y *2
    c = np.zeros(length_of_y*2)
    
    #it has E constraints , and the # of variables are 2*length_of_y , 
    # so the shape of A should be 
    #[E,length_of_y*2]
    
    A = np.zeros((E,length_of_y*2))
    
    #length of b should be the number of the inequalities constraints
    b = np.zeros(E)
    for node, data in g.nodes(data=True):
        # print(node)
        
        edge_list = list(g.edges(node,data=True))
        # print(edge_list)
        for e in edge_list:
            #We want to minimize sum(c(u,v)*y_uv), we can assume the first E variables are y_uv
            #So for each edge we should change the corresponding c to the capacity of this edge
            c[e[-1]['idx']] = e[-1]['capacity']
            
            #for each yuv 
            A[e[-1]['idx']][e[-1]['idx']] = 1
            
            #relax variable, we put the relax variables after all yuv and yv
            A[e[-1]['idx']][e[-1]['idx']+2*length_of_y-E]=-1
            
            
            if data['name'] == 's':
                #since yv are free, we should subsitute it with a-b, so the coefficient of the yv_a,yv_b is 1,-1
                A[e[-1]['idx']][E+2*(e[1]-S)] = 1
                A[e[-1]['idx']][E+2*(e[1]-S)+1] = -1
                
                #only the edge from 's' we need to change it to 1
                b[e[-1]['idx']] = 1
            elif e[1] in sink_set :
                A[e[-1]['idx']][E+2*(e[0]-S)] = -1
                A[e[-1]['idx']][E+2*(e[0]-S)+1] = 1
            else:
                A[e[-1]['idx']][E+2*(e[1]-S)] = 1
                A[e[-1]['idx']][E+2*(e[1]-S)+1] = -1
                A[e[-1]['idx']][E+2*(e[0]-S)] = -1
                A[e[-1]['idx']][E+2*(e[0]-S)+1] = 1
        # after this step, each row illustrate the 
                
        
            
        # you can check if a node is a source or sink by checking the name
        # data['name'] == 's' or data['name'] == 't'
        
        # get the edges of the node
        # g.edges(node, data=True)
    return A,b,c





if __name__ == "__main__":
    fname = "problem.txt"
    # generate a graph
    # generate_graph(0,fname)
    
    # parse the graph
    # g = parse_dimacs(fname)
    # convert the graph to a linear program
    g = nx.DiGraph()
    # g.add_node(0,name='s')
    # g.add_node(1,name='r')
    # g.add_node(2,name='r')
    # g.add_node(3,name='r')
    # g.add_node(4,name='r')
    # g.add_node(5,name='t')
    
    # g.add_edge(0,1,capacity = 10,idx = 0)
    # g.add_edge(0,2,capacity = 10,idx = 1)
    # g.add_edge(1,2,capacity = 2,idx = 2)
    # g.add_edge(1,3,capacity = 4,idx = 3)
    # g.add_edge(1,4,capacity = 8,idx = 4)
    # g.add_edge(2,4,capacity = 9,idx = 5)
    # g.add_edge(3,5,capacity = 10,idx = 6)
    # g.add_edge(4,3,capacity = 6,idx = 7)
    # g.add_edge(4,5,capacity = 10,idx = 8)
    
    # g.add_node(0,name='s')
    # g.add_node(1,name='r')
    # g.add_node(2,name='r')
    # g.add_node(3,name='t')
    
    # g.add_edge(0,1,capacity = 20,idx = 0)
    # g.add_edge(0,2,capacity = 10,idx = 1)
    # g.add_edge(1,2,capacity = 30,idx = 2)
    # g.add_edge(1,3,capacity = 10,idx = 3)
    # g.add_edge(2,3,capacity = 20,idx = 0)
    
    g.add_node(0,name='s')
    g.add_node(1,name='r')
    g.add_node(2,name='r')
    g.add_node(3,name='r')
    g.add_node(4,name='r')
    g.add_node(5,name='r')
    g.add_node(6,name='r')
    g.add_node(7,name='t')
    
    g.add_edge(0, 1, capacity=10, idx=0)
    g.add_edge(0, 2, capacity=5, idx=1)
    g.add_edge(0, 3, capacity=15, idx=2)
    g.add_edge(1, 2, capacity=4, idx=3)
    g.add_edge(1, 4, capacity=9, idx=4)
    g.add_edge(1, 5, capacity=15, idx=5)
    g.add_edge(2, 3, capacity=4, idx=6)
    g.add_edge(2, 5, capacity=8, idx=7)
    g.add_edge(3, 6, capacity=30, idx=8)
    g.add_edge(4, 5, capacity=15, idx=9)
    g.add_edge(4, 7, capacity=10, idx=12)
    g.add_edge(5, 6, capacity=15, idx=11)
    g.add_edge(5, 7, capacity=10, idx=14)
    g.add_edge(6, 2, capacity=6, idx=10)
    g.add_edge(6, 7, capacity=10, idx=13)
    A, b, c = graph_to_lp(g)
    print("c:", c, "\n")
    print("A:", A, "\n")
    print("b:", b, "\n")
    import cvxpy as cvx
    
    x = cvx.Variable(c.shape[0])
    
    obj = cvx.Minimize(c.T@x)
    con  = [0<=x, A@x==b]
    prob = cvx.Problem(obj, con)
    prob.solve()
    
    print("Dual value associated witth the first constraint:", prob.constraints[0].dual_value, "\n")
    print("Dual value associated witth the second constraint:", prob.constraints[1].dual_value, "\n")
    print("Optimal value for c^Tx:", prob.value, "(30 is the total capacity) \n")
        
    edge_weights = {}
    for i, edge in enumerate(g.edges()):
        edge_weights[edge] = c[i]*x.value[i]
    print("Edges:", edge_weights)

 
    

# `print(c)`: This statement prints the variable `c`, which represents the coefficients of the linear objective function in the linear programming problem. It shows the coefficients associated with each decision variable.

# `print(A)`: This prints the matrix `A`, which represents the coefficients of the constraints in the linear programming problem. Each row corresponds to a constraint, and each column corresponds to a decision variable.

# `print(x.value)`: This statement attempts to print the value of the decision variables `x` after solving the linear programming problem. However, since the solver hasn't been called yet (`prob.solve()` hasn't been executed), `x.value` will likely show `None` or an uninitialized value.

# `print(prob.constraints[1].dual_value)`: This prints the dual value associated with the second constraint in the optimization problem. The dual values provide information about the sensitivity of the constraints in the optimization problem.

# `print(prob.value)`: This prints the optimal value of the objective function once the linear programming problem is solved (`prob.solve()` is called). It represents the optimal solution or the maximum flow achieved in the network flow problem.

# `print(x.value)`: Similar to the second print of `x.value`, it attempts to display the value of the decision variables `x` after solving the linear programming problem.



    
    