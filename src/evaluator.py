import os
from openai import OpenAI
import pandas as pd
from .debate_manager import DebateManager
from .debate_processor import process_debate
from .visualization import graph_scene_graph, graph_all_scene_graphs
from .utils import save_results, calculate_rmse, generate

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  
)

# Element 1: Factual accuracy evaluation
def evaluate_factual_accuracy_gpt(statement):
    prompt = f"""
    Evaluate the factual accuracy of the following statement:

    "{statement}"

    Respond in the format and do not say anything else:
    - Factual: (True/False) respond with one word only
    - Confidence: (0.0 to 1.0 scale, where 1.0 is absolute confidence)
    - Feedback: Only if it's False, give a one-line explanation for why that is the case.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a fact-checking assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0
        )
        content = response.choices[0].message.content
        

        factual = "True" in content.split("\n")[0]  
        confidence_line = next(line for line in content.split("\n") if "Confidence:" in line)
        confidence = float(confidence_line.split("Confidence: ")[-1].strip())
        
        feedback_line = next((line for line in content.split("\n") if "Feedback:" in line), None)
        feedback = feedback_line.split("Feedback: ")[-1].strip() if feedback_line else None
        
        return int(factual), confidence, feedback
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return 0, 0.0, None

def calculate_normalized_score(results):
    total_score = sum(factuality * confidence for factuality, confidence, _ in results)
    max_score = len(results) 
    feedback = [feedback for _, _, feedback in results if feedback] 
    return total_score / max_score if max_score > 0 else 0, feedback

# Element 2: Persuasiveness evaluation
def evaluate_persuasiveness_gpt(pro_argument, con_argument):
    prompt = f"""
    Compare the following arguments and decide which is more persuasive:

    Pro Argument: "{pro_argument}"
    Con Argument: "{con_argument}"

    Respond with "Pro" or "Con" based on which is more persuasive.
    If you find either argument lacking, explain briefly why it is less persuasive.

    Respond in the format:
    - Persuasiveness: (Pro/Con)
    - Feedback: (Brief explanation if any argument is less persuasive)
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a debate evaluator who determines persuasiveness."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0
        )
        content = response.choices[0].message.content.strip()

       
        lines = content.split("\n")
    
        persuasiveness = lines[0].replace('- Persuasiveness:', '').strip().lower()
        
        feedback_line = next((line for line in lines if "Feedback:" in line), None)
        feedback = feedback_line.split("Feedback:")[-1].strip() if feedback_line else None

        return persuasiveness, feedback
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Error", None

def find_entity_by_id(entities, node_id):
    return entities.get(node_id)  


#Element 3: argument structure 
def count_nodes_with_relationship(relationships, relationship_type, entities):
    nodes_with_relationship = set()
    for rel in relationships:
        if rel.relationship_type == relationship_type:
            nodes_with_relationship.add(rel.source_id)
            nodes_with_relationship.add(rel.target_id)

    pro_count = 0
    con_count = 0
    for node in nodes_with_relationship:
        entity = find_entity_by_id(entities, node)
        if entity:  
            if entity.side == "pro":
                pro_count += 1
            elif entity.side == "con":
                con_count += 1
    return pro_count, con_count

def normalize_score(pro_count, con_count, total):
    pro_score = pro_count / total if total > 0 else 0
    con_score = con_count / total if total > 0 else 0
    return pro_score, con_score

def print_feedback(feedback_list, side):
    if not feedback_list:
        print(f"No issues were found with the {side} arguments.")
    else:
        print(f"\nFeedback for {side} arguments:")
        for i, feedback in enumerate(feedback_list, 1):
            print(f"{i}. {feedback}")

def evaluate_graph(debate_graph):
    pro_arguments = []
    con_arguments = []
    #factual accuracy 
    for argument in debate_graph.entities:
        if argument.side =='pro':
            pro_arguments.append(argument)
        elif argument.side =='con': 
            con_arguments.append(argument)
    
    relationships = debate_graph.relationships
    entities = {entity.id: entity for entity in debate_graph.entities}

    rebuttals = []
    for rel in relationships:
        if rel.relationship_type == 'rebuttal':
            source = entities[rel.source_id]
            target = entities[rel.target_id]
            rebuttals.append((source, target))

    pro_results = [evaluate_factual_accuracy_gpt(arg) for arg in pro_arguments]
    con_results = [evaluate_factual_accuracy_gpt(arg) for arg in con_arguments]

    pro_score, pro_factual_feedback = calculate_normalized_score(pro_results)
    con_score, con_factual_feedback = calculate_normalized_score(con_results)

    pro_score_persuasion = 0
    con_score_persuasion = 0
    feedback_pro = []
    feedback_con = []

    for source, target in rebuttals:
        if source.side == 'pro' and target.side == 'con':
            result, feedback = evaluate_persuasiveness_gpt(source.content, target.content)
        elif source.side == 'con' and target.side == 'pro':
            result, feedback = evaluate_persuasiveness_gpt(target.content, source.content)
        else:
            continue  


        if result == "pro":
            pro_score_persuasion += 1
            if feedback:
                feedback_pro.append(feedback)
        elif result == "con":
            con_score_persuasion += 1
            if feedback:
                feedback_con.append(feedback)



    total_rebuttals = pro_score_persuasion + con_score_persuasion
    pro_score_persuasion_normalized = pro_score_persuasion / total_rebuttals if total_rebuttals > 0 else 0
    con_score_persuasion_normalized = con_score_persuasion / total_rebuttals if total_rebuttals > 0 else 0

    support_pro_count, support_con_count = count_nodes_with_relationship(relationships, "support", entities)
    premise_pro_count, premise_con_count = count_nodes_with_relationship(relationships, "premise", entities)
    rebuttal_pro_count, rebuttal_con_count = count_nodes_with_relationship(relationships, "rebuttal", entities)

    total_nodes = len(entities)

    support_premise_pro_score, support_premise_con_score = normalize_score(
        support_pro_count + premise_pro_count,
        support_con_count + premise_con_count,
        total_nodes
    )

    rebuttal_pro_score, rebuttal_con_score = normalize_score(
        rebuttal_pro_count,
        rebuttal_con_count,
        total_nodes
    )

    total_pro_score_structure = (support_premise_pro_score + rebuttal_pro_score) / 2
    total_con_score_structure = (support_premise_con_score + rebuttal_con_score) / 2



    total_pro_score = pro_score + pro_score_persuasion_normalized + total_pro_score_structure
    total_con_score = con_score + con_score_persuasion_normalized + total_con_score_structure

    if total_pro_score > total_con_score:
        overall_winner = "pro"
    elif total_con_score > total_pro_score:
        overall_winner = "con"
    else:
        overall_winner = "tie"



    print(f"Pro Factual Accuracy Score: {pro_score:.2f}")
    print(f"Con Factual Accuracy Score: {con_score:.2f}")
    print(f"Pro Persuasiveness Score: {pro_score_persuasion_normalized:.2f}")
    print(f"Con Persuasiveness Score: {con_score_persuasion_normalized:.2f}")
    print(f"Pro Argument Structure Score: {total_pro_score_structure:.2f}")
    print(f"Con Argument Structure Score: {total_con_score_structure:.2f}")
    print(f"Overall Pro Score: {total_pro_score:.2f}")
    print(f"Overall Con Score: {total_con_score:.2f}")
    print(f"The overall winner is: {overall_winner}")

    print_feedback(pro_factual_feedback + feedback_pro, "Pro")
    print_feedback(con_factual_feedback + feedback_con, "Con")

    feedback_dict= {"pro": pro_factual_feedback + feedback_pro, "con": con_factual_feedback + feedback_con}

    return overall_winner, feedback_dict


        