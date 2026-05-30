#!/usr/bin/env python3
"""
Galaxy A12 Device Detector
"""

import subprocess
import re
import json

class A12Detector:
    def __init__(self):
        self.a12_identifiers = {
            "model": ["SM-A125F", "SM-A125M", "SM-A125U"],
            "board": ["a12q"],
            "chipset": ["mt6765"],
        }
    
    def detect_a12(self):
        """Detect if connected device is Galaxy A12"""
        try:
            # Get device properties
            props = self.get_device_properties()
            
            # Check model
            model = props.get("ro.product.model", "")
            board = props.get("ro.product.board", "").lower()
            
            # Check if it's A12
            is_a12 = any(id in model for id in self.a12_identifiers["model"])
            is_a12_board = any(id in board for id in self.a12_identifiers["board"])
            
            return is_a12 or is_a12_board
            
        except:
            return False
    
    def get_device_properties(self):
        """Get all device properties"""
        properties = {}
        
        try:
            result = subprocess.run(
                ["adb", "shell", "getprop"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse getprop output
            for line in result.stdout.split('\n'):
                match = re.match(r'\[([^\]]+)\]: \[([^\]]*)\]', line)
                if match:
                    key, value = match.groups()
                    properties[key] = value
            
        except:
            pass
        
        return properties
    
    def check_usb_connection(self):
        """Check USB connection status"""
        try:
            result = subprocess.run(
                ["lsusb"],
                capture_output=True,
                text=True
            )
            
            # Samsung USB vendor ID: 04e8
            return "04e8:" in result.stdout
            
        except:
            return False
    
    def get_device_info(self):
        """Get comprehensive device information"""
        info = {
            "model": "Unknown",
            "android_version": "Unknown",
            "security_patch": "Unknown",
            "bootloader": "Unknown",
            "state": "Unknown",
            "adb_available": False,
            "frp_active": False,
            "bootloader_unlocked": False,
        }
        
        try:
            props = self.get_device_properties()
            
            info.update({
                "model": props.get("ro.product.model", "Unknown"),
                "android_version": props.get("ro.build.version.release", "Unknown"),
                "security_patch": props.get("ro.build.version.security_patch", "Unknown"),
                "bootloader": props.get("ro.boot.bootloader", "Unknown"),
                "state": self._get_device_state(),
                "adb_available": self._check_adb_availability(),
                "frp_active": self._check_frp_status(props),
                "bootloader_unlocked": props.get("ro.boot.flash.locked", "1") == "0",
            })
            
        except:
            pass
        
        return info
    
    def _get_device_state(self):
        """Get current device state"""
        try:
            result = subprocess.run(
                ["adb", "get-state"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            state = result.stdout.strip()
            
            if state == "device":
                return "Normal (ADB authorized)"
            elif state == "unauthorized":
                return "Connected but not authorized"
            elif state == "offline":
                return "Device offline"
            else:
                return "Not connected"
                
        except:
            return "Unknown"
    
    def _check_adb_availability(self):
        """Check if ADB is available"""
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            return "device" in result.stdout
            
        except:
            return False
    
    def _check_frp_status(self, props):
        """Check FRP status"""
        # FRP is usually active after factory reset without Google account removal
        frp_props = [
            props.get("ro.frp.pst", ""),
            props.get("persist.sys.frp.pst", ""),
        ]
        
        return any(prop == "1" for prop in frp_props)
