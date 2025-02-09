"""TTS implementation using py3-tts-wrapper library."""

from typing import Optional, Dict, Any, Tuple
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
        """Get Azure credentials from config.
        
        Returns:
            Optional[Tuple[str, str]]: (subscription_key, subscription_region) or None
        """
        if not hasattr(self.config, 'tts_credentials'):
            return None
            
        key = getattr(self.config.tts_credentials, 'azure_key', None)
        region = getattr(self.config.tts_credentials, 'azure_region', None)
        
        if key and region:
            return (key, region)
        return None
    
    def _setup_engine(self):
        """Set up the TTS engine based on configuration."""
        try:
            engine_type = self.config.extra_options.get('engine_type', 'espeak')
            
            # Import the appropriate client and TTS classes
            if engine_type == 'polly':
                from tts_wrapper import PollyClient, PollyTTS
                aws_key = getattr(self.config.tts_credentials, 'aws_key_id', None)
                aws_secret = getattr(self.config.tts_credentials, 'aws_secret_key', None)
                if aws_key and aws_secret:
                    self._client = PollyClient(credentials=(aws_key, aws_secret))
                    self._engine = PollyTTS(self._client)
            
            elif engine_type == 'watson':
                from tts_wrapper import WatsonClient, WatsonTTS
                api_key = getattr(self.config.tts_credentials, 'watson_api_key', None)
                url = getattr(self.config.tts_credentials, 'watson_url', None)
                if api_key and url:
                    self._client = WatsonClient(credentials=(api_key, url))
                    self._engine = WatsonTTS(self._client)
            
            elif engine_type == 'azure':
                from tts_wrapper import MicrosoftClient, MicrosoftTTS
                azure_creds = self._get_azure_credentials()
                if azure_creds:
                    self._client = MicrosoftClient(credentials=azure_creds)
                    self._engine = MicrosoftTTS(self._client)
                else:
                    print("Error: Azure credentials not found in config")
            
            elif engine_type == 'elevenlabs':
                from tts_wrapper import ElevenLabsClient, ElevenLabsTTS
                api_key = getattr(self.config.tts_credentials, 'elevenlabs_api_key', None)
                if api_key:
                    self._client = ElevenLabsClient(credentials=api_key)
                    self._engine = ElevenLabsTTS(self._client)
            
            else:  # default to espeak
                from tts_wrapper import ESpeakTTS
                self._engine = ESpeakTTS()
            
            if self._engine:
                # Configure audio output device if specified
                if hasattr(self.config, 'audio') and self.config.audio.output_device:
                    self._engine.set_output_device(self.config.audio.output_device)
                
                # Set engine properties if supported
                if hasattr(self._engine, 'set_property'):
                    if self.config.rate is not None:
                        self._engine.set_property('rate', self.config.rate)
                    if self.config.volume is not None:
                        self._engine.set_property('volume', self.config.volume)
                    if self.config.pitch is not None:
                        self._engine.set_property('pitch', self.config.pitch)
                    if self.config.voice is not None:
                        self._engine.set_property('voice', self.config.voice)
            
        except Exception as e:
            print(f"Error setting up TTS engine: {str(e)}")
            self._engine = None
    
    def speak(self, text: str) -> bool:
        """Speak the given text.
        
        Args:
            text: Text to speak
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._engine:
            return False
            
        try:
            # Use streamed speech for better real-time performance
            self._engine.speak_streamed(text)
            return True
        except Exception as e:
            print(f"Error speaking text: {str(e)}")
            return False
    
    def get_available_voices(self) -> list[str]:
        """Get list of available voices.
        
        Returns:
            list[str]: List of voice names/identifiers
        """
        if not self._engine:
            return []
            
        try:
            return self._engine.get_voices()
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
    
    def stop(self) -> None:
        """Stop current speech."""
        if self._engine and hasattr(self._engine, 'stop_audio'):
            try:
                self._engine.stop_audio()
            except Exception as e:
                print(f"Error stopping speech: {str(e)}")
