import networkx as nx
import matplotlib.pyplot as plt

def graph_scene_graph(debate_graph):
    G = nx.DiGraph()  # Use a directed graph to represent relationships

    # Add nodes with attributes
    for entity in debate_graph.entities:
        G.add_node(entity.id, content=entity.content)

    # Add edges with relationship types
    for rel in debate_graph.relationships:
        G.add_edge(rel.source_id, rel.target_id, relationship=rel.relationship_type)

    # Set up the plot
    plt.figure(figsize=(15, 10))
    
    # Create the layout
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Draw the graph
    nx.draw(G, pos, with_labels=False, node_color='lightblue', 
            node_size=3000, arrowsize=20)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Draw node labels with content
    node_labels = {node: f"ID: {node}\n{data['content'][:50]}..." 
                  for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

    plt.title("Debate Graph Visualization")
    plt.axis('off')
    
    return plt

# Function to graph all scene graphs in the history list
def graph_all_scene_graphs(graph_history):
    for i, scene_graph in enumerate(graph_history):
        print(f"Scene Graph {i+1}:")
        graph_scene_graph(scene_graph)