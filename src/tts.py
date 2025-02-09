"""TTS module for playing back extracted text."""

import subprocess
import time

class TTSPlayer:
    """Handles text-to-speech playback using macOS say command."""

    def __init__(self, voice: str = None, rate: int = 175):
        """Initialize the TTS player.
        
        Args:
            voice: Name of the voice to use. If None, system default is used.
            rate: Speech rate in words per minute.
        """
        self.voice = voice
        self.rate = rate

    def speak(self, text: str) -> bool:
        """Speak the given text using TTS.
        
        Args:
            text: The text to speak.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            cmd = ["say"]
            if self.voice:
                cmd.extend(["-v", self.voice])
            cmd.extend(["-r", str(self.rate)])
            cmd.append(text)

            # Run the say command and wait for it to complete
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Add a small delay after speaking
            time.sleep(0.5)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"TTS error: {e.stderr}")
            return False
