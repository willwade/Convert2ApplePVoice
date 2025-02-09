"""TTS package for Convert2ApplePVoice."""

from .base import TTSEngine, TTSConfig
from .factory import create_engine, get_available_engines
from .macos import MacOSTTS

__all__ = [
    'TTSEngine',
    'TTSConfig',
    'create_engine',
    'get_available_engines',
    'MacOSTTS',
]
