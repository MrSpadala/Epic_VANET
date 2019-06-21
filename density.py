

import os
import pickle
from math import sqrt
import numpy as np
from collections import defaultdict

#cars = init_cars()


def dist(c1, c2):
	p,q = c1.pos, c2.pos
	return sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


def find_nearest(fromcar):
	d = None
	tocar = None
	for car in cars:
		if car == fromcar:
			continue
		newd = dist(fromcar, car)
		if d is None or newd < d:
			d = newd
			tocar = car
	return car


# A Python program for Prim's Minimum Spanning Tree (MST) algorithm. 
# The program is for adjacency matrix representation of the graph 

def init_cars():
    city_name, scenario = "Luxembourg", "time27100Tper1000.txt"   #USE LUXEMBURG
    #city_name, scenario = "Cologne", "time23000Tper1000.txt"     #USE COLOGNE
    #return init_cars_newyork()                                   #USE NEWYORK
    
    fpath = os.path.join("cached", city_name+"_"+scenario+'.bin')
    cached = _load_cached(fpath)
    if cached:  return cached

    print('Computing car graph...')
    positions = []
    p = open("grafi/"+city_name+"/pos/pos_"+scenario, "r")
    for i in p:
        d = i[:-1].split(' ')  #discard trailing \n
        if d[0] == d[2] and d[2] == d[4]:  #don't append malformed rows
            positions.append(None)
        else:
            positions.append((float(d[2]), float(d[3])))

    a = open("grafi/"+city_name+"/adj/adj_"+scenario, "r")
    adi = []
    for l in a:
        adi.append([int(n) for n in l.split(' ')])   #get the value as an int
    cars = [Car(i,p,a) if p else None for i,p,a in zip(range(len(adi)),positions,adi)]   #Use as plate the index of the car
    cars = list(filter(lambda x: x != None, cars))
    cars = get_largest_conn_component(cars)
    pickle.dump(cars, open(fpath, 'wb'))
    return cars

def init_cars_newyork():
    fname = 'Newyork5003.mat'
    fpath = os.path.join("cached", fname+'.bin')
    cached = _load_cached(fpath)
    if cached:  return cached

    print('Computing car graph...')
    import scipy.io as sio
    import numpy as np
    contents = sio.loadmat(os.path.join('grafi/NewYork/', fname))
    adia, coord = contents['Adia'], contents['coord']
    coord = [(x,y) for x,y in zip(coord[0], coord[1])]
    cars = []
    for i,c,a in zip(range(len(adia)),coord,adia):
        cars.append(Car(i,c,a))
    cars = get_largest_conn_component(cars)
    pickle.dump(cars, open(fpath, 'wb'))
    return cars


def _load_cached(fpath):
    if not os.path.exists("cached"):
        os.makedirs("cached")
    if os.path.exists(fpath):
        return pickle.load(open(fpath, "rb"))
    return None

  

cars = init_cars()

print([c.plate for c in cars])
print(len([c.plate for c in cars]))

_car_dict = {c.plate: c for c in cars if c != None}
car_dict = defaultdict(lambda: None, _car_dict)

car_graph = []
for car in cars:
    entry = []
    for i in range(len(car.adj)):
        if car.adj[i]==1 and not car_dict[i] is None:
            entry.append(dist(car, car_dict[i]))
        elif car_dict[i] is None:
            continue
        else:
            entry.append(0)
    car_graph.append(entry)



  
class Graph(): 
  
    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = [[0 for column in range(vertices)]  
                    for row in range(vertices)] 
  
    # A utility function to print the constructed MST stored in parent[] 
    def printMST(self, parent): 
        print ("Edge \tWeight")
        tot_w = 0
        for i in range(1, self.V): 
            print (parent[i], "-", i, "\t", self.graph[i][ parent[i] ] )
            tot_w += self.graph[i][ parent[i] ]
        print('\nTOTAL: ', tot_w)
        print('\nDENSITY (cars/km): ', len(self.graph)/(tot_w/1000))

  
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

print(len(car_graph))
for l in car_graph:
    print(l)
  
g.primMST(); 
  
# Contributed by Divyanshu Mehta 
