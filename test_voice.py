"""Test script to verify Azure TTS voice configuration."""
import json
from tts_wrapper import MicrosoftClient, MicrosoftTTS

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def test_voice():
    # Load credentials
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
        azure_key = creds.get('azure_key')
        azure_region = creds.get('azure_region')

    # Load config
    config = load_config()
    voice = config['tts_extra_options']['voice']
    
    # Create TTS client
    client = MicrosoftClient(credentials=(azure_key, azure_region))
    tts = MicrosoftTTS(client)
    
    # Test text
    text = "Hello! This is a test of the Azure Text-to-Speech voice configuration."
    
    # Generate speech
    print(f"Testing voice: {voice}")
    print("Converting text to speech...")
    
    # Set the voice (extract language code from voice ID)
    lang_code = voice.split('-')[0] + '-' + voice.split('-')[1]  # e.g., "en-GB" from "en-GB-SoniaNeural"
    tts.set_voice(voice, lang_code)
    
    # Create SSML and speak
    ssml_text = tts.ssml.add(text)
    tts.speak_streamed(ssml_text)
    
    print("Test complete! Audio should be playing through the configured output device.")

if __name__ == "__main__":
    test_voice()
