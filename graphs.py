import networkx as nx
import matplotlib.pyplot as plt
import math
import itertools

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

elif heuristics == "2":
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

elif heuristics == "3":

    def weight(node1: [float,float], node2: [float,float]):
        return math.sqrt((node1[0]-node2[0])**2
              + (node1[1]-node2[1])**2)

    def powerset(iterable, lb=1):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(lb, len(s)+1))

    viable_routes = []
    total_capacity = sum(capacities)
    total_demand = sum(demands)
    lower_bound = total_demand % max(capacities) or max(capacities)

    for route in powerset(range(1, len(G.nodes))):
        demand = 0
        viable = True
        for i in route:
            if not viable:
                continue
            demand += demands[i]
            if demand > max(capacities):
                viable = False
                break
        else:
            if demand >= lower_bound:
                viable_routes += [[route, demand]]

    best_route = [[], 99999999999]
    for solution in tqdm(powerset(viable_routes)):
        attended_demand = sum([x[1] for x in solution])
        coverage = set(i for x in solution for i in x[0])
        if attended_demand == total_demand <= total_capacity and len(coverage) == len(G.nodes) - 1:
            total_weight = sum([G.get_edge_data(x[0][i], x[0][i+1])["weight"] for x in solution for i in range(len(x[0])-1)])
            if total_weight < best_route[1]:
                best_route = [solution, total_weight]
    print(best_route)
    
elif heuristics == "4":
    def ktree(G: nx.Graph, k: int) -> nx.Graph:
        mst = nx.algorithms.tree.minimum_spanning_tree(G, algorithm="prim", weight="weight")
        edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
        while(len(mst.edges) < (len(mst.nodes) + k - 1)):
            for edge in edges:
                if not mst.get_edge_data(edge[0], edge[1]):
                    mst.add_edge(edge[0], edge[1], weight=edge[2]["weight"])
        
        assert(len(mst.edges) < (len(mst.nodes) + k - 1))
        
        # TODO: step 0: make a copy of mst called ktree
        
        
        while ktree.degree[0] > 2*k:
            pass
            # TODO: step 1: store edges on node 0 (depot), ordered by highest weight
            
            # TODO: step 2: remove all edges on depot
            
            # TODO: step 3: label nodes according to their connected components
            
            # TODO: step 4: add those depot_edges again
            
            # TODO: step 5: REMEMBER ONLY COMPONENTS WITH 2+ EDGES TO DEPOT CAN BE DISCONNECTED
            # but they'll be changing during this execution
            # this is going to be a difficult but crucial step
            
            # TODO: step 6: for every edge between customers, compute a cost function w(c1, c2):
            # w(c1,c2) = G.get_edge_data(c1, c2)["weight"] - depot_edges[0][2]["weight"] if label(c1) == label(c2)
            # else G.get_edge_data(c1, c2)["weight"] - max(depot_edges[0][2]["weight"], depot_edge to label(c1)["weight"], depot_edge to label(c2)["weight"])
            # REMEMBER TO STORE THE COMBINATION PICKED (c1, c2, which depot_edge)
            
            # TODO: step 7: if min(w(c1,c2)) from label(c1) == label(c2):
            # remove depot_edges[0][2] from ktree
            # delete depot_edges[0][2]
            # ktree.add_edge(c1,c2,G.get_edge_data(c1, c2)["weight"])
            # ??? maybe ktree.add_edge(G.edges(c1,c2)) ???
            # else:
            # remove depot_edge from ktree
            # delete depot_edge
            # add best edge (according to min(w(c1,c2))) to ktree
            # for all edges which label == label(c2): label = label(c1) since they're now connected
            
        while ktree.degree[0] < 2*k:
            pass
            # TODO: I have no idea 
            
        assert ktree.degree[0] == 2*k
        for i in len(ktree.nodes):
            assert ktree.degree[i] == 2
            
        return ktree

    # TODO: relaxation

    print(ktree(G, len(capacities)))

