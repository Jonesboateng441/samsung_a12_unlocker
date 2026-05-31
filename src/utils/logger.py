#!/usr/bin/env python3
"""
Logging utility for Galaxy A12 Unlock Tool
"""

import logging
import sys
from datetime import datetime
import json
import os

class A12Logger:
    def __init__(self, log_file="a12_unlocker.log"):
        self.log_file = log_file
        self.setup_logger()
        
    def setup_logger(self):
        """Setup logging configuration"""
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Configure logging
        self.logger = logging.getLogger("A12Unlocker")
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(
            filename=f"logs/{self.log_file}",
            mode='a',
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_event(self, event_type, details):
        """Log an event with details"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
            "device_model": self._get_device_info()
        }
        
        # Log to file
        self.logger.info(f"{event_type}: {details}")
        
        # Also save to JSON log
        self._save_json_log(event)
        
        return event
    
    def _save_json_log(self, event):
        """Save event to JSON log file"""
        json_file = "logs/events.json"
        
        # Load existing events
        events = []
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    events = json.load(f)
            except:
                events = []
        
        # Add new event
        events.append(event)
        
        # Save back
        with open(json_file, 'w') as f:
            json.dump(events, f, indent=2)
    
    def _get_device_info(self):
        """Get device information for logging"""
        try:
            import subprocess
            
            result = subprocess.run(
                ["adb", "shell", "getprop", "ro.product.model"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() or "Unknown"
        except:
            return "Unknown"
    
    def log_error(self, error_message, exception=None):
        """Log an error"""
        details = {
            "error": error_message,
            "exception": str(exception) if exception else None
        }
        return self.log_event("ERROR", details)
    
    def log_success(self, success_message):
        """Log a success"""
        return self.log_event("SUCCESS", success_message)
    
    def log_warning(self, warning_message):
        """Log a warning"""
        return self.log_event("WARNING", warning_message)
    
    def log_info(self, info_message):
        """Log an info message"""
        return self.log_event("INFO", info_message)
    
    def get_recent_events(self, count=10):
        """Get recent events from JSON log"""
        json_file = "logs/events.json"
        
        if not os.path.exists(json_file):
            return []
        
        try:
            with open(json_file, 'r') as f:
                events = json.load(f)
            
            return events[-count:]  # Return last 'count' events
        except:
            return []
