# Convert2ApplePVoice

A macOS automation tool that facilitates the creation of Apple Personal Voice using TTS output from another system. This tool automates the Personal Voice training process by extracting text via OCR and playing it back using TTS.

## Features

- OCR-based text extraction using Apple's Vision framework
- Automated UI interaction with Personal Voice interface
- TTS playback of extracted prompts
- Fully automated workflow with customizable delays
- Privacy-focused: runs entirely on-device with no external data transmission

## Requirements

- macOS (tested on macOS Sonoma)
- Python 3.10+
- Accessibility permissions enabled for script execution

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Convert2ApplePVoice.git
cd Convert2ApplePVoice
```

2. Install dependencies using uv:
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

3. Grant necessary permissions:
   - Open System Settings > Privacy & Security > Accessibility
   - Enable permissions for your terminal application
   - Enable permissions for System Settings

## Usage

1. Open Personal Voice setup in System Settings
2. Run the automation script:
```bash
python src/main.py
```

3. The script will:
   - Extract text from the Personal Voice UI
   - Automate button clicks
   - Play back the extracted text using TTS
   - Continue until all prompts are processed

## Configuration

Edit `config.py` to adjust:
- Delay timings
- OCR settings
- TTS voice settings
- UI automation parameters

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Apple Vision framework for OCR capabilities
- macOS Accessibility features for UI automation
