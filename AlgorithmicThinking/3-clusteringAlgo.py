"""
http://www.codeskulptor.org/#user38_VfeERFhySO_13.py
Template for Project 3:Project 3 - Closest pairs and clustering algorithms 
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

import math
import alg_cluster



def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    min_distance = set([( float('inf'), 0, 0 )]) 
    for i_idx in xrange(len(cluster_list)):
        for j_idx in xrange(i_idx+1 , len(cluster_list)):
            pair_dis = pair_distance(cluster_list, i_idx, j_idx)
            if list(pair_dis)[0] < list(min_distance)[0][0] :
                min_distance = set([pair_dis])
            elif list(pair_dis)[0] == list(min_distance)[0][0]:
                min_distance.add(pair_dis) 
    return min_distance


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
        
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        
        # base case
        if len(horiz_order) <= 3:
            sublist = [cluster_list[horiz_order[i]] for i in range(len(horiz_order))]
            result = list(slow_closest_pairs(sublist))[0]
            return result[0], horiz_order[result[1]], horiz_order[result[2]] 

        # divide
        half_num = int(math.ceil(len(horiz_order) / 2.0))  # No. of points in each half
        horiz_line = 0.5 * ( cluster_list[horiz_order[half_num-1]].horiz_center() 
                            + cluster_list[horiz_order[half_num]].horiz_center()) # horizontal line
        # conquer
        front = fast_helper(cluster_list, horiz_order[ : half_num ], [vf for vf in vert_order if vf in set(horiz_order[ : half_num ])])
        back = fast_helper(cluster_list, horiz_order[ half_num : ], [vb for vb in vert_order if vb in set(horiz_order[half_num :])])
        min_d = min(front, back)
        # merge	
        sss = [vi for vi in vert_order if
                abs(cluster_list[vi].horiz_center() - horiz_line) < min_d[0]]

        for _uuu in range(len(sss) - 1):
            for _vvv in range(_uuu + 1, min(_uuu + 4, len(sss))):
                dsuv = cluster_list[sss[_uuu]].distance(cluster_list[sss[_vvv]])
                min_d = min((min_d), (dsuv, sss[_uuu], sss[_vvv]))

        return min_d[0], min(min_d[1], min_d[2]), max(min_d[1], min_d[2])  #return a tuple
            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))

    

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters :
        _, nod1, nod2 = fast_closest_pair(cluster_list)
        cluster_list[nod1].merge_clusters(cluster_list[nod2])
        del cluster_list[nod2]
    return cluster_list

def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    cluster_n = len(cluster_list)
    # initialize k-means clusters to be initial clusters with largest populations
    miu_k = sorted(cluster_list, key = lambda c : c.total_population())[-num_clusters:]
    miu_k = [c.copy() for c in miu_k]

    # iteration 
    for _ in xrange(num_iterations):
        cluster_result = [alg_cluster.Cluster(set([]), 0, 0, 0, 0) for _ in range(num_clusters)]
        # put the node into closet center node

        for jjj in xrange(cluster_n):
            min_num_k = 0
            min_dist_k = float('inf')
            for num_k in xrange(len(miu_k)):
                dist = cluster_list[jjj].distance(miu_k[num_k])
                if dist < min_dist_k:
                    min_dist_k = dist
                    min_num_k = num_k

            cluster_result[min_num_k].merge_clusters(cluster_list[jjj])

        # re-computer its center node
        for kkk in xrange(len(miu_k)):
            miu_k[kkk] = cluster_result[kkk]
    return cluster_result
