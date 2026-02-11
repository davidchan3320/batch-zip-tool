#!/bin/bash
# Build script for creating Windows executable (cross-compile)
# Note: This requires Wine on macOS/Linux for testing

echo "========================================"
echo "  Batch ZIP - Windows Build Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python not found. Please install Python 3.7 or higher."
    exit 1
fi

echo "[1/4] Installing build dependencies..."
pip3 install pyinstaller tkinterdnd2

echo ""
echo "[2/4] Cleaning previous build..."
rm -rf build dist *.spec

echo ""
echo "[3/4] Building executable with PyInstaller..."
pyinstaller --name="Batch-ZIP" \
    --onefile \
    --windowed \
    --icon=NONE \
    --add-data="README.md:." \
    --hidden-import=tkinterdnd2 \
    --hidden-import=tkinter \
    --hidden-import=tkinter.ttk \
    --hidden-import=tkinter.messagebox \
    --hidden-import=tkinter.filedialog \
    --collect-all=tkinterdnd2 \
    --noconsole \
    batch_zip_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Build failed!"
    exit 1
fi

echo ""
echo "[4/4] Build complete!"
echo ""
echo "========================================"
echo "  Executable created successfully!"
echo "========================================"
echo ""
echo "Location: dist/Batch-ZIP"
echo ""
echo "Note: On macOS/Linux, this creates a Unix executable."
echo "To create a Windows .exe, run this script on Windows"
echo "or use build_windows.bat on a Windows machine."
echo ""
