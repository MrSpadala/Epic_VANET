
from math import sqrt
from collections import defaultdict

import numpy as np


# DEGREE OF CARS
#[75, 35, 51, 35, 106, 77, 36, 99, 66, 57, 56, 71, 30, 54, 86, 53, 32, 54, 27, 53, 71, 57, 68, 52, 33, 35, 5, 53, 22, 53, 65, 39, 54, 8, 122, 74, 35, 85, 46, 32, 30, 78, 27, 58, 59, 43, 44, 22, 46, 53, 52, 53, 52, 63, 31, 26, 34, 47, 90, 53, 81, 4, 45, 30, 53, 31, 53, 49, 44, 46, 28, 26, 49, 43, 12, 33, 58, 40, 45, 29, 47, 38, 83, 81, 73, 46, 80, 18, 59, 14, 58, 20, 50, 55, 50, 56, 24, 73, 17, 54, 28, 89, 50, 88, 53, 78, 31, 44, 61, 62, 62, 2, 96, 16, 68, 26, 40, 97, 31, 37, 37, 78, 59, 45, 75, 14, 62, 78, 54, 38, 52, 50, 61, 55, 47, 48, 7, 59, 29, 94, 31, 27, 55, 73, 6, 25, 55, 43, 86, 84, 7, 55, 15, 31, 11, 29, 92, 49, 60, 47, 79, 41, 9, 58, 40, 46, 81, 44, 70, 28, 47, 35, 44, 26, 29, 52, 21, 47, 48, 67, 6, 107, 48, 42, 57, 81, 48, 57, 45, 96, 61, 57, 41, 22, 71, 54, 89, 52, 76, 71, 103, 80, 29, 98, 62, 93, 26, 45, 48, 90, 29, 46, 93, 29, 17, 31, 59, 40, 26, 106, 50, 77, 54, 53, 74, 28, 91, 17, 31, 79, 54, 10, 102, 13, 12, 22, 27, 24, 22, 52, 98, 21, 73, 50, 46, 49, 29, 59, 44, 23, 55, 49, 41, 56, 66, 28, 68, 56, 30, 49, 55, 85, 104, 10, 55, 55, 44, 22, 40, 55, 36, 17, 6, 65, 9, 61, 62, 58, 66, 79, 32, 81, 16, 12, 65, 65, 67, 43, 42, 111, 45, 73, 49, 17, 17, 7, 49, 57, 49, 27, 58, 9, 13, 24, 55, 63, 16, 88, 17, 56, 45, 68, 50, 76, 70, 86, 55, 74, 56, 95, 74, 55, 46, 92, 71, 69, 23, 91, 45, 48, 25, 50, 80, 31, 16, 31, 17, 56, 53, 16, 23, 26, 12, 30, 32, 110, 17, 27, 17, 58, 17, 16, 48, 52, 22, 29, 121, 4, 49, 49, 72, 98, 44, 38, 22, 3, 4, 76, 50, 50, 5, 57, 51, 8, 21, 38, 48, 25, 10, 48, 12, 43, 103, 55, 48, 45, 54, 61, 55, 57, 43, 45, 57, 81, 7, 47, 45, 19, 5, 11, 52, 36, 45, 42, 58, 44, 94, 37, 46, 37, 44, 44, 73, 38, 49, 10, 78, 56, 23, 55, 18, 18, 66, 38, 20, 58, 55, 36, 67, 40, 59, 21, 53, 103, 62, 27, 40, 77, 67, 82, 85, 50, 38, 53, 4, 86, 60, 77, 85, 35, 58, 73, 53, 6, 74, 52, 38, 101, 81, 64, 10, 50, 33, 36, 31, 95, 52, 55, 31, 58, 55, 21, 57, 51, 33, 30, 32, 25, 32, 57, 2, 81, 53, 67, 14, 58, 48, 79, 83, 31, 55, 84, 75, 36, 52, 54, 84, 16, 31, 14, 53, 36, 32, 46, 10, 34, 38, 35, 41, 23, 83, 29, 46, 24, 59, 43, 27, 16, 10, 37, 46, 17, 46, 32, 47, 39, 30, 33, 57, 43, 46, 28, 14, 48, 18, 67, 35, 31, 37, 62, 25, 46, 42, 46, 58, 27, 58, 16, 52, 35, 46, 46, 17, 49, 34, 46, 60, 56, 41, 46, 42, 34, 45, 43, 84, 59, 47, 49, 58, 44, 66, 30, 33, 24, 9, 42, 8, 33, 35, 17, 27, 59, 37, 17, 34, 34, 18, 30, 16, 34, 55, 13, 46, 38, 31, 38, 50, 6, 31, 57, 53, 102, 101, 31, 93, 22, 20, 73, 103, 16, 104, 35, 105, 30, 37, 4, 22, 104, 34, 101, 68, 30, 103, 31, 104, 22, 48, 47, 50, 103, 31, 32, 36, 25, 38, 54, 46, 19, 49, 39, 31, 35, 46, 7, 36, 58, 13, 36, 32, 39, 41, 38, 56, 46, 41, 46, 47, 38, 39, 9, 22, 53, 54, 52, 65, 51, 49, 48, 20, 48, 10, 35, 49, 48, 49, 49, 51, 34, 48, 41, 49, 49, 48, 39, 49, 19, 49, 10, 30, 41, 23, 40, 68, 17, 1, 3, 41, 37, 9, 40, 8, 4, 9, 1, 38, 37, 39, 22, 4, 44, 47, 2, 6, 42, 37, 27, 27, 2, 27, 27, 25, 15, 32, 27, 16, 27, 27, 44, 39, 29, 11, 17, 27, 21, 15, 21, 35, 17, 17, 3, 40, 49, 29, 1, 13, 55, 27, 27, 28, 9, 4, 42, 1, 30, 42, 28, 26, 47, 29, 37, 14, 26, 40, 3, 30, 28, 25, 30, 25, 6, 14, 5, 8, 1, 6, 3, 24, 14, 6, 2, 6, 35, 24, 30, 6, 25, 4, 15, 25, 1]
# CUMULATIVE
#defaultdict(<class 'int'>, {75: 3, 35: 15, 51: 5, 106: 2, 77: 4, 36: 10, 99: 1, 66: 5, 57: 13, 56: 10, 71: 5, 30: 16, 54: 12, 86: 4, 53: 19, 32: 11, 27: 20, 68: 6, 52: 14, 33: 7, 5: 4, 22: 13, 65: 5, 39: 8, 8: 5, 122: 1, 74: 5, 85: 4, 46: 25, 78: 5, 58: 16, 59: 10, 43: 9, 44: 14, 63: 2, 31: 21, 26: 9, 34: 9, 47: 13, 90: 2, 81: 8, 4: 9, 45: 13, 49: 24, 28: 9, 12: 5, 40: 11, 29: 13, 38: 15, 83: 3, 73: 8, 80: 3, 18: 5, 14: 8, 20: 4, 50: 14, 55: 22, 24: 7, 17: 19, 89: 2, 88: 2, 61: 5, 62: 7, 2: 5, 96: 2, 16: 12, 97: 1, 37: 12, 48: 18, 7: 5, 94: 2, 6: 11, 25: 11, 84: 4, 15: 4, 11: 3, 92: 2, 60: 3, 79: 4, 41: 10, 9: 8, 70: 2, 21: 7, 67: 6, 107: 1, 42: 9, 76: 3, 103: 6, 98: 3, 93: 3, 91: 2, 10: 9, 102: 2, 13: 5, 23: 6, 104: 4, 111: 1, 95: 2, 69: 1, 110: 1, 121: 1, 72: 1, 3: 5, 19: 3, 82: 1, 101: 3, 64: 1, 105: 1, 1: 6})


def dist(c1, c2):
	p,q = c1.pos, c2.pos
	return sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


# A Python program for Prim's Minimum Spanning Tree (MST) algorithm. 
# The program is for adjacency matrix representation of the graph 

def print_MST_stats(cars):

    #print([c.plate for c in cars])
    #print(len([c.plate for c in cars]))

    _car_dict = {c.plate: c for c in cars if c != None}
    car_dict = defaultdict(lambda: None, _car_dict)

    car_graph = []
    tot_degree = 0
    for car in cars:
        entry = []
        deg_entry = 0
        for i in range(len(car.adj)):
            if car.adj[i]==1 and not car_dict[i] is None:
                entry.append(dist(car, car_dict[i]))
                tot_degree += 1
                deg_entry += 1
            elif car_dict[i] is None:
                continue
            else:
                entry.append(0)
        #print(f'{deg_entry}')
        car_graph.append(entry)

    print(f'Mean degree {tot_degree/len(car_graph)}')
    print(f'Edges {tot_degree/2}')



      
    class Graph(): 
      
        def __init__(self, vertices): 
            self.V = vertices 
            self.graph = [[0 for column in range(vertices)]  
                        for row in range(vertices)] 
      
        # A utility function to print the constructed MST stored in parent[] 
        def printMST(self, parent): 
            #print ("Edge \tWeight")
            tot_w = 0
            for i in range(1, self.V): 
                #print (parent[i], "-", i, "\t", self.graph[i][ parent[i] ] )
                tot_w += self.graph[i][ parent[i] ]
            print(f'MST length on street (m): {tot_w:.2f}')
            print(f'Vehicle density (cars/km): {len(self.graph)/(tot_w/1000):.2f}')

      
        # A utility function to find the vertex with  
        # minimum distance value, from the set of vertices  
        # not yet included in shortest path tree 
        def minKey(self, key, mstSet): 
      
            # Initilaize min value 
            min = np.inf 
      
            for v in range(self.V): 
                if key[v] < min and mstSet[v] == False: 
                    min = key[v] 
                    min_index = v 
      
            return min_index 
      
        # Function to construct and print MST for a graph  
        # represented using adjacency matrix representation 
        def primMST(self): 
      
            # Key values used to pick minimum weight edge in cut 
            key = [np.inf] * self.V 
            parent = [None] * self.V # Array to store constructed MST 
            # Make key 0 so that this vertex is picked as first vertex 
            key[0] = 0 
            mstSet = [False] * self.V 
      
            parent[0] = -1 # First node is always the root of 
      
            for cout in range(self.V): 
      
                # Pick the minimum distance vertex from  
                # the set of vertices not yet processed.  
                # u is always equal to src in first iteration 
                u = self.minKey(key, mstSet) 
      
                # Put the minimum distance vertex in  
                # the shortest path tree 
                mstSet[u] = True
      
                # Update dist value of the adjacent vertices  
                # of the picked vertex only if the current  
                # distance is greater than new distance and 
                # the vertex in not in the shotest path tree 
                for v in range(self.V): 
                    # graph[u][v] is non zero only for adjacent vertices of m 
                    # mstSet[v] is false for vertices not yet included in MST 
                    # Update the key only if graph[u][v] is smaller than key[v] 
                    if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]: 
                            key[v] = self.graph[u][v] 
                            parent[v] = u 
      
            self.printMST(parent) 
      
    g = Graph(len(car_graph)) 
    g.graph = car_graph
      
    g.primMST(); 
      
    # Contributed by Divyanshu Mehta 
