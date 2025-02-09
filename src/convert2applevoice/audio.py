"""Audio device management for Convert2ApplePVoice."""

import subprocess
from typing import Optional, List, Dict, Tuple

class AudioManager:
    """Manages audio device selection and routing."""
    
    @staticmethod
    def get_audio_devices() -> List[Dict[str, str]]:
        """Get list of available audio devices.
        
        Returns:
            List[Dict[str, str]]: List of devices with 'name' and 'type' keys
        """
        devices = []
        try:
            # Use system_profiler to get audio devices
            cmd = ["system_profiler", "SPAudioDataType", "-json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                # Parse audio devices from system profiler output
                for device_type in ["SPAudioDataType"]:
                    if device_type in data:
                        for item in data[device_type]:
                            if "_items" in item:
                                for dev in item["_items"]:
                                    if "coreaudio_device" in dev:
                                        devices.append({
                                            "name": dev["_name"],
                                            "type": "input" if "input" in dev["coreaudio_device"].lower() 
                                                   else "output"
                                        })
        except Exception as e:
            print(f"Error getting audio devices: {str(e)}")
        
        return devices
    
    @staticmethod
    def set_default_input_device(device_name: str) -> bool:
        """Set the default system input device.
        
        Args:
            device_name: Name of the device to set as default input
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Use switchaudio-osx to set default input
            cmd = ["switchaudiosource", "-s", device_name, "-t", "input"]
            result = subprocess.run(cmd)
            return result.returncode == 0
        except Exception as e:
            print(f"Error setting default input device: {str(e)}")
            return False
    
    @staticmethod
    def set_default_output_device(device_name: str) -> bool:
        """Set the default system output device.
        
        Args:
            device_name: Name of the device to set as default output
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Use switchaudio-osx to set default output
            cmd = ["switchaudiosource", "-s", device_name, "-t", "output"]
            result = subprocess.run(cmd)
            return result.returncode == 0
        except Exception as e:
            print(f"Error setting default output device: {str(e)}")
            return False
    
    @staticmethod
    def create_multi_output_device(name: str, devices: List[str]) -> Optional[str]:
        """Create a multi-output device.
        
        Args:
            name: Name for the new multi-output device
            devices: List of device names to include
            
        Returns:
            str: Device ID if successful, None otherwise
        """
        try:
            # First list existing devices to get their IDs
            cmd = ["system_profiler", "SPAudioDataType", "-json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                # Get device IDs
                device_ids = []
                for device_type in ["SPAudioDataType"]:
                    if device_type in data:
                        for item in data[device_type]:
                            if "_items" in item:
                                for dev in item["_items"]:
                                    if dev["_name"] in devices:
                                        if "coreaudio_device_id" in dev:
                                            device_ids.append(dev["coreaudio_device_id"])
                
                if device_ids:
                    # Create multi-output device
                    devices_str = ",".join(device_ids)
                    cmd = [
                        "audiodevice", "aggregate", "create", 
                        name, *device_ids
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        return result.stdout.strip()
        except Exception as e:
            print(f"Error creating multi-output device: {str(e)}")
        
        return None
    
    @staticmethod
    def setup_audio_routing(config: 'Config') -> Tuple[bool, str]:
        """Set up audio routing based on configuration.
        
        Args:
            config: Application configuration
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Install required tools if not present
            subprocess.run(["brew", "install", "switchaudio-osx"], capture_output=True)
            
            # Set output to BlackHole
            if config.audio.output_device:
                if not AudioManager.set_default_output_device(config.audio.output_device):
                    return False, f"Failed to set output device to {config.audio.output_device}"
            
            # Set up monitoring if enabled
            if config.audio.enable_monitoring and config.audio.monitoring_device:
                # Create multi-output device if needed
                devices = [config.audio.output_device, config.audio.monitoring_device]
                multi_device = AudioManager.create_multi_output_device("Convert2Voice Monitor", devices)
                if multi_device:
                    if not AudioManager.set_default_output_device(multi_device):
                        return False, "Failed to set multi-output device"
                else:
                    return False, "Failed to create multi-output device"
            
            return True, "Audio routing configured successfully"
            
        except Exception as e:
            return False, f"Error setting up audio routing: {str(e)}"
