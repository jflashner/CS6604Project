import json
from .models import example_graph

# Prompt Functions
def create_scene_graph_prompt(topic, side, speech):
    base_prompt = f"""
    You are an AI agent tasked with analyzing a debate. The topic of the debate is: "{topic}". 
    You are representing the {side} side. Below is a speech from your side:

    "{speech}"

    Based on this speech without making up new arguments, generate a scene graph in JSON format that includes the following:
    1. Arguments, and relationships that are most relevant to understanding your side's speech and point of view.
    2. Ensure the relations used are one of the following: ["claim", "premise", "conclusion", "first principle", "rebuttal"]
    3. The scene graph should be structured to clearly represent the key points and relationships in the argument.
    4. All ids should be unique

    Here is an example scene graph for climate change, you should follow this format in your generated scene graph:

    "{example_graph}"

    Please provide the scene graph between the markers <SCENE_GRAPH> and </SCENE_GRAPH>
    """

    return base_prompt

def create_counterfactual_scene_graph_prompt(topic, con_speech, pro_scene_graph):
    base_prompt = f"""
    You are an AI agent representing the con side in a debate. The topic of the debate is: "{topic}". 
    Below is a speech from your side:

    "{con_speech}"

    Additionally, here is the current scene graph representing the debate which has just been modified by the pro side:

    {json.dumps(pro_scene_graph, indent=2)}

    Your task is to generate counterfactual argument entities and relationships in the same JSON format that refutes the pro side's arguments and introduces new arguments for the con side. All of your arguments should be based on the given con side speech, do not make up new arguments that are not mentioned in the con side speech. The counterfactual scene graph should include the following:
    1. Arguments, and relationships that directly counter the pro side's scene graph.
    2. Arguments, and relationships that support the con side's arguments.
    3. The scene graph should be structured to clearly represent the key points and relationships in the argument.
    4. Make reference to the pro side's arguments by referencing their ids in the your proposed relations.
    5. Do not include duplicates of the pro side's arguments in your graph when you could instead reference their ids in your relations.
    6. Do not add any new fields to the json which are not in the provided examples.
    7. Source and Target Id should always refer to an integer of an existing argument.
    8. All generated argument ids should be unique from any other id in the current scene graph.
    9. Ensure the relations used are one of the following: ["claim", "premise", "conclusion", "first principle", "rebuttal"]

    Your proposed arguments and relationships will be added to the scene graph to form an update debate graph from which a judge can determine the winner.

    Here is an example another example scene graph for climate change which you can use as reference for the format of your json output:

    "{example_graph}"

    Please provide the counterfactual scene graph between the markers <SCENE_GRAPH> and </SCENE_GRAPH>.

    You should additionally provide a brief explanation of the counterfactual scene graph between the markers <EXPLANATION> and </EXPLANATION>.
    """

    return base_prompt

def create_pro_counterfactual_scene_graph_prompt(topic, pro_speech, con_scene_graph):
    base_prompt = f"""
    You are an AI agent representing the pro side in a debate. The topic of the debate is: "{topic}". 
    Below is a speech from your side:

    "{pro_speech}"

    Additionally, here is the current scene graph representing the debate which has just been modified by the con side:

    {json.dumps(con_scene_graph, indent=2)}

    Your task is to generate counterfactual argument entities and relationships in the same JSON format that refutes the con side's arguments and introduces new arguments for the pro side. All of your arguments should be based on the given pro side speech, do not make up new arguments that are not mentioned in the pro side speech. The counterfactual scene graph should include the following:
    1. Arguments, and relationships that directly counter the con side's scene graph.
    2. Arguments, and relationships that support the pro side's arguments.
    3. The scene graph should be structured to clearly represent the key points and relationships in the argument.
    4. Make reference to the con side's arguments by referencing their ids in the your proposed relations.
    5. Do not include duplicates of the con side's arguments in your graph when you could instead reference their ids in your relations.
    6. Do not add any new fields to the json which are not in the provided examples.
    7. Source and Target Id should always refer to an integer of an existing argument.
    8. All generated argument ids should be unique from any other id in the current scene graph.
    9. Ensure the relations used are one of the following: ["claim", "premise", "conclusion", "first principle", "rebuttal"]

    Your proposed arguments and relationships will be added to the scene graph to form an update debate graph from which a judge can determine the winner.

    Here is an example another example scene graph for climate change which you can use as reference for the format of your json output:

    "{example_graph}"

    Please provide the counterfactual scene graph between the markers <SCENE_GRAPH> and </SCENE_GRAPH>.

    You should additionally provide a brief explanation of the counterfactual scene graph between the markers <EXPLANATION> and </EXPLANATION>.
    """

    return base_prompt

def create_judge_prompt(topic, scene_graph, thoughts_history):
    base_prompt = f"""
    You are an AI judge tasked with evaluating the logical validity of arguments in a debate. The topic of the debate is: "{topic}". 
    Below is the scene graph generated by the pro and con sides:

    Scene Graph:
    {json.dumps(scene_graph, indent=4)}

    Additionally, here is the history of your previous thoughts:
    {thoughts_history}

    Your task is to analyze the logical structure and validity of each side's arguments based on the scene graph. Consider the relationships and attributes in the graph to determine the strength and coherence of the arguments. Provide your reasoning and conclusion wrapped in <thoughts> tags. Based on this analysis and the history of your previous thoughts, decide which side has presented a stronger argument. If the pro side has a stronger argument, write <winner>pro</winner>. If the con side has a stronger argument, write <winner>con</winner>. If both sides are equally strong, write <winner>tie</winner>.

    Please provide your reasoning and conclusion between the markers <thoughts> and </thoughts>, and your decision between the markers <winner> and </winner>.
    """

    return base_prompt