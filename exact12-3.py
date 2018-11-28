import networkx as nx
import matplotlib.pyplot as plt
import math
import itertools
from tqdm import tqdm_notebook as tqdm
from timeit import default_timer as timer


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

start = timer()
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

v_r = viable_routes[:]

# while len(v_r) > 0:
#     total_trucks = 0
#     attended_demand = 0
#     indexes = range(1, len(capacities))
#     solution = []
#     solution_weight = 9999999999999
#     # while total_trucks <= len(capacities):
#     solution += [v_r[0]]
    
#     total_trucks += 1
#     attended_demand = sum([x[1] for x in solution])
#     coverage = set(i for x in solution for i in x[0])
    
#     for i in range(1, len(capacities)):
#         solution += [viable_routes[i]]
#         total_trucks += 1
#         attended_demand = sum([x[1] for x in solution])
#         coverage = set(i for x in solution for i in x[0])
        
#         if attended_demand == total_demand <= total_capacity \
#            and len(coverage) == len(G.nodes) - 1:
#             total_weight = sum(
#                 [G.get_edge_data(x[0][i], x[0][i+1])["weight"]
#                 for x in solution for i in range(len(x[0])-1)])
#             print("solution: {}, weight: {}, time: {}".format(
#                solution, total_weight, timer() - start))
            
#             for k in range(j+1, len(viable_routes)):
#                 solution += [viable_routes[i]]
#                 total_trucks += 1
#                 attended_demand = sum([x[1] for x in solution])
#                 coverage = set(i for x in solution for i in x[0])
#                 for l in range(k+1, len(viable_routes)):
#                     solution += [viable_routes[i]]
#                     total_trucks += 1
#                     attended_demand = sum([x[1] for x in solution])
#                     coverage = set(i for x in solution for i in x[0])


while len(v_r) > 0:
    total_trucks = 0
    attended_demand = 0
    indexes = range(1, len(capacities))
    solution = []
    solution_weight = 9999999999999
    # while total_trucks <= len(capacities):
    solution += [v_r[0]]
    
#     total_trucks += 1
#     attended_demand = sum([x[1] for x in solution])
#     coverage = set(i for x in solution for i in x[0])
    
#     for i in range(1, len(capacities)):
#         solution += [viable_routes[i]]
#         total_trucks += 1
#         attended_demand = sum([x[1] for x in solution])
#         coverage = set(i for x in solution for i in x[0])
        
#         if attended_demand == total_demand <= total_capacity \
#            and len(coverage) == len(G.nodes) - 1:
#             total_weight = sum(
#                 [G.get_edge_data(x[0][i], x[0][i+1])["weight"]
#                 for x in solution for i in range(len(x[0])-1)])
#             print("solution: {}, weight: {}, time: {}".format(
#                solution, total_weight, timer() - start))
            
#             for k in range(j+1, len(viable_routes)):
#                 solution += [viable_routes[i]]
#                 total_trucks += 1
#                 attended_demand = sum([x[1] for x in solution])
#                 coverage = set(i for x in solution for i in x[0])
#                 for l in range(k+1, len(viable_routes)):
#                     solution += [viable_routes[i]]
#                     total_trucks += 1
#                     attended_demand = sum([x[1] for x in solution])
#                     coverage = set(i for x in solution for i in x[0])

    v_r.pop(0)