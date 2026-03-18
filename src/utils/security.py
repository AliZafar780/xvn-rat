"""
Security utilities for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import base64
import logging

logger = logging.getLogger(__name__)

def encode_data(data):
    """Encode data to base64"""
    try:
        if isinstance(data, str):
            data = data.encode()
        return base64.b64encode(data).decode()
    except Exception as e:
        logger.error(f"Failed to encode data: {e}")
        return None

def decode_data(data):
    """Decode base64 data"""
    try:
        return base64.b64decode(data)
    except Exception as e:
        logger.error(f"Failed to decode data: {e}")
        return None