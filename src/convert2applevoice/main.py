#!/usr/bin/env python3
"""Main entry point for Convert2ApplePVoice automation."""

import sys
import time
from pathlib import Path
from rich import print
from rich.console import Console

from convert2applevoice.ocr import OCRExtractor
from convert2applevoice.tts import create_engine, TTSConfig
from convert2applevoice.config import Config

console = Console()

def main():
    """Main automation loop for Personal Voice creation."""
    try:
        config = Config()
        ocr = OCRExtractor(region=config.ocr.get('region'))
        
        # Create TTS engine with config
        tts_config = TTSConfig(
            voice=config.tts_voice,
            rate=config.tts_rate,
            volume=config.tts_volume,
            pitch=config.tts_pitch,
        )
        tts_config.extra_options = config.tts_extra_options
        tts = create_engine(config.tts_engine, tts_config)
        
        if not tts:
            console.print(f"[bold red]Error: TTS engine '{config.tts_engine}' not found[/bold red]")
            sys.exit(1)

        console.print("[bold green]Starting Personal Voice automation...[/bold green]")
        console.print("[yellow]Make sure Personal Voice is in Continuous Recording mode[/yellow]")
        console.print("[yellow]Press Ctrl+C to stop[/yellow]")
        
        last_text = ""
        waiting_for_focus = False
        
        while True:
            # Extract text from current prompt
            text = ocr.extract_text()
            
            # If text is empty and we weren't previously waiting for focus
            if not text and not waiting_for_focus:
                console.print("[yellow]Waiting for Personal Voice window to be focused...[/yellow]")
                waiting_for_focus = True
            # If we have text and we were waiting for focus
            elif text and waiting_for_focus:
                console.print("[green]Personal Voice window detected![/green]")
                waiting_for_focus = False
            
            # Only process if text has changed (new prompt)
            if text and text != last_text:
                console.print(f"[cyan]New phrase detected:[/cyan] {text}")
                
                # Play text using TTS
                tts.speak(text)
                last_text = text
            
            time.sleep(config.check_interval)  # Wait before next check
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping automation...[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
