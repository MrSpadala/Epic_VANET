
import numpy as np
import sys
sys.path.append("src")
from simulator import init_cars
from sim_config import config


_loaded_scenario = None
_loaded_cars = None
def load_cars(func):
    """
    Decorator loading vehicle data specified in config file.
    """
    def wrapper(*args, **kwargs):
        # Check if we have already loaded the scenario, if yes execute func, otherwise load it
        global _loaded_scenario, _loaded_cars
        if _loaded_scenario != config.scenario:
            _loaded_scenario = config.scenario
            _loaded_cars = init_cars()
        return func(*args, **kwargs)
    return wrapper


# NUMBER OF NODES
@load_cars
def get_n_nodes():
    global _loaded_cars
    return len(_loaded_cars)
    

# NUMBER OF EDGES
@load_cars
def get_n_edges():
    global _loaded_cars
    edges = 0
    for c in _loaded_cars:
        edges += len(c.neighbors)
    edges /= 2
    return edges


# AVERAGE DEGREE
@load_cars
def get_avg_degree():
    global _loaded_cars
    deg = 0
    for c in _loaded_cars:
        deg += len(c.neighbors)
    deg /= len(_loaded_cars)
    return deg


# STD DEV OF DEGREE
@load_cars
def get_std_dev_degree():
    global _loaded_cars
    from matplotlib import pyplot as plt
    import pandas as pd
    degrees = np.array(list(map(lambda c: len(c.neighbors), _loaded_cars)))
    return np.std(degrees)


# GLOBAL CLUSTERING COEFFICIENT
@load_cars
def global_clustering_cff():
    car_dict = {c.plate: c for c in _loaded_cars}
    triangles = 0
    for c1 in _loaded_cars:
        for c2_id in c1.neighbors:
            c2 = car_dict[c2_id]
            for c3_id in c2.neighbors:
                if c3_id in c1.neighbors:
                    triangles += 1
    N = len(_loaded_cars)
    return triangles / (N*(N-1)*(N-2))
    

# LOCAL CLUSTERING COEFFICIENT
@load_cars
def avg_local_clustering_cff():
    car_dict = {c.plate: c for c in _loaded_cars}
    Ci_s = []
    for car in _loaded_cars:
        Ci = 0
        for c1_id in car.neighbors:
            c1 = car_dict[c1_id]
            for c2_id in car.neighbors:
                Ci += 1 if c2_id in c1.neighbors else 0
        ki = len(car.neighbors)
        if ki <= 1:
            Ci_s.append(0)
        else:
            Ci_s.append(Ci / (ki*(ki-1)))
    return sum(Ci_s) / len(Ci_s)


# Average of jaccard similarities of neighborhood of each node
@load_cars
def avg_jaccard():
    def jaccard(c1,c2):
        """
        Calculates the jaccard similarity of neighbors of c1 and neighbors of c2
        """
        neigh1 = set(c1.neighbors)
        neigh2 = set(c2.neighbors) 
        inters = len(set.intersection(neigh1, neigh2))
        union = len(set.union(neigh1, neigh2))
        return inters / union

    car_dict = {c.plate: c for c in _loaded_cars}
    n_cars = len(_loaded_cars)
    jacc_tot = 0
    for c1 in _loaded_cars:
        n_neighbors = len(c1.neighbors)
        jacc_accumulator = 0
        for c2_plate in c1.neighbors:
            c2 = car_dict[c2_plate]
            jacc_accumulator += jaccard(c1,c2)
        jacc_tot += jacc_accumulator / n_neighbors
    return jacc_tot / n_cars

    """
    n_cars = len(_loaded_cars)
    jacc_accumulator = 0
    for c1 in _loaded_cars:
        for c2 in _loaded_cars:
            if c1.plate == c2.plate:
                continue
            jacc_accumulator += jaccard(c1, c2)
    return jacc_accumulator / (n_cars * (n_cars-1))
    """

# DIAMETER, using exact ANF algorithm
@load_cars
def get_diameter():
    global _loaded_cars
    h = 0
    M_prev = {}
    for c in _loaded_cars:
        M_prev[c.plate] = set([c.plate])  # M[x] --> set of nodes reachable from x within h steps

    def all_equals(M):
        val = None
        for reachable in M.values():
            if val is None:
                val = reachable
            elif val != reachable:
                return False
        return True

    while True:
        M_curr = {}
        for car in _loaded_cars:
            M_curr[car.plate] = M_prev[car.plate].copy()
        for c1 in _loaded_cars:
            for c2_plate in c1.neighbors:
                M_curr[c1.plate].update(M_prev[c2_plate])
                M_curr[c2_plate].update(M_prev[c1.plate])

        if all_equals(M_curr):
            return h

        M_prev = M_curr
        h += 1


def print_all():
    print("Printing graph stats for:", config.city_name, config.scenario)
    print("nodes: ", get_n_nodes())
    print("edges: ", get_n_edges())
    print("avg degree: ", get_avg_degree())
    print("std dev degree: ", get_std_dev_degree())
    print("avg local clustering coefficient: ", avg_local_clustering_cff())
    print("diameter: ", get_diameter())


if __name__ == "__main__":
    #print_all()

    
    city_scenario = {
        "Luxembourg": [
            "time27100Tper1000.txt",
            "time27100Tper50.txt"
        ],
        "Cologne": [
            "time23000Tper1000.txt",
            "time23000Tper50.txt"
        ],
        "NewYork": [
            "Newyork7005.mat",
            "Newyork3005.mat"
        ]
    }

    for city, scenarios in city_scenario.items():
        for i, scenario in enumerate(scenarios):  #two scenarios per city, they must be in order high density then low density
            config.city_name = city
            config.scenario = scenario

            print(f"Jaccard {city} {scenario} {avg_jaccard()}")
    