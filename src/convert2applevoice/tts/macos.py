"""macOS system TTS implementation."""

import subprocess
from typing import Optional
from .base import TTSEngine, TTSConfig

class MacOSTTS(TTSEngine):
    """TTS engine using macOS 'say' command."""
    
    def __init__(self, config: Optional[TTSConfig] = None):
        """Initialize the TTS engine.
        
        Args:
            config: TTS configuration
        """
        self.config = config or TTSConfig()
        self._current_process: Optional[subprocess.Popen] = None
    
    def speak(self, text: str) -> bool:
        """Speak text using macOS say command.
        
        Args:
            text: Text to speak
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Stop any current speech
            self.stop()
            
            cmd = ["say"]
            if self.config.voice:
                cmd.extend(["-v", self.config.voice])
            if self.config.rate:
                cmd.extend(["-r", str(self.config.rate)])
            cmd.append(text)
            
            self._current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            return True
            
        except Exception as e:
            print(f"MacOS TTS error: {str(e)}")
            return False
    
    def get_available_voices(self) -> list[str]:
        """Get list of available system voices.
        
        Returns:
            list[str]: List of voice names
        """
        try:
            result = subprocess.run(
                ["say", "-v", "?"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse voice names from output
            voices = []
            for line in result.stdout.splitlines():
                if line.strip():
                    voice_name = line.split()[0]
                    voices.append(voice_name)
            
            return voices
            
        except Exception as e:
            print(f"Error getting voices: {str(e)}")
            return []
    
    def is_speaking(self) -> bool:
        """Check if currently speaking.
        
        Returns:
            bool: True if speaking, False otherwise
        """
        if self._current_process is None:
            return False
            
        # Check if process is still running
        return self._current_process.poll() is None
    
    def stop(self) -> None:
        """Stop current speech."""
        if self._current_process and self.is_speaking():
            self._current_process.terminate()
            self._current_process = None
