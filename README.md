# CS6604Project

# Group Members:
1. Joshua Flashner
2. Priya Pitre
3. Prayash Joshi
4. Evar Jones

#Project Description
Generate a debate graph capturing the argumentative structure of real debates. 
The generated graph can be used to score each debater and determine a final winner.

# Environment Setup
Run pip install -r requirements.txt

To run code OpenAI API key is required to be set in the environment variable OPENAI_API_KEY.

# Instructions
data/ contains a sample of the data from DebateArt and BP-Competition which can be used for testing.

To run evaluation on sample data, run all cells in benchmark_eval.ipynb.
Results for DebateArt are saved to debate_results_sample/ and BP-Competition results are saved to debate_results_bp/