"""Configuration management."""

import json
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuration manager."""
    
    def __init__(self, config_file: str = 'config.json'):
        """Initialize configuration.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = Path(config_file)
        self._load_config()
        
    def _load_config(self):
        """Load configuration from file."""
        if not self.config_file.exists():
            self._create_default_config()
            
        with open(self.config_file) as f:
            config = json.load(f)
            
        # TTS settings
        self.tts_engine = config.get('tts_engine', 'azure')
        self.tts_voice = config.get('tts_voice', 'en-GB-SoniaNeural')
        self.tts_rate = config.get('tts_rate', 175)
        self.tts_volume = config.get('tts_volume', 1.0)
        self.tts_pitch = config.get('tts_pitch', 1.0)
        self.tts_extra_options = config.get('tts_extra_options', {})
        
        # Audio settings
        self.audio = config.get('audio', {
            'output_device': 'BlackHole 2ch',
            'enable_monitoring': True,
            'monitoring_device': None
        })
        
        # OCR settings
        self.ocr = config.get('ocr', {
            'region': {
                'x': 400,
                'y': 400,
                'width': 600,
                'height': 60
            }
        })
        
        # Timing settings
        self.check_interval = config.get('check_interval', 0.5)  # seconds
        self.retry_delay = config.get('retry_delay', 1.0)  # seconds
        
    def _create_default_config(self):
        """Create default configuration file."""
        default_config = {
            'tts_engine': 'azure',
            'tts_voice': 'en-GB-SoniaNeural',
            'tts_rate': 175,
            'tts_volume': 1.0,
            'tts_pitch': 1.0,
            'tts_extra_options': {
                'engine_type': 'azure',
                'voice': 'en-GB-SoniaNeural',
                'style': 'General'
            },
            'audio': {
                'output_device': 'BlackHole 2ch',
                'enable_monitoring': True,
                'monitoring_device': None
            },
            'ocr': {
                'region': {
                    'x': 400,
                    'y': 400,
                    'width': 600,
                    'height': 60
                }
            },
            'check_interval': 0.5,  # seconds
            'retry_delay': 1.0,  # seconds
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
