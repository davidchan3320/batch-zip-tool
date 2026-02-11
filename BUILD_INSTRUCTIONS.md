# Building Windows Executable 🏗️

This guide explains how to create a standalone Windows executable (.exe) that can run on any Windows computer without requiring Python installation.

## Quick Build (Windows)

If you're on Windows, simply run:

```bash
build_windows.bat
```

The executable will be created in `dist/Batch-ZIP.exe`

## Manual Build Instructions

### Prerequisites

1. **Python 3.7 or higher** installed on Windows
2. **Internet connection** for downloading dependencies

### Step-by-Step Build Process

#### 1. Install Build Dependencies

```bash
pip install -r requirements-build.txt
```

Or install manually:

```bash
pip install pyinstaller tkinterdnd2
```

#### 2. Build the Executable

**Option A: Using the build script (Recommended)**

```bash
build_windows.bat
```

**Option B: Using PyInstaller directly**

```bash
pyinstaller --name="Batch-ZIP" ^
    --onefile ^
    --windowed ^
    --noconsole ^
    --hidden-import=tkinterdnd2 ^
    --collect-all=tkinterdnd2 ^
    batch_zip_gui.py
```

**Option C: Using the spec file**

```bash
pyinstaller Batch-ZIP.spec
```

#### 3. Find Your Executable

After successful build, find your executable at:
```
dist/Batch-ZIP.exe
```

## Build Output

### File Size
- Expected size: 15-30 MB (depending on Python version and included libraries)
- Single file, fully portable

### What's Included
✅ Python interpreter
✅ All required libraries (tkinter, tkinterdnd2, etc.)
✅ Application code
✅ Drag-and-drop support

### What's NOT Included
❌ 7-Zip (users need to install separately for 7-Zip features)

## Distribution

### Sharing the Executable

1. Copy `dist/Batch-ZIP.exe` to any location
2. Share it with others
3. No installation needed - just double-click to run!

### System Requirements for End Users

- **OS**: Windows 7/8/10/11 (64-bit)
- **RAM**: 100 MB minimum
- **Disk**: 50 MB free space
- **Optional**: 7-Zip for enhanced compression

## Customization

### Adding an Icon

1. Create or obtain a `.ico` file (Windows icon format)
2. Save it as `app_icon.ico` in the project directory
3. Update the build command:

```bash
pyinstaller --icon=app_icon.ico ...other options...
```

Or edit `Batch-ZIP.spec` and change:
```python
icon=None
```
to:
```python
icon='app_icon.ico'
```

### Building with 7-Zip Bundled

To include 7-Zip in the executable:

1. Download 7-Zip command-line version
2. Add to spec file:
```python
datas=[('7z.exe', '.'), ('7z.dll', '.')]
```

## Troubleshooting

### Issue: "PyInstaller not found"
**Solution**: Install PyInstaller
```bash
pip install pyinstaller
```

### Issue: "Module not found: tkinterdnd2"
**Solution**: Install tkinterdnd2
```bash
pip install tkinterdnd2
```

### Issue: Executable is very large (>50MB)
**Solution**: Add UPX compression
1. Download UPX: https://upx.github.io/
2. Add UPX to PATH
3. Rebuild - PyInstaller will automatically use UPX

### Issue: Antivirus flags the .exe
**Solution**: This is common with PyInstaller executables
- The file is safe, it's a false positive
- You can submit it to antivirus vendors as a false positive
- Users may need to add an exception in their antivirus

### Issue: Drag-and-drop doesn't work
**Solution**: Make sure tkinterdnd2 is properly collected
```bash
pyinstaller --collect-all=tkinterdnd2 ...
```

### Issue: Application crashes on startup
**Solution**: Build with console enabled to see errors
```bash
pyinstaller --console ...
```
Then check the error messages

## Advanced Build Options

### Creating a Directory-Based Build

For easier debugging, create a directory instead of single file:

```bash
pyinstaller --onedir batch_zip_gui.py
```

### Including Version Information (Windows only)

Create a `version_info.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    ...
  )
)
```

Then build:
```bash
pyinstaller --version-file=version_info.txt ...
```

## Build on macOS/Linux for Windows

Cross-compilation is complex. Recommended approach:

1. Use a Windows virtual machine (VirtualBox, VMware)
2. Use Windows Subsystem for Linux (WSL) on Windows 11
3. Use a Windows build service
4. Build on actual Windows hardware

## Testing the Executable

Before distribution, test on:
- ✅ Fresh Windows installation (no Python)
- ✅ Different Windows versions (7, 10, 11)
- ✅ With/without 7-Zip installed
- ✅ With antivirus software enabled

## Performance Notes

- First launch may be slower (10-15 seconds)
- Subsequent launches are faster (2-3 seconds)
- Drag-and-drop works immediately
- All features function identically to Python version

## Distribution Checklist

Before sharing your executable:

- [ ] Test on clean Windows system
- [ ] Verify drag-and-drop works
- [ ] Test with/without 7-Zip
- [ ] Check file operations (zip, delete)
- [ ] Verify error handling
- [ ] Include README or user guide
- [ ] Provide system requirements
- [ ] Note optional 7-Zip requirement

---

## Need Help?

If you encounter issues:
1. Check the error messages
2. Review PyInstaller documentation
3. Verify all dependencies are installed
4. Try building with `--debug` flag

Happy building! 🚀
