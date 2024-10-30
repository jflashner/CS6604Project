from pathlib import Path
from typing import Dict, Any, Optional, List
import yaml
import pandas as pd

class defaultLoader:
    
    def __init__(self, format_config: Dict[str, Any]):
        """Initialize loader with format-specific configuration."""
        self.config = format_config  # This now only holds format-specific settings
        self.base_path = Path(self.config['data_dir'])  # Access 'data_dir' from format-specific config
    
    def load_yaml(self, path: Path) -> Dict[str, Any]:
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return {}
    
    def get_file_path(self, format_str: str, **kwargs) -> Path:
        return self.base_path / format_str.format(**kwargs)

class PanelBenchLoader(defaultLoader):
    """Loader for PanelBench dataset"""

    def __init__(self, config: Dict[str, Any], debate_format: str):
        # Ensure 'datasets' key exists
        if 'datasets' not in config:
            raise ValueError("Config missing 'datasets' key")

        datasets_config = config['datasets']
        if debate_format not in datasets_config:
            raise ValueError(f"Invalid debate format: {debate_format}")

        format_config = datasets_config[debate_format]
        self.debate_format = debate_format  # Store debate format
        super().__init__(format_config)
        
    def load_debate(self, debate_id: str) -> Dict[str, Any]:
        # Load motion
        motion_path = self.get_file_path(self.config['formats']['motion'], id=debate_id)
        motion_data = self.load_yaml(motion_path)

        # Load speech
        speech_path = self.get_file_path(self.config['formats']['speech'], id=debate_id)
        speech_data = self.load_yaml(speech_path)

        # Load gold standard (if exists)
        gold_data = None
        if 'gold' in self.config['formats']:
            gold_path = self.get_file_path(self.config['formats']['gold'])
            if gold_path.exists():
                gold_df = pd.read_csv(gold_path)
                gold_data = gold_df[gold_df['bp_id'] == debate_id].to_dict('records')

        return {
            'id': debate_id,
            'format': self.debate_format,
            'motion': motion_data,
            'speech': speech_data,
            'gold': gold_data
        }
    
    def get_debate_ids(self) -> List[str]:
        pattern = self.config['formats']['motion'].split('{id}')[0] + '*'
        paths = list(self.base_path.glob(pattern))
        return [p.stem.split('_')[-1] for p in paths]

    def load_all_debates(self) -> List[Dict[str, Any]]:
        debate_ids = self.get_debate_ids()
        return [self.load_debate(id) for id in debate_ids]
