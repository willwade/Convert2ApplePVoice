"""Configuration settings for Convert2ApplePVoice."""

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Optional, Dict, Any

@dataclass
class AudioConfig:
    """Audio device configuration."""
    output_device: Optional[str] = "BlackHole 2ch"  # Default to BlackHole
    enable_monitoring: bool = False  # Whether to enable audio monitoring
    monitoring_device: Optional[str] = None  # Device for monitoring (if enabled)

@dataclass
class TTSCredentials:
    """Credentials for TTS services."""
    # AWS Polly
    aws_key_id: Optional[str] = None
    aws_secret_key: Optional[str] = None
    aws_region: str = "us-east-1"
    
    # Azure
    azure_key: Optional[str] = None
    azure_region: str = "eastus"
    
    # Watson
    watson_api_key: Optional[str] = None
    watson_url: Optional[str] = None
    
    # ElevenLabs
    elevenlabs_api_key: Optional[str] = None

@dataclass
class Config:
    """Configuration settings."""
    
    # OCR settings
    ocr_region_x: int = 100
    ocr_region_y: int = 300  # Adjusted for typical Personal Voice UI
    ocr_region_width: int = 800
    ocr_region_height: int = 100
    
    # TTS settings
    tts_engine: str = "macos"  # Name of TTS engine to use
    tts_voice: Optional[str] = None  # Voice name/id
    tts_rate: int = 175  # Words per minute
    tts_volume: float = 1.0  # Volume level (0.0 to 1.0)
    tts_pitch: float = 1.0  # Pitch multiplier
    tts_extra_options: Dict[str, Any] = field(default_factory=dict)  # Engine-specific options
    
    # Audio settings
    audio: AudioConfig = field(default_factory=AudioConfig)
    
    # TTS service credentials
    tts_credentials: TTSCredentials = field(default_factory=TTSCredentials)
    
    # Timing settings
    ocr_interval: float = 0.2  # Seconds between OCR checks
    retry_delay: float = 0.5   # Seconds to wait after failed OCR
    check_interval: float = 0.5  # seconds
    retry_delay_timing: float = 1.0  # seconds
    
    def __post_init__(self):
        """Load custom config if it exists."""
        self._load_config()
        self._load_credentials()
    
    def _load_config(self):
        """Load main configuration file."""
        config_path = Path.home() / ".config" / "convert2applevoice" / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    custom_config = json.load(f)
                    # Handle audio config separately
                    if "audio" in custom_config:
                        for key, value in custom_config["audio"].items():
                            if hasattr(self.audio, key):
                                setattr(self.audio, key, value)
                        del custom_config["audio"]
                    
                    # Load other config options
                    for key, value in custom_config.items():
                        if key != "tts_credentials" and hasattr(self, key):
                            setattr(self, key, value)
            except Exception as e:
                print(f"Error loading config: {str(e)}")
    
    def _load_credentials(self):
        """Load TTS service credentials from separate file."""
        creds_path = Path.home() / ".config" / "convert2applevoice" / "credentials.json"
        if creds_path.exists():
            try:
                with open(creds_path) as f:
                    creds_data = json.load(f)
                    for key, value in creds_data.items():
                        if hasattr(self.tts_credentials, key):
                            setattr(self.tts_credentials, key, value)
            except Exception as e:
                print(f"Error loading credentials: {str(e)}")

    def save(self):
        """Save current configuration to files."""
        config_dir = Path.home() / ".config" / "convert2applevoice"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Save main config
        config_dict = {
            key: value for key, value in self.__dict__.items()
            if not key.startswith("_") and key not in ["tts_credentials", "audio"]
        }
        # Add audio config
        config_dict["audio"] = {
            key: value for key, value in vars(self.audio).items()
            if not key.startswith("_")
        }
        
        try:
            with open(config_dir / "config.json", "w") as f:
                json.dump(config_dict, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {str(e)}")
        
        # Save credentials separately
        creds_dict = {
            key: value for key, value in vars(self.tts_credentials).items()
            if value is not None  # Only save non-None credentials
        }
        
        if creds_dict:  # Only save if there are credentials
            try:
                with open(config_dir / "credentials.json", "w") as f:
                    json.dump(creds_dict, f, indent=4)
            except Exception as e:
                print(f"Error saving credentials: {str(e)}")
