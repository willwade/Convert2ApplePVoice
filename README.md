# Convert2ApplePVoice


**Warning: I'm not going to pretend here - if you use this it may break licence terms with TTS systems. Not with Apple - but any other provider. So why have we made this? Because we had to. Simply if a person voice banked with one provider and the provider didnt provide a apple Synth Engine (most of them apart from cereproc) then a client is forced to use software which they cant access to have access to their voice. So this way we make a Apple Personal Voice and all AAC apps have can then play this voice.. Well, thats the idea. Your mileage may vary**


A macOS automation tool that facilitates the creation of Apple Personal Voice using TTS output from another system. This tool automates the Personal Voice training process by extracting text via OCR and playing it back using TTS.

## Features

- OCR-based text extraction using Apple's Vision framework
- Extensive TTS engine support (local and cloud-based)
- Works with Personal Voice's Continuous Recording mode
- Audio routing to system input via virtual audio device
- Privacy-focused: runs entirely on-device with no external data transmission
- Configurable OCR region and TTS settings

## Requirements

- macOS (tested on macOS Sonoma)
- Python 3.10+
- Screen Recording permission for OCR functionality
- BlackHole 2ch or similar virtual audio device
- For eSpeak support: `brew install espeak-ng`
- For cloud-based TTS: Valid API credentials

## Installation

1. Install BlackHole for audio routing:
```bash
brew install blackhole-2ch
```

2. Set up audio routing:
   - Open System Settings > Sound
   - Under Input, select "BlackHole 2ch"
   - Under Output, your regular speakers should be selected

3. Clone this repository:
```bash
git clone https://github.com/yourusername/Convert2ApplePVoice.git
cd Convert2ApplePVoice
```

4. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate
```

5. Install the package in development mode:
```bash
uv pip install -e .
```

6. Grant necessary permissions:
   - Open System Settings > Privacy & Security > Screen Recording
   - Enable permissions for your terminal application

## Audio Setup

The tool needs to route TTS audio to Personal Voice's input. Here's how to set it up:

1. **Install Virtual Audio Device**:
   ```bash
   brew install blackhole-2ch
   ```

2. **Configure System Audio**:
   - Open System Settings > Sound
   - Set Input to "BlackHole 2ch"
   - Set Output to your regular speakers

3. **Optional: Audio Monitoring**
   To hear the TTS output while it's being recorded:
   - Install Audio MIDI Setup (if not already installed)
   - Create a Multi-Output Device:
     1. Open Audio MIDI Setup
     2. Click the + button > Create Multi-Output Device
     3. Check both your speakers and "BlackHole 2ch"
     4. Use this as your system output to hear the TTS

### (Optional)Switching Audio Input Devices

You can programmatically switch between audio input devices using the `switchaudio-osx` command-line tool:

1. Install the tool:
```bash
brew install switchaudio-osx
```

2. Switch to BlackHole:
```bash
SwitchAudioSource -s "BlackHole 2ch" -t input
```

3. Switch back to built-in microphone:
```bash
SwitchAudioSource -s "MacBook Air Microphone" -t input
```

You can also list all available audio devices:
```bash
SwitchAudioSource -a
```

## Usage

1. Open Personal Voice setup in System Settings
2. Enable "Continuous Recording" mode in Personal Voice
3. Run the automation script:
```bash
PYTHONPATH=src uv run -m convert2applevoice
```

4. The script will:
   - Continuously monitor the screen for new phrases
   - Automatically speak each phrase using the configured TTS engine
   - Move to the next phrase when speech is detected

Press Ctrl+C to stop the automation.

## Configuration

The configuration is split into two files in `~/.config/convert2applevoice/`:

### Main Configuration (config.json)

```json
{
    "ocr_region_x": 100,
    "ocr_region_y": 300,
    "ocr_region_width": 800,
    "ocr_region_height": 100,
    "tts_engine": "macos",
    "tts_voice": null,
    "tts_rate": 175,
    "tts_volume": 1.0,
    "tts_pitch": 1.0,
    "tts_extra_options": {},
    "ocr_interval": 0.2,
    "retry_delay": 0.5
}
```

### Credentials Configuration (credentials.json)

```json
{
    "aws_key_id": "your_aws_key",
    "aws_secret_key": "your_aws_secret",
    "aws_region": "us-east-1",
    "azure_key": "your_azure_key",
    "azure_region": "eastus",
    "watson_api_key": "your_watson_key",
    "watson_url": "your_watson_url",
    "elevenlabs_api_key": "your_elevenlabs_key"
}
```

## Supported TTS Engines

The tool supports multiple TTS engines through py3-tts-wrapper:

### Local Engines
- `macos`: Built-in macOS TTS (default)
- `espeak`: Open-source speech synthesizer

### Cloud-based Engines (requires credentials)
- `polly`: Amazon AWS Polly
- `azure`: Microsoft Azure TTS
- `watson`: IBM Watson TTS
- `elevenlabs`: ElevenLabs TTS

### Engine Features

| Engine | Online/Offline | SSML | Rate/Volume/Pitch | Word Events |
|--------|---------------|------|-------------------|-------------|
| macos | Offline | Yes | Yes | No |
| espeak | Offline | Yes | Yes | Yes |
| polly | Online | Yes | Yes | Yes |
| azure | Online | Yes | Yes | Yes |
| watson | Online | Yes | No | Yes |
| elevenlabs | Online | No | Yes | Yes |

### Selecting an Engine

To use a specific engine, set `tts_engine` in your config.json to one of:
- `"macos"` (default)
- `"espeak"`
- `"polly"`
- `"azure"`
- `"watson"`
- `"elevenlabs"`

For cloud-based engines, make sure to add your credentials to credentials.json.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Apple Vision framework for OCR capabilities
- py3-tts-wrapper for TTS engine support
- Various TTS service providers
