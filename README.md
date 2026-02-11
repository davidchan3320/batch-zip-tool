# Batch ZIP GUI Tool 🗜️

A cross-platform GUI application for batch zipping folders on Windows and macOS.

## Features ✨

- **Batch Processing**: Zip multiple folders at once
- **Drag and Drop**: Simply drag folders into the application window
- **Multi-Select Support**: Choose between single folder or multi-select mode
  - **Single Folder Mode**: Add folders one at a time
  - **Multi-Select Mode**: Select a parent folder and choose multiple subfolders at once
- **7-Zip Integration**: Automatically uses 7-Zip if installed for better compression
- **Original Names**: Zipped files keep the original folder names
- **Two Operation Modes**:
  - **Update and Replace**: Creates ZIP files while keeping the original folders
  - **Update and Delete**: Creates ZIP files and removes the original folders
- **User-Friendly Interface**: Simple and intuitive GUI
- **Progress Tracking**: Visual progress bar and status updates
- **Cross-Platform**: Works on both Windows and macOS

## Requirements 📋

### Essential
- Python 3.7 or higher
- tkinter (included with Python on most systems)

### Optional (Recommended)
- **tkinterdnd2**: For drag-and-drop functionality
- **7-Zip**: For better compression ratios

### Installing Python & tkinter

#### macOS
Python 3 usually comes pre-installed on macOS. To check:
```bash
python3 --version
```

If you need to install Python:
```bash
brew install python-tk
```

#### Windows
Download Python from [python.org](https://www.python.org/downloads/). Make sure to check "Add Python to PATH" during installation. tkinter is included by default.

## Installation 🚀

1. Clone or download this repository
2. Navigate to the project directory:
```bash
cd batch-zip
```

3. **(Recommended)** Run the installation script to set up everything:

**macOS/Linux:**
```bash
./install_dependencies.sh
```

**Windows:**
```bash
install_dependencies.bat
```

This will:
- Create a virtual environment
- Install tkinterdnd2 for drag-and-drop
- Check for and optionally install 7-Zip

### Manual Installation

If you prefer manual setup:

**Create virtual environment:**
```bash
python3 -m venv .venv
```

**Activate virtual environment:**

*macOS/Linux:*
```bash
source .venv/bin/activate
```

*Windows:*
```bash
.venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install tkinterdnd2
```

**Install 7-Zip (optional):**

**macOS:**
```bash
brew install p7zip
```

**Windows:**
Download and install from [7-zip.org](https://www.7-zip.org/)

**Linux:**
```bash
sudo apt-get install p7zip-full
```

## Usage 💡

### Running the Application

#### Using the launch script (Recommended)

**macOS/Linux:**
```bash
./run.sh
```

**Windows:**
Double-click `run.bat` or:
```bash
run.bat
```

#### Direct Python execution

**If you used the installation script (virtual environment):**
```bash
.venv/bin/python batch_zip_gui.py    # macOS/Linux
.venv\Scripts\python batch_zip_gui.py  # Windows
```

**Without virtual environment:**
```bash
python3 batch_zip_gui.py  # macOS/Linux
python batch_zip_gui.py   # Windows
```

### Using the Application

1. **Add Folders** - You have multiple ways to add folders:
   - **Drag and Drop**: Drag folders directly from your file manager into the list
   - **Click Button**: Click "➕ 加入資料夾" (Add Folders) button
     - **Single Folder Mode**: Select one folder at a time
     - **Multi-Select Mode**: Choose a parent folder, then select multiple subfolders from a checklist

2. **Choose Operation Mode**:
   - **Update and Replace**: Creates ZIP files, keeps original folders
   - **Update and Delete**: Creates ZIP files, deletes original folders ⚠️

3. **Compression Method** (if 7-Zip is installed):
   - Check "使用 7-Zip 壓縮" for better compression (slower but smaller files)
   - Uncheck to use built-in Python compression (faster)

4. **Start Processing**: Click "🚀 開始批次壓縮" (Start Batch ZIP)

5. **Monitor Progress**: Watch the progress bar and status messages

### Example

If you have folders:
```
/Users/john/Documents/Project1/
/Users/john/Documents/Project2/
```

The application will create:
```
/Users/john/Documents/Project1.zip
/Users/john/Documents/Project2.zip
```

## Operation Modes 🔧

### Update and Replace
- Creates a ZIP file for each selected folder
- Keeps the original folder intact
- Safe option - no data loss
- Use for backup purposes

### Update and Delete ⚠️
- Creates a ZIP file for each selected folder
- **Permanently deletes** the original folder
- Use when you want to save disk space
- **Warning**: This action cannot be undone!

## Features in Detail 📝

### Drag and Drop 🎯
Simply drag folders from your file manager (Finder on macOS, File Explorer on Windows) directly into the application's folder list. Multiple folders can be dropped at once!

### 7-Zip Integration 🗜️
If 7-Zip is installed on your system, the application will automatically detect it:
- **Better Compression**: 7-Zip typically achieves 10-30% better compression than standard ZIP
- **Maximum Compression**: Uses 7-Zip's maximum compression setting (-mx=9)
- **Fallback**: If 7-Zip is not available, uses Python's built-in compression
- **Optional**: You can toggle 7-Zip on/off even if installed

### Multi-Select Folder Addition
When you click "Add Folders", you'll see two options:

#### Single Folder Mode 📁
- Select one folder at a time
- After selecting, you'll be asked if you want to add more
- Good for selecting folders from different locations

#### Multi-Select Mode 📂
- Select a parent folder first
- See all subfolders with checkboxes
- Use "Select All" to quickly select/deselect all folders
- Add multiple folders at once
- Perfect for batch operations on project folders, etc.

### Folder Selection
- Select folders using either single or multi-select mode
- View all selected folders in a list
- Remove individual folders or clear the entire list
- Duplicate folders are automatically detected and skipped

### Error Handling
- Validates folder existence before processing
- Reports errors for individual folders
- Shows summary of successful and failed operations
- Continues processing even if some folders fail

### Progress Tracking
- Real-time progress bar
- Current folder being processed
- Success/failure count
- Detailed error messages

## Troubleshooting 🔍

### "tkinter not found" error

**macOS:**
```bash
brew install python-tk
```

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Windows:**
Reinstall Python from python.org and ensure tkinter is selected during installation.

### Drag and Drop Not Working
Install tkinterdnd2:
```bash
pip install tkinterdnd2
```
Then restart the application.

### 7-Zip Not Detected
Make sure 7-Zip is installed:
- **macOS**: `brew install p7zip`
- **Windows**: Install from [7-zip.org](https://www.7-zip.org/)
- **Linux**: `sudo apt-get install p7zip-full`

Restart the application after installing.

### Permission Errors
Make sure you have read/write permissions for the folders you're trying to zip.

### Folder Already Exists
If a ZIP file with the same name already exists, it will be overwritten.

## Creating a Standalone Executable 📦

To create a standalone Windows executable that doesn't require Python installation:

### Quick Build (Windows)

Simply run the automated build script:
```bash
build_windows.bat
```

This will create `dist/Batch-ZIP.exe` - a standalone executable that includes everything needed.

### Quick Build (macOS/Linux)

```bash
./build_windows.sh
```

### Detailed Instructions

For detailed build instructions, customization options, and troubleshooting:
- See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

The executable will be in the `dist` folder (~15-30 MB) and includes:
- Python interpreter
- All required libraries (tkinter, tkinterdnd2)
- The application 程式碼

**Note:** Cross-compilation is not recommended. Build the Windows .exe on a Windows machine for best results.

## License 📄

This project is open source and available under the MIT License.

## Contributing 🤝

Contributions, issues, and feature requests are welcome!

## Support 💬

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ for efficient file management
