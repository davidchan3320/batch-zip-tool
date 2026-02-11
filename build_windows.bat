@echo off
REM Build script for creating Windows executable

echo ========================================
echo   Batch ZIP - Windows Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo [1/4] Installing build dependencies...
pip install pyinstaller tkinterdnd2

echo.
echo [2/4] Cleaning previous build...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec

echo.
echo [3/4] Building executable with PyInstaller...
pyinstaller --name="Batch-ZIP" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --add-data="README.md;." ^
    --hidden-import=tkinterdnd2 ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=tkinter.filedialog ^
    --collect-all=tkinterdnd2 ^
    --noconsole ^
    batch_zip_gui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [4/4] Build complete!
echo.
echo ========================================
echo  Executable created successfully!
echo ========================================
echo.
echo Location: dist\Batch-ZIP.exe
echo.
echo You can now copy and run this .exe file on any Windows computer.
echo No Python installation required!
echo.
pause
