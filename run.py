from src.debate_manager import DebateManager

manager = DebateManager("config/data_config.yaml", debate_format="bp_competition")
manager.load_and_print_debate('003')  # Replace '003' with an actual debate ID from your dataset
