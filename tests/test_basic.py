"""Basic tests for Convert2ApplePVoice components."""

import pytest
from pathlib import Path

from src.config import Config
from src.tts import TTSPlayer
from src.ui_automation import UIController

def test_config_defaults():
    """Test that config loads with default values."""
    config = Config()
    assert config.ocr_region_x == 100
    assert config.ocr_region_y == 100
    assert config.tts_rate == 175
    assert config.button_click_delay == 1.0

def test_tts_player():
    """Test TTS player initialization."""
    player = TTSPlayer()
    assert player.voice is None
    assert player.rate == 175

    custom_player = TTSPlayer(voice="Alex", rate=200)
    assert custom_player.voice == "Alex"
    assert custom_player.rate == 200

def test_ui_controller():
    """Test UI controller initialization."""
    controller = UIController()
    scripts_dir = Path(controller.scripts_dir)
    
    assert scripts_dir.exists()
    assert (scripts_dir / "click_record.scpt").exists()
    assert (scripts_dir / "click_continue.scpt").exists()
