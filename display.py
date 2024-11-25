import networkx as nx
import matplotlib.pyplot as plt
import time

drawn = 0

def create_graph(nodes, edges):
    # Create a graph
    g = nx.Graph()

    # Add nodes to the graph
    for node_id, attributes in nodes.items():
        g.add_node(node_id, **attributes)

    # Add edges to the graph
    for edge in edges:
        g.add_edge(edge['node1'], edge['node2'])

    # Draw the graph
    pos = nx.spring_layout(g)  # Positions for nodes


    return g, pos
    
def draw_graph(g, pos):
    # Draw nodes with labels
    nx.draw_networkx_nodes(g, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_labels(g, pos, labels={node: node for node in g.nodes}, font_size=12, font_color='black')

    # Draw edges
    nx.draw_networkx_edges(g, pos, edge_color='gray')

    # Show the plot
    plt.title(f"Graph Visualization {drawn}")
    plt.axis('off')  # Turn off the axis
    plt.show()

def run(nodes, edges):
    # Example IMPLEMENTATION
    g, pos = create_graph(nodes, edges)
    draw_graph(g, pos)

# Example NODES
nodes = {
    'W': {"name": "Node A"},
    'E': {"name": "Node B"},
    'L': {"name": "Node C"},
    'C': {"name": "Node D"},
    'O': {"name": "Node A"},
    'M': {"name": "Node B"},
    'e': {"name": "Node C"}
}

# Example EDGES
edges = [
    {"node1": 'W', "node2": 'E'},
    {"node1": 'E', "node2": 'L'},
    {"node1": 'L', "node2": 'C'},
    {"node1": 'C', "node2": 'O'},
    {"node1": 'O', "node2": 'M'},
    {"node1": 'M', "node2": 'e'}
]

# Example IMPLEMENTATION
g, pos = create_graph(nodes, edges)
draw_graph(g, pos)