import networkx as nx
import matplotlib.pyplot as plt
import math
import itertools

# Locations in block units
_locations = \
      [(4, 4), # depot
       (2, 0), (8, 0), # locations to visit
       (0, 1),
       (5, 2),
       (3, 3), (6, 3),
       (5, 5), (8, 5),
       (1, 6), (2, 6),
       (0, 8), (7, 8)]

demands = [0, # depot
         1, 1, # row 0
         2,
         2,
         8, 8,
         1, 2,
         1, 2,
         8, 8]

capacities = [15, 15, 15, 15]

time_windows = \
        [(0, 0),
         (75, 85), (75, 85), # 1, 2
         (60, 70), # 3, 4
         (0, 8), # 5, 6
         (0, 10), (10, 20), # 7, 8
         (0, 10), (75, 85), # 9, 10
         (85, 95), (5, 15), # 11, 12
         (45, 55), (30, 40)] # 15, 16

def weight(node1: [float,float], node2: [float,float]):
    return math.sqrt((node1[0]-node2[0])**2
              + (node1[1]-node2[1])**2)

def powerset(iterable, lb=1):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(lb, len(s)+1))

def all_partitions(collection):
    """Returns the set of all partitions for a given set
     e.g for [1,2], it returns [[1],[2]] and [[1,2]]
     https://stackoverflow.com/questions/19368375/set-partitions-in-python
    """
    if len(collection) == 1:
        yield [collection]
        return
    first = collection[0]
    for smaller in all_partitions(collection[1:]):
        for n, subset in enumerate(smaller):
              yield smaller[:n] + [[first] + subset] + smaller[n + 1:]
        yield [[first]] + smaller

G = nx.Graph(instance="Google OR example")

for i in range(len(_locations)):
    G.add_node(i, location=_locations[i], demand=demands[i], time_window=time_windows[i], status=0)

for i in range(len(_locations)):
    for j in range(len(_locations)):
        if i >= j:
            continue
        G.add_edge(i, j,
                   weight=math.sqrt(
                       (_locations[i][0]-_locations[j][0])**2
                       + (_locations[i][1]-_locations[j][1])**2))

viable_routes = []
total_capacity = sum(capacities)
total_demand = sum(demands)
lower_bound = total_demand % max(capacities) or max(capacities)
upper_bound = max(capacities)

for route in powerset(range(1, len(G.nodes))):
    demand = 0
    route_weight = 0
    viable = True
    for i in route:
        if not viable:
            continue
        demand += demands[i]
        if demand > upper_bound:
            viable = False
            break
    else:
        if demand >= lower_bound:
            viable_routes += [[route, demand]]

for truck in capacities:
    # find nearest unattended customer
    current_node = 0
    nearest_neighbor = None
    min_distance = 9999999999
    
    max_distance = 0
    furthest_neighbor = None
    
    print("New route:", end=" ")
    
    for customer in range(1, len(_locations)):
        if G.node[customer]["status"]:
            continue
        if current_node == customer:
            continue
        if max_distance < G.get_edge_data(current_node, customer)["weight"]:
            max_distance = G.get_edge_data(current_node, customer)["weight"]
            furthest_neighbor = customer
    current_node = furthest_neighbor
    if current_node == None or truck < 0:
            break
    truck -= G.node[current_node]["demand"]
    G.node[current_node]["status"] = 1
    
    while truck > 0:
        print("{:>3}".format(current_node), end=" => ")
        for customer in range(1, len(_locations)):
            if G.node[customer]["status"] or current_node == customer:
                continue
            if min_distance > G.get_edge_data(current_node, customer)["weight"]:
                min_distance = G.get_edge_data(current_node, customer)["weight"]
                nearest_neighbor = customer
        current_node = nearest_neighbor
        if current_node == None:
            break
        truck -= G.node[current_node]["demand"]
        if truck < 0:
            break
        G.node[current_node]["status"] = 1
        # print("(capacity left {})".format(truck), end=" ")
        min_distance = 9999999999
    print("back to depot")