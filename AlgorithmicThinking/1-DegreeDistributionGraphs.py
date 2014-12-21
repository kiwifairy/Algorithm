#http://www.codeskulptor.org/#user37_m0aqxXSBKy_0.py
"""Define three constants """
EX_GRAPH0 = {0:set([1,2]), 
             1:set([]),
             2:set([])}

EX_GRAPH1 = {0:set([1,4,5]), 
             1:set([2,6]),
             2:set([3]),
             3:set([0]),
             4:set([1]),
             5:set([2]),
             6:set([])}
             
EX_GRAPH2 = {0:set([1,4,5]), 
             1:set([2,6]),
             2:set([3,7]),
             3:set([7]),
             4:set([1]),
             5:set([2]),
             6:set([]),
             7:set([3]),
             8:set([1,2]),
             9:set([0,3,4,5,6,7])}

GRAPH4 = {"dog": set(["cat"]),
          "cat": set(["dog"]),
          "monkey": set(["banana"]),
          "banana": set([])}
          
def make_complete_graph(num_nodes):  
    """
    Takes the number of nodes num_nodes 
    and returns a dictionary corresponding to a complete directed graph 
    with the specified number of nodes.
    """
    graph = {} 
    lst = []
    if num_nodes>0:
        for num in range(num_nodes):
            lst.append(num) 
        for num2 in range(num_nodes):
            lst_copy = lst[:]
            lst_copy.remove(num2)
            graph[num2]=set(lst_copy)
    return graph


def compute_in_degrees(digraph):   
    """
    Takes a directed graph digraph (represented as a dictionary) 
    and computes the in-degrees for the nodes in the graph. 
    """
    indegree = {}
    for key0 in digraph:
        indegree[key0] = 0
    for key in digraph:
        for node in digraph[key]:
            indegree[node] += 1
    return indegree


def in_degree_distribution(digraph):   
    """
    Takes a directed graph digraph (represented as a dictionary) 
    and computes the unnormalized distribution of the in-degrees of the graph
    """    
    new = {}
    for key0 in range(len(digraph)):
        new[key0] = 0
    distri = compute_in_degrees(digraph)
    for key in distri:
        new[distri[key]] += 1
    new_copy = new.copy()
    for key2 in new:
        if new[key2]==0:
            new_copy.pop(key2)
    return new_copy

#print compute_in_degrees(GRAPH4) 
#print in_degree_distribution(GRAPH4)    
    
