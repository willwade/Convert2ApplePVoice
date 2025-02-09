"""Base interface for TTS engines."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class TTSConfig:
    """Configuration for TTS engines."""
    voice: Optional[str] = None
    rate: int = 175
    volume: float = 1.0
    pitch: float = 1.0
    extra_options: Dict[str, Any] = None

    def __post_init__(self):
        if self.extra_options is None:
            self.extra_options = {}

class TTSEngine(ABC):
    """Abstract base class for TTS engines."""
    
    @abstractmethod
    def speak(self, text: str) -> bool:
        """Speak the given text.
        
        Args:
            text: The text to speak
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_available_voices(self) -> list[str]:
        """Get list of available voices.
        
        Returns:
            list[str]: List of voice names/identifiers
        """
        pass
    
    @abstractmethod
    def is_speaking(self) -> bool:
        """Check if the engine is currently speaking.
        
        Returns:
            bool: True if speaking, False otherwise
        """
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """Stop any current speech."""
        pass
