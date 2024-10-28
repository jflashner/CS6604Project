import logging
import os
from openai import OpenAI
from prompts import create_one_example

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debate.log',level=logging.INFO)

struct = {'topic': 'The debate centers on whether elementary school students should be assigned homework. Proponents argue that homework reinforces learning and builds responsibility, while opponents believe it can burden young students, detracting from valuable free time for rest, play, and family interaction. This discussion explores the impact of homework on academic success, emotional well-being, and development.',
          'context': ['Ms. Carter, a fifth-grade teacher with over a decade of experience, argues in favor of homework for elementary students. She believes that small, manageable homework assignments help reinforce what students learn in class, fostering essential skills like responsibility and time management. According to Ms. Carter, a structured homework routine also gives students a chance to review and practice material, helping them develop confidence in their abilities. By building these habits early, she contends, students gain a strong foundation for future academic success, ensuring they feel prepared for the increasing demands of middle and high school.',
                      'Mr. Jackson, a child psychologist and former teacher, contends that elementary students should not have homework. He argues that the school day is already structured with ample time for learning, and young children benefit more from unstructured play, family time, and rest after school. According to Mr. Jackson, homework can cause stress and diminish students’ natural enthusiasm for learning, while time spent playing or engaging in other interests allows for social and emotional development that is crucial at this stage. He believes that children develop a more positive attitude toward school when it doesn’t intrude into their home lives, supporting a balanced approach to early education.'],
          'kg': ['', '']
          }

def generate(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def init_prompt_multi(struct, input_format):
    return create_one_example(input_format, struct['topic'], struct['context'], struct['kg'])

debate = 2

for debate_ in range(debate):
    logger.info("########--DEBATE{}--######".format(debate_))
    if debate_ == 0:
            prompt_format = "gen_graph"
            prompt_G = init_prompt_multi(struct, prompt_format)
            kg_base = generate(prompt=prompt_G)
            struct['kg'] = [kg_base, kg_base]
            logger.info("#####---KG_P---#####\n{}".format(prompt_G))
            logger.info("#####---KG_B---#####\n{}".format(kg_base))

    prompt_format = "neg_iter"
    prompt_A = init_prompt_multi(struct, prompt_format)
    kg_neg = generate(prompt=prompt_A)
    struct['kg'] = [struct['kg'][0],kg_neg]
    logger.info("#####---NEG_ITER---#####\n{}".format(prompt_A))

    prompt_format = "aff_iter"
    prompt_N = init_prompt_multi(struct, prompt_format)
    kg_aff = generate(prompt=prompt_N)
    struct['kg'] = [kg_aff, kg_neg]
    logger.info("#####---AFF_ITER---#####\n{}".format(prompt_N))

    prompt_format =  "judge"
    prompt_F = init_prompt_multi(struct, prompt_format)
    response = generate(prompt=prompt_F)
    logger.info("#####---JUDGE---#####\n{}".format(prompt_F))
    
    logger.info("########--ANSWER-{}--######\n{}".format(debate_, response))

logger.info("\nANS: {} - ".format(response))