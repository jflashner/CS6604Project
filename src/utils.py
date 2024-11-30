# Helper functions
import json
import math
from .debate_manager import DebateManager
from .models import DebateGraph
import logging
import os
from openai import OpenAI

# Set up OpenAI client
api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

def extract_scene_graph(response):
    start_marker = "<SCENE_GRAPH>"
    end_marker = "</SCENE_GRAPH>"
    
    start_index = response.find(start_marker) + len(start_marker)
    end_index = response.find(end_marker)
    
    scene_graph_json = response[start_index:end_index].strip()
    return DebateGraph.model_validate_json(scene_graph_json)

def extract_thoughts_and_winner(judge_response):
    # Extract thoughts
    thoughts_start = judge_response.find("<thoughts>") + len("<thoughts>")
    thoughts_end = judge_response.find("</thoughts>")
    thoughts = judge_response[thoughts_start:thoughts_end].strip()

    # Extract winner
    winner_start = judge_response.find("<winner>") + len("<winner>")
    winner_end = judge_response.find("</winner>")
    winner = judge_response[winner_start:winner_end].strip()

    return thoughts, winner

def display_scene_graph(scene_graph):
    print(json.dumps(scene_graph, indent=4))

def generate(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def calculate_rmse(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Lists must have the same length")

    mse = sum((a - b) ** 2 for a, b in zip(list1, list2)) / len(list1)
    rmse = math.sqrt(mse)
    return rmse

# Used two combine the graphs into one
def combine_debate_graphs(graph1: DebateGraph, graph2: DebateGraph) -> DebateGraph:
    """
    Combines two DebateGraph objects into a single DebateGraph.
    
    Args:
        graph1 (DebateGraph): First debate graph
        graph2 (DebateGraph): Second debate graph
        
    Returns:
        DebateGraph: A new debate graph containing all entities and relationships from both graphs
    """
    # Create sets of entity IDs to check for duplicates
    existing_entity_ids = {entity.id for entity in graph1.entities}
    
    # Combine entities, avoiding duplicates based on ID
    combined_entities = list(graph1.entities)
    for entity in graph2.entities:
        if entity.id not in existing_entity_ids:
            combined_entities.append(entity)
            existing_entity_ids.add(entity.id)
    
    # Combine relationships
    combined_relationships = list(graph1.relationships)
    for rel in graph2.relationships:
        # Only add relationship if both source and target entities exist in combined entities
        if any(e.id == rel.source_id for e in combined_entities) and \
            any(e.id == rel.target_id for e in combined_entities):
            combined_relationships.append(rel)
    
    # Create new DebateGraph with combined entities and relationships
    return DebateGraph(
        entities=combined_entities,
        relationships=combined_relationships
    )

def save_results(winners, structs, batch_number):
    with open(f'debate_results_batch_{batch_number}.json', 'w') as f:
        json.dump(winners, f, indent=4)
    with open(f'structs_batch_{batch_number}.json', 'w') as f:
        json.dump(structs, f, indent=4)

