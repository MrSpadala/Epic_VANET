
import numpy as np
import sys
sys.path.append("src")
from simulator import init_cars
from sim_config import config

cars = init_cars()
car_dict = {c.plate: c for c in cars}
n_cars = len(cars)

def get_n_nodes():
    # NUMBER OF NODES
    return n_cars
    

# NUMBER OF EDGES
def get_n_edges():
    edges = 0
    for c in cars:
        edges += len(c.neighbors)
    edges /= 2
    return edges

# AVERAGE DEGREE
def get_avg_degree():
    deg = 0
    for c in cars:
        deg += len(c.neighbors)
    deg /= n_cars
    return deg

# STD DEV OF DEGREE
def get_std_dev_degree():
    from matplotlib import pyplot as plt
    import pandas as pd
    degrees = np.array(list(map(lambda c: len(c.neighbors), cars)))
    return np.std(degrees)
    

# DIAMETER, using exact ANF algorithm
def get_diameter():
    h = 0
    M_prev = {}
    for c in cars:
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
        for car in cars:
            M_curr[car.plate] = M_prev[car.plate].copy()
        for c1 in cars:
            for c2_plate in c1.neighbors:
                M_curr[c1.plate].update(M_prev[c2_plate])
                M_curr[c2_plate].update(M_prev[c1.plate])

        if all_equals(M_curr):
            return h

        M_prev = M_curr
        h += 1


if __name__ == "__main__":
    print("Printing graph stats for:", config.city_name, config.scenario)
    print("nodes: ", get_n_nodes())
    print("edges: ", get_n_edges())
    print("avg degree: ", get_avg_degree())
    print("std dev degree: ", get_std_dev_degree())
    print("diameter: ", get_diameter())