"""UI automation module for controlling Personal Voice interface."""

import subprocess
import time
from pathlib import Path

class UIController:
    """Controls UI interaction with Personal Voice interface using AppleScript."""

    def __init__(self):
        """Initialize the UI controller."""
        self.scripts_dir = Path(__file__).parent / "scripts"
        self.scripts_dir.mkdir(exist_ok=True)
        self._create_scripts()

    def _create_scripts(self):
        """Create necessary AppleScript files."""
        # Script to click Record button
        record_script = self.scripts_dir / "click_record.scpt"
        if not record_script.exists():
            record_script.write_text('''
tell application "System Events"
    tell process "System Settings"
        click button "Record" of window 1
    end tell
end tell
''')

        # Script to click Continue button
        continue_script = self.scripts_dir / "click_continue.scpt"
        if not continue_script.exists():
            continue_script.write_text('''
tell application "System Events"
    tell process "System Settings"
        click button "Continue" of window 1
    end tell
end tell
''')

    def _run_applescript(self, script_path: Path) -> bool:
        """Run an AppleScript file.
        
        Args:
            script_path: Path to the AppleScript file.
            
        Returns:
            bool: True if script executed successfully, False otherwise.
        """
        try:
            subprocess.run(
                ["osascript", str(script_path)],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"AppleScript error: {e.stderr}")
            return False

    def click_record(self) -> bool:
        """Click the Record button.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        success = self._run_applescript(self.scripts_dir / "click_record.scpt")
        if success:
            time.sleep(1)  # Wait for button press to register
        return success

    def click_continue(self) -> bool:
        """Click the Continue button.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        success = self._run_applescript(self.scripts_dir / "click_continue.scpt")
        if success:
            time.sleep(1)  # Wait for button press to register
        return success
