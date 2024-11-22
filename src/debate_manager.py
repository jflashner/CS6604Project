from .loader.panel_bench import PanelBenchLoader

class DebateManager:
    """Handles debate operations and data loading."""

    def __init__(self, config_path: str, debate_format: str):
        """Initialize the DebateManager with the given configuration."""
        self.config = self._load_config(config_path)
        print("Loaded Config:", self.config)
        self.loader = PanelBenchLoader(self.config, debate_format)

    def _load_config(self, config_path: str):
        """Load the YAML configuration file."""
        import yaml
        try:
            with open(config_path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Failed to load config: {e}")
            return {}

    def load_and_print_debate(self, debate_id: str):
        """For validation."""
        debate_data = self.loader.load_debate(debate_id)
        # Print out key components for validation
        print(f"\n--- Debate {debate_id} ---")
        print(f"Motion: {debate_data['motion']}")
        print(f"Speech: {debate_data['speech']}")
        if debate_data['gold']:
            print(f"Gold Standard: {debate_data['gold']}")
        else:
            print("No gold standard available.")
    
    def load_debate(self, debate_id: str):
        """Load the debate data."""
        return self.loader.load_debate(debate_id)
