#!/usr/bin/env python3
"""Main entry point for Convert2ApplePVoice automation."""

import sys
from pathlib import Path
from rich import print
from rich.console import Console

from ocr import OCRExtractor
from ui_automation import UIController
from tts import TTSPlayer
from config import Config

console = Console()

def main():
    """Main automation loop for Personal Voice creation."""
    try:
        config = Config()
        ocr = OCRExtractor()
        ui = UIController()
        tts = TTSPlayer()

        console.print("[bold green]Starting Personal Voice automation...[/bold green]")
        
        while True:
            # Extract text from current prompt
            text = ocr.extract_text()
            if not text:
                console.print("[bold red]Failed to extract text. Retrying...[/bold red]")
                continue

            console.print(f"[cyan]Extracted text:[/cyan] {text}")

            # Click record button
            if not ui.click_record():
                console.print("[bold red]Failed to click Record button[/bold red]")
                break

            # Play text using TTS
            tts.speak(text)

            # Click continue button
            if not ui.click_continue():
                console.print("[bold red]Failed to click Continue button[/bold red]")
                break

    except KeyboardInterrupt:
        console.print("\n[yellow]Automation stopped by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
