"""Configuration settings for Convert2ApplePVoice."""

from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class Config:
    """Configuration settings."""
    
    # OCR settings
    ocr_region_x: int = 100
    ocr_region_y: int = 100
    ocr_region_width: int = 800
    ocr_region_height: int = 100
    
    # TTS settings
    tts_voice: str = None  # Use system default
    tts_rate: int = 175  # Words per minute
    
    # UI automation settings
    button_click_delay: float = 1.0  # Seconds to wait after clicking buttons
    
    def __post_init__(self):
        """Load custom config if it exists."""
        config_path = Path.home() / ".config" / "convert2applevoice" / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    custom_config = json.load(f)
                    for key, value in custom_config.items():
                        if hasattr(self, key):
                            setattr(self, key, value)
            except Exception as e:
                print(f"Error loading config: {str(e)}")

    def save(self):
        """Save current configuration to file."""
        config_path = Path.home() / ".config" / "convert2applevoice" / "config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        config_dict = {
            key: value for key, value in self.__dict__.items()
            if not key.startswith("_")
        }
        
        try:
            with open(config_path, "w") as f:
                json.dump(config_dict, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {str(e)}")
