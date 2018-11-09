import networkx as nx
import matplotlib.pyplot as plt
import math
import sys

instance = sys.argv[1]
_locations = sys.argv[2]
demands = sys.argv[3]
capacities = sys.argv[4]
time_windows = sys.argv[5]
heuristics = sys.argv[6]


G = nx.Graph(instance=instance)
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

if heuristics == "1":
    for truck in capacities:
        # find nearest unattended customer
        current_node = 0
        nearest_neighbor = None
        min_distance = 9999999999
        print("New route:")
        
        while truck > 0:
            print("current node {}".format(current_node))
            for customer in range(1, len(_locations)):
                print("customer considered {} from node {}".format(customer, current_node))
                if G.node[customer]["status"]:
                    continue
                if current_node == customer:
                    print("equals")
                    continue
                if min_distance > G.get_edge_data(current_node, customer)["weight"]:
                    min_distance = G.get_edge_data(current_node, customer)["weight"]
                    nearest_neighbor = customer
            current_node = nearest_neighbor
            truck -= G.node[current_node]["demand"]
            G.node[current_node]["status"] = 1
            print("customer {}".format(current_node))
            print("capacity left {}".format(truck))
            min_distance = 9999999999

else:
    for truck in capacities:
        # find nearest unattended customer
        current_node = 0
        nearest_neighbor = None
        min_distance = 9999999999
        
        max_distance = 0
        furthest_neighbor = None
        
        print("New route:")
        
        for customer in range(1, len(_locations)):
            if G.node[customer]["status"]:
                    continue
            if current_node == customer:
                continue
            if max_distance < G.get_edge_data(current_node, customer)["weight"]:
                max_distance = G.get_edge_data(current_node, customer)["weight"]
                furthest_neighbor = customer
        current_node = furthest_neighbor
        truck -= G.node[current_node]["demand"]
        G.node[current_node]["status"] = 1
        
        while truck > 0:
            print("current node {}".format(current_node))
            for customer in range(1, len(_locations)):
                if G.node[customer]["status"]:
                    continue
                if current_node == customer:
                    print("equals")
                    continue
                if min_distance > G.get_edge_data(current_node, customer)["weight"]:
                    min_distance = G.get_edge_data(current_node, customer)["weight"]
                    nearest_neighbor = customer
            current_node = nearest_neighbor
            truck -= G.node[current_node]["demand"]
            G.node[current_node]["status"] = 1
            print("customer {}".format(current_node))
            print("capacity left {}".format(truck))
            min_distance = 9999999999
        print("back to depot")
