# Quick Start Guide - Batch ZIP 🗜️

## New Features! 🎉

### 1. Drag and Drop 🎯
The easiest way to add folders!

**How to use:**
1. Open your file manager (Finder on macOS, File Explorer on Windows)
2. Select one or more folders
3. Drag them into the Batch ZIP application window
4. Drop on the folder list area
5. Done! ✓

**Tips:**
- You can drop multiple folders at once
- Only folders will be added (files are ignored)
- Duplicate folders are automatically skipped

---

### 2. 7-Zip Integration 🗜️
Better compression for smaller file sizes!

**Benefits:**
- 10-30% better compression than standard ZIP
- Uses maximum compression (-mx=9)
- Automatically detected if installed

**Installation:**

**macOS:**
```bash
brew install p7zip
```

**Windows:**
1. Download from [7-zip.org](https://www.7-zip.org/)
2. Install using the installer
3. Restart Batch ZIP

**Linux:**
```bash
sudo apt-get install p7zip-full
```

**Using 7-Zip:**
- If detected, you'll see "✓ 已檢測到 7-Zip"
- Check the box "使用 7-Zip 壓縮" to enable
- Uncheck to use standard Python compression (faster but larger files)

---

## All Three Ways to Add Folders

### Method 1: Drag and Drop (Fastest) 🎯
Just drag folders from your file manager into the list!

### Method 2: Single Folder Mode 📁
1. Click "➕ 加入資料夾"
2. Choose "單一資料夾"
3. Select a folder
4. Repeat as needed

### Method 3: Multi-Select Mode 📂
1. Click "➕ 加入資料夾"
2. Choose "多選模式"
3. Select a parent folder
4. Check multiple subfolders
5. Click "確認加入"

---

## Performance Tips ⚡

### For Speed:
- Use standard compression (uncheck 7-Zip)
- Process fewer folders at once
- Use "Update and Replace" mode

### For File Size:
- Enable 7-Zip compression
- This will be slower but creates smaller files
- Good for archival or sharing

### For Convenience:
- Use drag-and-drop for quick operations
- Use multi-select for organized folder structures
- Combine methods as needed!

---

## Workflow Examples

### Example 1: Quick Backup
1. Drag project folders into the list
2. Select "Update and Replace"
3. Keep 7-Zip unchecked for speed
4. Click Start

### Example 2: Archival
1. Use multi-select to choose old projects
2. Select "Update and Delete" ⚠️
3. Enable 7-Zip for maximum compression
4. Click Start
5. Confirm deletion warning

### Example 3: Sharing
1. Drag folders you want to share
2. Select "Update and Replace"
3. Enable 7-Zip for smaller uploads
4. Click Start
5. Share the .zip files

---

## Troubleshooting

### Drag and Drop Not Working?
- Make sure tkinterdnd2 is installed: `pip3 install tkinterdnd2`
- Restart the application after installing

### 7-Zip Not Detected?
- Install 7-Zip using the commands above
- Make sure it's in your PATH
- Restart the application

### Application Won't Start?
- Check Python version: `python3 --version` (need 3.7+)
- Install tkinter if needed (see main README)

---

## Keyboard Shortcuts

- **Delete**: Remove selected items from list
- **Cmd/Ctrl + A**: Select all items in list (then remove if needed)

---

## Safety Features

- **Duplicate Detection**: Same folder won't be added twice
- **Validation**: Checks if folders exist before processing
- **Delete Warning**: Confirms before deleting original folders
- **Error Handling**: Continues processing even if some folders fail
- **Progress Tracking**: Shows which folder is being processed

---

Enjoy your enhanced Batch ZIP experience! 🎉
