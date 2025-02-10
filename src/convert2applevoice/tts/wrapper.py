"""TTS implementation using py3-tts-wrapper library."""

import json
import os
from typing import Optional, Dict, Any, Tuple, List
from .base import TTSEngine, TTSConfig
from ..audio import AudioManager

class WrapperTTS(TTSEngine):
    """TTS engine using py3-tts-wrapper library."""
    
    def __init__(self, config: Optional[TTSConfig] = None):
        """Initialize the TTS engine.
        
        Args:
            config: TTS configuration
        """
        self.config = config or TTSConfig()
        self._engine = None
        self._client = None
        self._setup_engine()
        
        # Set up audio routing
        if hasattr(self.config, 'audio'):
            success, message = AudioManager.setup_audio_routing(self.config)
            if not success:
                print(f"Warning: {message}")
    
    def _get_azure_credentials(self) -> Optional[Tuple[str, str]]:
        """Get Azure credentials from credentials.json.
        
        Returns:
            Optional[Tuple[str, str]]: (subscription_key, subscription_region) or None
        """
        try:
            creds_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'credentials.json')
            with open(creds_path, 'r') as f:
                creds = json.load(f)
                return (creds['azure_key'], creds['azure_region'])
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            print(f"Error loading Azure credentials: {str(e)}")
            return None
    
    def _setup_engine(self):
        """Set up the TTS engine based on configuration."""
        try:
            engine_type = self.config.extra_options.get('engine_type', 'espeak')
            
            # Import the appropriate client and TTS classes
            if engine_type == 'azure':
                from tts_wrapper import MicrosoftClient, MicrosoftTTS
                azure_creds = self._get_azure_credentials()
                if not azure_creds:
                    raise ValueError("Azure credentials not found in credentials.json")
                    
                key, region = azure_creds
                self._client = MicrosoftClient(credentials=(key, region))
                self._engine = MicrosoftTTS(self._client)
                
                # Set voice after initialization
                if self.config.voice:
                    self._engine.set_voice(self.config.voice, 'en-GB')
                
            elif engine_type == 'polly':
                from tts_wrapper import PollyClient, PollyTTS
                aws_key = getattr(self.config.tts_credentials, 'aws_key_id', None)
                aws_secret = getattr(self.config.tts_credentials, 'aws_secret_key', None)
                aws_region = getattr(self.config.tts_credentials, 'aws_region', 'us-east-1')
                
                if aws_key and aws_secret:
                    self._client = PollyClient(credentials=(aws_key, aws_secret, aws_region))
                    self._engine = PollyTTS(self._client)
                else:
                    raise ValueError("AWS credentials not found")
                    
            elif engine_type == 'watson':
                from tts_wrapper import WatsonClient, WatsonTTS
                api_key = getattr(self.config.tts_credentials, 'watson_api_key', None)
                url = getattr(self.config.tts_credentials, 'watson_url', None)
                
                if api_key and url:
                    self._client = WatsonClient(credentials=(api_key, url))
                    self._engine = WatsonTTS(self._client)
                else:
                    raise ValueError("Watson credentials not found")
                    
            elif engine_type == 'elevenlabs':
                from tts_wrapper import ElevenLabsClient, ElevenLabsTTS
                api_key = getattr(self.config.tts_credentials, 'elevenlabs_api_key', None)
                
                if api_key:
                    self._client = ElevenLabsClient(credentials=(api_key,))
                    self._engine = ElevenLabsTTS(self._client)
                else:
                    raise ValueError("ElevenLabs API key not found")
                    
            else:  # espeak
                from tts_wrapper import EspeakClient, EspeakTTS
                self._client = EspeakClient()
                self._engine = EspeakTTS(self._client)
                
        except ImportError as e:
            raise ImportError(f"Failed to import TTS engine: {str(e)}")
        except Exception as e:
            raise Exception(f"Error setting up TTS engine: {str(e)}")
    
    def speak(self, text: str):
        """Speak the given text.
        
        Args:
            text: Text to speak
        """
        if not self._engine:
            raise RuntimeError("TTS engine not initialized")
            
        # Convert to SSML if it's not already
        if not text.startswith('<speak>'):
            text = self._engine.ssml.add(text)
            
        self._engine.speak(text)
    
    def speak_streamed(self, text: str):
        """Speak the given text with streaming.
        
        Args:
            text: Text to speak
        """
        if not self._engine:
            raise RuntimeError("TTS engine not initialized")
            
        # Convert to SSML if it's not already
        if not text.startswith('<speak>'):
            text = self._engine.ssml.add(text)
            
        self._engine.speak_streamed(text)
    
    def stop(self):
        """Stop current speech."""
        if self._engine:
            self._engine.stop()
            
    def get_voices(self) -> Dict[str, Any]:
        """Get available voices.
        
        Returns:
            Dict[str, Any]: Dictionary of available voices
        """
        if not self._engine:
            raise RuntimeError("TTS engine not initialized")
            
        return self._engine.get_voices()

    def get_available_voices(self) -> List[str]:
        """Get list of available voices.
        
        Returns:
            List[str]: List of voice names/identifiers
        """
        if not self._engine:
            return []
            
        try:
            voices = self._engine.get_voices()
            return list(voices.keys()) if isinstance(voices, dict) else list(voices)
        except Exception as e:
            print(f"Error getting voices: {str(e)}")
            return []
    
    def is_speaking(self) -> bool:
        """Check if currently speaking.
        
        Returns:
            bool: True if speaking, False otherwise
        """
        # Not all engines support this, so we'll assume it's not speaking
        return False
