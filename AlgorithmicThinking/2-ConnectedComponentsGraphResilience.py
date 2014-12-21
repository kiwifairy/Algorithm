"""
Project 2 - Connected components and graph resilience | Python
http://www.codeskulptor.org/#user37_u2WgaWe5HR_45.py
general import
"""
import poc_queue as que
import random
import alg_module2_graphs

def bfs_visited(ugraph, start_node):
    """
    input: set
    output: set
    Takes the undirected graph ugraph 
    and the node start_node 
    and returns the set consisting of all nodes 
    that are visited by a breadth-first search 
    that starts at start_node
    """
    queue = que.Queue()
    visited = set([start_node])
    queue.enqueue(start_node)
    while len(queue) > 0 :
        j_deque = queue.dequeue()
        for h_neigh in ugraph[j_deque]:
            if h_neigh not in visited:
                visited.add(h_neigh)
                queue.enqueue(h_neigh)
    return visited

def cc_visited(ugraph):
    """
    input: set
    output: list
    Takes the undirected graph ugraph 
    and returns a list of sets, 
    where each set consists of all the nodes (and nothing else) 
    in a connected component, 
    and there is exactly one set in the list 
    for each connected component in ugraph and nothing else
    """
    remain_node = set(ugraph.keys())
    cc_setlist = []
    while len(remain_node) > 0 :
        i_node = random.choice(tuple(remain_node))
        w_group = bfs_visited(ugraph, i_node)
        cc_setlist.append(set(w_group))
        remain_node = remain_node.difference(w_group)
    return cc_setlist

def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph 
    and returns the size (an integer) 
    of the largest connected component in ugraph.
    """
    cc_visit = cc_visited(ugraph)
    length = 0
    for item in cc_visit:
        if len(item) > length:
            length = len(item)
    return length
    
def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, 
    a list of nodes attack_order and 
    iterates through the nodes in attack_order. 
    For each node in the list, 
    the function removes the given node 
    and its edges from the graph and then 
    computes the size of the largest connected component 
    for the resulting graph.
    """
    lst = [largest_cc_size(ugraph)] #  the size list of the largest connected component in the graph after the removal of the first  nodes
    for head in attack_order:
        for tail in ugraph[head]:
            ugraph[tail].remove(head)
        ugraph.pop(head)
        lst.append(largest_cc_size(ugraph))
    return lst