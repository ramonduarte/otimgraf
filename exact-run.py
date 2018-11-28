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

total_capacity = sum(capacities)
total_demand = sum(demands)
upper_bound = max(capacities)
lower_bound = min(
    total_demand % max(capacities)  # in case best route include only one truck not full
    or max(capacities),  # in case all trucks are full, lower bound can't be zero
    max(demands[1:]),)  # every truck must attend at least one customer

def weight(node1: [float,float], node2: [float,float]):
    return math.sqrt((node1[0]-node2[0])**2
              + (node1[1]-node2[1])**2)

def powerset(iterable, lb=1):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(lb, len(s)+1))

def valid_powerset(route, routeset):
    ret = []
    for i in range(len(routeset)):
        if len(set(routeset[i][0] + route[0])) == len(routeset[i][0] + route[0]) \
           and total_distance(route) + total_distance(routeset[i]) < upper_bound_distance:
            ret.append(routeset[i])
    return ret

def total_distance(route):
    dist = G.get_edge_data(0, route[0][0])["weight"] + G.get_edge_data(0, route[0][-1])["weight"]
    for i in range(len(route[0]) - 1):
        dist += G.get_edge_data(route[0][i], route[0][i+1])["weight"]
    return dist or 2 * G.get_edge_data(0, route[0])["weight"]

G = nx.Graph(instance="Google OR example")
start = timer()

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

# HAS TO RUN FIRST NO MATTER WHAT
def heuristics_bounds() -> dict:
    viable_routes = []
    for route in powerset(range(1, len(G.nodes))):
        demand = 0
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

    ret = []
    distance_upper_bound = 0

    for truck in capacities:
        # find nearest unattended customer
        current_node = 0
        nearest_neighbor = None
        min_distance = 9999999999

        max_distance = 0
        furthest_neighbor = None

        solution = [[], 0]

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
            solution[0].append(current_node)
            solution[1] += G.nodes[current_node]["demand"]

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
            min_distance = 9999999999

        # print(solution)
        ret.append(solution[1])
        this_solution_distance = sum([G.get_edge_data(solution[0][x],
                                    solution[0][x+1])["weight"]
                                    for x in range(len(solution[0]) - 1)]) \
                                    + G.get_edge_data(solution[0][-1], 0)["weight"] \
                                    + G.get_edge_data(solution[0][0], 0)["weight"]
        distance_upper_bound = max(distance_upper_bound, this_solution_distance)

    return {"lower": min(ret), "upper": distance_upper_bound}

hbounds = heuristics_bounds()
viable_routes = []
lower_bound = min(
    hbounds["lower"],
    total_demand % max(capacities)  # in case best route include only one truck not full
    or max(capacities),  # in case all trucks are full, lower bound can't be zero
    max(demands[1:]),)  # every truck must attend at least one customer
#     heuristic_bounds())  # exact algorithm must beat heuristics
lower_bound_trucks = math.ceil(total_demand % max(capacities))
upper_bound_distance = hbounds["upper"]

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
        if total_distance([route]) > upper_bound_distance:
            viable = False
            break
    else:
        if demand >= lower_bound:
            viable_routes += [[route, demand]]

start = timer()
best_route = [[], 99999999999]
counter = 0
counter2 = 0
for route in viable_routes[::-1]:
    # print(route)
    counter2 += 1
    print(100*counter2/(len(viable_routes)))
    if total_distance(route) > upper_bound_distance:
        print("nó podado: {}".format(route))
        continue
# for route in tqdm(viable_routes):
    # print(route, timer() - start)
    for solution in powerset([route] + valid_powerset(route, viable_routes), lower_bound_trucks):
        # print(valid_powerset(route, viable_routes), timer() - start)
        counter += 1
        attended_demand = sum([x[1] for x in solution])
        coverage = set(i for x in solution for i in x[0])
#         print(solution)
#         print(attended_demand, total_demand, total_capacity, coverage)
        if  total_demand <= attended_demand <= total_capacity and len(coverage) == len(G.nodes) - 1:
            total_weight = sum([G.get_edge_data(x[0][i], x[0][i+1])["weight"] for x in solution for i in range(len(x[0])-1)])
            if total_weight < best_route[1]:
                best_route = [solution, total_weight]
                print(best_route, timer() - start)
        if counter % 10000000 == 0:
            print("{} million at {}/s".format(counter / 1000000, counter/(timer() - start)))
best_route