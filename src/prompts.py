def create_one_example(input_format, topic, context, knowledge):   
    aff_base = f"You are a fellow debater from the AFFIRMATIVE side, You are Rational in thinking about problems. You are debateing the topic: {topic}. You will take the following argument as your own and should stick closely to it: {context[0]}"
    neg_base = f"You are a fellow debater from the NEGATIVE side, You are Rational in thinking about problems. You are debateing the topic: {topic}. You will take the following argument as your own and should stick closely to it: {context[1]}"

    kg_emo = knowledge[0]
    kg_rat = knowledge[1]
  
    if input_format == "gen_graph":
        input = f"""{aff_base}
        For the provided argument. generate a scene graph in JSON format that includes the following:
        1. Objects, attributes, relationships that are more relevant to understaning the core argument.
        2. Objects are NO MORE THAN 3. 
        """
        
    elif input_format == "aff_iter":
        input = f"""{aff_base} 
        Generate an updated graph from your own view based on the following Argument Graph in JSON format that includes the following:
        1. Objects, attributes, relationships that are more relevant to understaning the core argument.
        2. Delete the irrelevant objects, attributes and relationships.
        {kg_rat}
        """ 

#   elif input_format == "KDQIM":
#       input = f"""{aff_base} 
#       For the provided argument, Please give your solution and ideas to solve this problem, but do not give a final answer. Generate an updated graph from a different view based on the Debate Graph in JSON format that includes the following:
#       1. Objects, attributes, relationships that are more relevant to understaning the core argument.
#       2. Delete the irrelevant objects, attributes and relationships.
#       {hint}{question_}{kg_rat}
#       """ 
        
    elif input_format == "neg_iter":
        input = f"""{neg_base} 
        Generate an updated graph from your own view based on the following Argument Graph in JSON format that includes the following:
        1. Objects, attributes, relationships that are more relevant to understaning the core argument.
        2. Delete the irrelevant objects, attributes and relationships.
        {kg_emo}
        """ 

#    elif input_format == "KNQIM":
#        input = f"""{neg_base} 
#        For the provided image and its associated question, Please give your solution and ideas to solve this problem, but do not give a final answer. Generate an updated graph from a different view based on the Debate Graph in JSON format that includes the following:
#        1. Objects, attributes, relationships that are more relevant to answering the question.
#        2. Delete the irrelevant objects, attributes and relationships.
#        {hint}{question_}{kg_emo}
#        """ 
        
    elif input_format == "judge":
        input = f"""
        You're good at judging debates based on factual arguments and structured information.\nAffirmative side: {kg_emo}\nNegative side: {kg_rat}\n Use the two Argument Graphs representing both sides of the debate and determine the winner. Respond with just the winner. Winner: 
        """
        
    text = input
    text = text.replace("  ", " ")
    return text
