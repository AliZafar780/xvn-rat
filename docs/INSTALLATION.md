# Installation Guide
## XVNNN-RAT v1.0.0
### Author: Ali Zafar (alizafarbati@gmail.com)

## Prerequisites

### Python Requirements
- **Python 3.7+** required
- **pip** package manager

### Operating Systems
- Windows 10/11 or Server 2016+
- Linux (Ubuntu, Debian, Fedora, Arch, CentOS)
- macOS 10.15+

## Installation Methods

### Method 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/AliZafar780/xvnnn-rat.git
cd xvnnn-rat

# Run setup script
./setup.sh

# Verify installation
python3 test_advanced.py
```

### Method 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/AliZafar780/xvnnn-rat.git
cd xvnnn-rat

# Install core dependencies
pip3 install pynput mss Pillow psutil --break-system-packages

# Install optional dependencies (recommended)
pip3 install opencv-python pyaudio --break-system-packages

# Install build tools
pip3 install pyinstaller --break-system-packages

# Verify installation
python3 test_advanced.py
```

### Method 3: Virtual Environment (Most Secure)

```bash
# Clone repository
git clone https://github.com/AliZafar780/xvnnn-rat.git
cd xvnnn-rat

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
# venv\Scripts\activate

# Install dependencies
pip install pynput mss Pillow psutil opencv-python pyaudio pyinstaller

# Verify installation
python3 test_advanced.py

# Deactivate when done
deactivate
```

## Platform-Specific Instructions

### Windows

1. **Install Python 3.7+**
   - Download from python.org
   - Check "Add Python to PATH" during installation

2. **Install dependencies**
   ```bash
   pip install pynput mss Pillow psutil opencv-python pyaudio pyinstaller
   ```

3. **Run tests**
   ```bash
   python test_advanced.py
   ```

### Linux (Ubuntu/Debian)

```bash
# Update package lists
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv

# Install system dependencies for webcam/audio
sudo apt install ffmpeg libavcodec-dev libavformat-dev

# Follow installation methods above
```

### Linux (Fedora)

```bash
# Update package lists
sudo dnf update

# Install Python 3 and pip
sudo dnf install python3 python3-pip

# Install system dependencies
sudo dnf install ffmpeg ffmpeg-devel

# Follow installation methods above
```

### Linux (Arch)

```bash
# Update package lists
sudo pacman -Syu

# Install Python 3 and pip
sudo pacman -S python python-pip

# Install system dependencies
sudo pacman -S ffmpeg

# Follow installation methods above
```

### macOS

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python

# Install system dependencies
brew install ffmpeg

# Follow installation methods above
```

## Verifying Installation

### Run Test Suite
```bash
python3 test_advanced.py
```

**Expected output:**
```
✓ Modules: PASS
✓ Generators: PASS
✓ Persistence: PASS
✓ Utilities: PASS
Total: 4/4 tests passed
```

### Check Dependencies
```bash
# Check Python version
python3 --version

# Check installed packages
pip3 list | grep -E "(pynput|mss|Pillow|psutil|opencv|pyaudio)"
```

## Troubleshooting Installation

### Issue: "Module not found" errors
**Solution:**
```bash
# Install missing dependencies
pip3 install pynput mss Pillow psutil --break-system-packages
```

### Issue: Permission denied on Linux
**Solution:**
```bash
# Use --break-system-packages flag
pip3 install package_name --break-system-packages

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install package_name
```

### Issue: Webcam not working
**Solution:**
```bash
# Install OpenCV
pip3 install opencv-python --break-system-packages
```

### Issue: Audio not working
**Solution:**
```bash
# Install PyAudio
pip3 install pyaudio --break-system-packages

# On Linux, may need additional packages:
sudo apt install portaudio19-dev python3-pyaudio
```

### Issue: PyInstaller not found
**Solution:**
```bash
pip3 install pyinstaller --break-system-packages
```

## Next Steps

After successful installation:

1. **Start server:**
   ```bash
   python3 src/server/headless.py
   ```

2. **Start client (in another terminal):**
   ```bash
   python3 src/client/main.py
   ```

3. **Generate payloads:**
   ```bash
   python3 generate.py
   ```

## Security Considerations

- Use virtual environment for isolation
- Keep dependencies updated
- Review code before deployment
- Use only on authorized systems

## Support

For issues or questions:
- Email: alizafarbati@gmail.com
- Repository: https://github.com/AliZafar780/xvnnn-rat

---

**Author:** Ali Zafar  
**Email:** alizafarbati@gmail.com  
**Version:** 1.0.0