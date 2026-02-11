@echo off
REM Installation script for Batch ZIP dependencies on Windows

echo.
echo =================================
echo    Batch ZIP - Install Dependencies
echo =================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found Python %PYTHON_VERSION%
echo.

REM Install tkinterdnd2
echo Installing tkinterdnd2 for drag-and-drop...
pip install tkinterdnd2
if errorlevel 1 (
    echo [WARNING] Failed to install tkinterdnd2 (optional)
) else (
    echo [OK] tkinterdnd2 installed successfully
)
echo.

REM Check for 7-Zip
echo Checking for 7-Zip...
if exist "C:\Program Files\7-Zip\7z.exe" (
    echo [OK] 7-Zip is installed
) else if exist "C:\Program Files (x86)\7-Zip\7z.exe" (
    echo [OK] 7-Zip is installed
) else (
    echo [INFO] 7-Zip not found
    echo.
    echo For better compression, install 7-Zip from:
    echo https://www.7-zip.org/
    echo.
    set /p OPEN_BROWSER="Open 7-Zip website in browser? (Y/N): "
    if /i "%OPEN_BROWSER%"=="Y" (
        start https://www.7-zip.org/
    )
)
echo.

echo =================================
echo Installation complete!
echo.
echo To run the application:
echo   python batch_zip_gui.py
echo.
echo Or double-click:
echo   run.bat
echo.
pause
