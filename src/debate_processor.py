from .models import DebateGraph
from .prompts import create_scene_graph_prompt, create_pro_counterfactual_scene_graph_prompt, create_counterfactual_scene_graph_prompt, create_judge_prompt
from .utils import generate, extract_scene_graph, extract_thoughts_and_winner, combine_debate_graphs

# Debate Logic
def process_debate(debate):
    topic = debate['motion']['motion']
    pro_speeches = [speech['content'] for speech in debate['speech'] if speech['debater_name'] == debate['motion']['pro_side'][0]['name']]
    con_speeches = [speech['content'] for speech in debate['speech'] if speech['debater_name'] == debate['motion']['con_side'][0]['name']]

    pro_scene_graph = {}
    con_scene_graph = {}
    graph_history = []
    thought_history = ""
    winners = []

    # Iterate over speeches
    for i, (pro_speech, con_speech) in enumerate(zip(pro_speeches, con_speeches)):
        # Generate pro side counterfactual prompt
        if i == 0:
            pro_prompt = create_scene_graph_prompt(topic, 'pro', pro_speech)
            result = None
            while result is None:
                try:
                    pro_response = generate(pro_prompt)
                    result = extract_scene_graph(pro_response)
                    for argument in result.entities:
                        argument.side = "pro"
                except Exception as e:
                    print(e)
                    pass
            scene_graph = result
        else:
            pro_prompt = create_pro_counterfactual_scene_graph_prompt(topic, pro_speech, scene_graph.model_dump())
            result = None
            while result is None:
                try:
                    pro_response = generate(pro_prompt)
                    pro_scene_graph = extract_scene_graph(pro_response)
                    for argument in pro_scene_graph.entities:
                        argument.side = "pro"
                    result = combine_debate_graphs(pro_scene_graph,scene_graph)
                except Exception as e:
                    print
                    pass
            scene_graph = result

        graph_history.append(scene_graph)

        # Generate con side counterfactual prompt
        con_prompt = create_counterfactual_scene_graph_prompt(topic, con_speech, scene_graph.model_dump())
        result = None
        while result is None:
            try:
                con_response = generate(con_prompt)
                con_scene_graph = extract_scene_graph(con_response)
                for argument in con_scene_graph.entities:
                        argument.side = "con"
                result = combine_debate_graphs(con_scene_graph,scene_graph)
            except Exception as e:
                print(e)
                pass
        scene_graph = result

        # Save con scene graph to history
        graph_history.append(scene_graph)

        # Generate judge prompt
        judge_prompt = create_judge_prompt(topic, scene_graph.model_dump(), thought_history)
        judge_response = generate(judge_prompt)
        thoughts, winner = extract_thoughts_and_winner(judge_response)
        thought_history += f"Thought for round {i+1}: {thoughts}\n"
        winners.append(winner)

        struct = {
            "graph_history": graph_history,
            "thoughts": thoughts,
            "winner": winners
        }

    return winner, struct