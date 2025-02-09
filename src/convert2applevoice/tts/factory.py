"""Factory for creating TTS engine instances."""

from typing import Optional, Type
from .base import TTSEngine, TTSConfig
from .macos import MacOSTTS
from .wrapper import WrapperTTS

# Registry of available TTS engines
TTS_ENGINES = {
    'macos': MacOSTTS,
    'espeak': lambda config: WrapperTTS(TTSConfig(
        voice=config.voice,
        rate=config.rate,
        volume=config.volume,
        pitch=config.pitch,
        extra_options={'engine_type': 'espeak'}
    )),
    'polly': lambda config: WrapperTTS(TTSConfig(
        voice=config.voice,
        rate=config.rate,
        volume=config.volume,
        pitch=config.pitch,
        extra_options={'engine_type': 'polly'}
    )),
    'watson': lambda config: WrapperTTS(TTSConfig(
        voice=config.voice,
        rate=config.rate,
        volume=config.volume,
        pitch=config.pitch,
        extra_options={'engine_type': 'watson'}
    )),
    'azure': lambda config: WrapperTTS(TTSConfig(
        voice=config.voice,
        rate=config.rate,
        volume=config.volume,
        pitch=config.pitch,
        extra_options={'engine_type': 'azure', **config.extra_options}
    )),
    'elevenlabs': lambda config: WrapperTTS(TTSConfig(
        voice=config.voice,
        rate=config.rate,
        volume=config.volume,
        pitch=config.pitch,
        extra_options={'engine_type': 'elevenlabs'}
    )),
}

def create_engine(engine_name: str, config: Optional[TTSConfig] = None) -> Optional[TTSEngine]:
    """Create a TTS engine instance.
    
    Args:
        engine_name: Name of the engine to create
        config: Optional configuration for the engine
        
    Returns:
        TTSEngine: Instance of the requested engine, or None if not found
    """
    engine_factory = TTS_ENGINES.get(engine_name.lower())
    if engine_factory:
        if callable(engine_factory):
            return engine_factory(config)
        return engine_factory(config)
    return None

def get_available_engines() -> list[str]:
    """Get list of available TTS engine names.
    
    Returns:
        list[str]: List of engine names
    """
    return list(TTS_ENGINES.keys())
