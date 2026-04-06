#Import Statements
import networkx as nx
import matplotlib.pyplot as plt
import random

#Func to gen the standard graph
def generate_basic_graph(n):
    #Setting up graph vars
    G = nx.Graph()
    G.add_nodes_from(range(n))

    #Creating graph with n verts
    for i in range(1, n):
        target = random.randint(0, i - 1)
        G.add_edge(i, target)

    #Cleaning up/Adding extra edges
    extra_edges = max(1, n // 4)
    for _ in range(extra_edges):
        u, v = random.sample(range(n), 2)
        if not G.has_edge(u, v):
            G.add_edge(u, v)

    #Return
    return G

#Func to generate the fractal graph
def generate_flower_fractal(G, center, depth, max_depth, branch_factor):
    #Base Case
    if depth >= max_depth:
        return

    #Setting up array of new nodes
    new_nodes = []

    #Generating flower pattern/adding nodes
    for _ in range(branch_factor):
        new_node = max(G.nodes) + 1
        G.add_node(new_node)
        G.add_edge(center, new_node)
        new_nodes.append(new_node)

    #Recursive call to generate new flower on each node in new nodes
    for new_node in new_nodes:
        generate_flower_fractal(G, new_node, depth + 1, max_depth, branch_factor)

#Wrapper of sorts for fractal func
def generate_fractal_graph_at_start(n):
    #Setting up initial constants
    G = nx.Graph()
    G.add_node(0)
    max_depth = int((n ** 0.5) / 1.5)

    #Calling generation
    generate_flower_fractal(G, 0, 0, max_depth, 6)

    #Cleaning up the recursivness from furthest node to satisfy amount of nodes
    while len(G.nodes) > n:
        #Making sure to only remove leaf nodes
        leaves = [node for node in G.nodes if G.degree[node] == 1 and node != 0]
        if not leaves:
            break
        #Removing leaf node
        G.remove_node(random.choice(leaves))

    #Returning G
    return G

#Func to add random caps
def add_random_capacities(G, min_cap=1, max_cap=10):
    #Setting random caps, min 1 max 10
    for u, v in G.edges():
        G[u][v]['capacity'] = random.randint(min_cap, max_cap)

#Func to get the furthest node
def get_farthest_node(G, source):
    #Getting lengths and finding max to return farthest
    lengths = nx.single_source_shortest_path_length(G, source)
    farthest_node = max(lengths, key=lengths.get)
    return farthest_node

#Func to compute max flow
def compute_max_flow(G, source, sink):
    #Try-Except tree to get flow
    try:
        flow_value, flow_dict = nx.maximum_flow(G, source, sink, capacity='capacity')
        return flow_value, flow_dict
    #Error if flow messes up, return 0 and no path
    except nx.NetworkXError as e:
        print(f"Flow computation error: {e}")
        return 0, {}

#Func to get total cap
def get_total_capacity(G):
    return sum(G[u][v]['capacity'] for u, v in G.edges())

#Func to count how many edges are in use
def count_active_edges(flow_dict):
    #Returning sum of used edges
    return sum(1 for u in flow_dict for v in flow_dict[u] if flow_dict[u][v] > 0)

#Func to draw flow graph
def draw_flow_graph(G, flow_dict, title):
    #Setting up some vars for contants
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)

    #Aesthetic choices
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G, pos)

    #Initializing arrays
    edge_labels = {}
    edge_colors = []

    #For each edge
    for u, v in G.edges():
        #Getting flow cap and edge labels right
        flow = flow_dict.get(u, {}).get(v, 0)
        capacity = G[u][v]['capacity']
        edge_labels[(u, v)] = f"{flow}/{capacity}"

        #If elif else tree to color edges
        if flow == capacity and flow > 0:
            edge_colors.append('red')
        elif flow > 0:
            edge_colors.append('green')
        else:
            edge_colors.append('gray')

    #Designing the edges and their labels
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

    #Initializing the graph
    plt.title(title)
    plt.axis('off')
    plt.show()

#Running program
if __name__ == "__main__":
    #Collecting num of vert input
    n = int(input("Enter number of vertices: "))

    #Generating the graphs
    basic_graph = generate_basic_graph(n)
    fractal_graph = generate_fractal_graph_at_start(n)

    #Adding the capacities
    add_random_capacities(basic_graph)
    add_random_capacities(fractal_graph)

    #Setting source to 0 and sink to furthest node
    source_basic = 0
    sink_basic = get_farthest_node(basic_graph, source_basic)

    #Setting source to 0 and sink to furthest node
    source_fractal = 0
    sink_fractal = get_farthest_node(fractal_graph, source_fractal)

    #Computing the max flow of both basic and fractal graph
    basic_flow, basic_flow_dict = compute_max_flow(basic_graph, source_basic, sink_basic)
    fractal_flow, fractal_flow_dict = compute_max_flow(fractal_graph, source_fractal, sink_fractal)

    #Getting total capacities for graphs
    basic_capacity = get_total_capacity(basic_graph)
    fractal_capacity = get_total_capacity(fractal_graph)

    #Printing out the output for basic
    print(f"\n[Basic Graph] Source: {source_basic}, Sink: {sink_basic}")
    print(f"  Max Flow: {basic_flow}")
    print(f"  Normalized Flow: {basic_flow:.2f} / {basic_capacity} = {basic_flow / basic_capacity:.3f}")
    print(f"  Active Edges: {count_active_edges(basic_flow_dict)}")

    #Printing out the output for fractal
    print(f"\n[Fractal Graph] Source: {source_fractal}, Sink: {sink_fractal}")
    print(f"  Max Flow: {fractal_flow}")
    print(f"  Normalized Flow: {fractal_flow:.2f} / {fractal_capacity} = {fractal_flow / fractal_capacity:.3f}")
    print(f"  Active Edges: {count_active_edges(fractal_flow_dict)}")

    #Actually plotting/displaying the graphs, second on closure of the first
    draw_flow_graph(basic_graph, basic_flow_dict, "Basic Graph with Max Flow")
    draw_flow_graph(fractal_graph, fractal_flow_dict, "Fractal Graph with Max Flow")