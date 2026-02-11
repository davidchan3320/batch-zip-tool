#!/usr/bin/env python3
"""
Batch ZIP GUI Application
A cross-platform GUI tool for batch zipping folders with options to update/replace or update/delete.
"""

import os
import sys
import zipfile
import shutil
import threading
import subprocess
import platform
from pathlib import Path
from tkinter import Tk, Label, Button, Frame, Listbox, Scrollbar, StringVar, Radiobutton, Toplevel, Checkbutton, BooleanVar
from tkinter import filedialog, messagebox, ttk
from tkinter.constants import *

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False
    print("提示: 安裝 tkinterdnd2 以啟用拖放功能: pip install tkinterdnd2")


class BatchZipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch ZIP - 批次壓縮工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Dark theme colors
        self.colors = {
            'bg_dark': '#1a1a1a',         # Main background
            'bg_medium': '#2d2d2d',       # Secondary background
            'bg_light': '#3a3a3a',        # Lighter elements
            'fg_primary': '#d4d4d4',      # Primary text (lighter for better readability)
            'fg_secondary': '#a8a8a8',    # Secondary text (lighter)
            'accent_blue': '#3a8fd9',     # Blue accent (darker)
            'accent_red': '#e85555',      # Red accent (darker)
            'accent_green': '#45b854',    # Green accent (darker)
            'accent_purple': '#8b6fce',   # Purple accent (darker)
            'accent_gray': '#5a6672',     # Gray accent (darker)
            'accent_cyan': '#1db8c8',     # Cyan accent (darker)
            'border': '#404040'            # Border color
        }

        # Apply dark theme to root
        self.root.configure(bg=self.colors['bg_dark'])

        # List to store selected folders
        self.selected_folders = []

        # Operation mode: 'replace' or 'delete'
        self.operation_mode = StringVar(value='replace')

        # Check for 7zip availability
        self.sevenzip_path = self._find_7zip()
        self.use_7zip = BooleanVar(value=bool(self.sevenzip_path))

        self._setup_ui()

    def _find_7zip(self):
        """Find 7zip executable on the system"""
        system = platform.system()
        possible_paths = []

        if system == 'Windows':
            possible_paths = [
                r'C:\Program Files\7-Zip\7z.exe',
                r'C:\Program Files (x86)\7-Zip\7z.exe',
            ]
        elif system == 'Darwin':  # macOS
            possible_paths = [
                '/usr/local/bin/7z',
                '/opt/homebrew/bin/7z',
                '/usr/bin/7z',
            ]
        else:  # Linux
            possible_paths = [
                '/usr/bin/7z',
                '/usr/local/bin/7z',
            ]

        # Check each path
        for path in possible_paths:
            if os.path.exists(path):
                return path

        # Try to find in PATH
        try:
            result = subprocess.run(['which', '7z'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass

        return None

    def _setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = Frame(self.root, bg=self.colors['bg_medium'], pady=15)
        title_frame.pack(fill=X)

        title_label = Label(
            title_frame,
            text="🗜️ Batch ZIP Tool",
            font=('Helvetica', 20, 'bold'),
            bg=self.colors['bg_medium'],
            fg=self.colors['fg_primary']
        )
        title_label.pack()

        # Main container
        main_frame = Frame(self.root, bg=self.colors['bg_dark'], padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)

        # Folder selection section
        selection_frame = Frame(main_frame, bg=self.colors['bg_dark'])
        selection_frame.pack(fill=BOTH, expand=True)

        Label(
            selection_frame,
            text="選取的資料夾:",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['bg_dark'],
            fg=self.colors['fg_primary']
        ).pack(anchor=W, pady=(0, 5))

        # Drag and drop hint
        if HAS_DND:
            dnd_hint = Label(
                selection_frame,
                text="💡 提示: 您可以直接拖放資料夾到下方列表",
                font=('Helvetica', 9, 'italic'),
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_secondary']
            )
            dnd_hint.pack(anchor=W, pady=(0, 5))

        # Listbox with scrollbar
        listbox_frame = Frame(selection_frame, bg=self.colors['bg_dark'])
        listbox_frame.pack(fill=BOTH, expand=True)

        scrollbar = Scrollbar(listbox_frame, bg=self.colors['bg_medium'])
        scrollbar.pack(side=RIGHT, fill=Y)

        self.folder_listbox = Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=('Courier', 10),
            selectmode=EXTENDED,
            bg=self.colors['bg_light'],
            fg=self.colors['fg_primary'],
            selectbackground=self.colors['accent_blue'],
            selectforeground='white',
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['accent_blue']
        )
        self.folder_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.folder_listbox.yview)

        # Setup drag and drop
        if HAS_DND:
            self.folder_listbox.drop_target_register(DND_FILES)
            self.folder_listbox.dnd_bind('<<Drop>>', self._on_drop)

        # Buttons frame
        button_frame = Frame(main_frame, bg=self.colors['bg_dark'], pady=10)
        button_frame.pack(fill=X)

        Button(
            button_frame,
            text="➕ 加入資料夾",
            command=self.add_folders,
            bg=self.colors['accent_blue'],
            fg='#000000',
            font=('Helvetica', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=FLAT,
            activebackground='#5aa3e8',
            activeforeground='#000000',
            disabledforeground='#000000'
        ).pack(side=LEFT, padx=(0, 10))

        Button(
            button_frame,
            text="➖ 移除選取項目",
            command=self.remove_selected,
            bg=self.colors['accent_red'],
            fg='#000000',
            font=('Helvetica', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=FLAT,
            activebackground='#f16a6a',
            activeforeground='#000000',
            disabledforeground='#000000'
        ).pack(side=LEFT, padx=(0, 10))

        Button(
            button_frame,
            text="🗑️ 清空列表",
            command=self.clear_list,
            bg=self.colors['accent_gray'],
            fg='#000000',
            font=('Helvetica', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=FLAT,
            activebackground='#6b7885',
            activeforeground='#000000',
            disabledforeground='#000000'
        ).pack(side=LEFT)

        # Options frame
        options_frame = Frame(main_frame, bg=self.colors['bg_dark'], pady=15)
        options_frame.pack(fill=X)

        Label(
            options_frame,
            text="壓縮選項:",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['bg_dark'],
            fg=self.colors['fg_primary']
        ).pack(anchor=W, pady=(0, 8))

        Radiobutton(
            options_frame,
            text="更新並取代 (Update and Replace) - 建立 ZIP 檔案，保留原始資料夾",
            variable=self.operation_mode,
            value='replace',
            font=('Helvetica', 10),
            cursor='hand2',
            bg=self.colors['bg_dark'],
            fg=self.colors['fg_primary'],
            selectcolor=self.colors['bg_light'],
            activebackground=self.colors['bg_dark'],
            activeforeground=self.colors['fg_primary']
        ).pack(anchor=W, pady=2)

        Radiobutton(
            options_frame,
            text="更新並刪除 (Update and Delete) - 建立 ZIP 檔案，刪除原始資料夾",
            variable=self.operation_mode,
            value='delete',
            font=('Helvetica', 10),
            cursor='hand2',
            bg=self.colors['bg_dark'],
            fg=self.colors['fg_primary'],
            selectcolor=self.colors['bg_light'],
            activebackground=self.colors['bg_dark'],
            activeforeground=self.colors['fg_primary']
        ).pack(anchor=W, pady=2)

        # 7zip option
        if self.sevenzip_path:
            ttk.Separator(options_frame, orient='horizontal').pack(fill=X, pady=8)

            sevenzip_frame = Frame(options_frame, bg=self.colors['bg_dark'])
            sevenzip_frame.pack(anchor=W, pady=2)

            Checkbutton(
                sevenzip_frame,
                text="使用 7-Zip 壓縮 (更高壓縮率)",
                variable=self.use_7zip,
                font=('Helvetica', 10, 'bold'),
                cursor='hand2',
                bg=self.colors['bg_dark'],
                fg=self.colors['accent_cyan'],
                selectcolor=self.colors['bg_light'],
                activebackground=self.colors['bg_dark'],
                activeforeground=self.colors['accent_cyan']
            ).pack(side=LEFT)

            Label(
                sevenzip_frame,
                text=f"  ✓ 已檢測到 7-Zip",
                font=('Helvetica', 9),
                bg=self.colors['bg_dark'],
                fg=self.colors['accent_green']
            ).pack(side=LEFT)
        else:
            ttk.Separator(options_frame, orient='horizontal').pack(fill=X, pady=8)

            Label(
                options_frame,
                text="💡 安裝 7-Zip 以獲得更好的壓縮效果 (可選)",
                font=('Helvetica', 9, 'italic'),
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_secondary']
            ).pack(anchor=W, pady=2)

        # Progress section
        progress_frame = Frame(main_frame, bg=self.colors['bg_dark'], pady=10)
        progress_frame.pack(fill=X)

        self.progress_label = Label(
            progress_frame,
            text="準備開始...",
            font=('Helvetica', 10),
            bg=self.colors['bg_dark'],
            fg=self.colors['fg_secondary']
        )
        self.progress_label.pack(anchor=W)

        # Style the progress bar for dark theme
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Dark.Horizontal.TProgressbar',
                       background=self.colors['accent_green'],
                       troughcolor=self.colors['bg_light'],
                       bordercolor=self.colors['border'],
                       lightcolor=self.colors['accent_green'],
                       darkcolor=self.colors['accent_green'])

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=300,
            style='Dark.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=X, pady=(5, 0))

        # Start button
        self.start_button = Button(
            main_frame,
            text="🚀 開始批次壓縮",
            command=self.start_batch_zip,
            bg=self.colors['accent_green'],
            fg='#000000',
            font=('Helvetica', 14, 'bold'),
            padx=30,
            pady=15,
            cursor='hand2',
            relief=FLAT,
            activebackground='#5ac966',
            activeforeground='#000000',
            disabledforeground='#000000'
        )
        self.start_button.pack(pady=15)

    def add_folders(self):
        """Add folders to the list with multi-select support"""
        # Show dialog asking for single or multi-select mode
        dialog = Toplevel(self.root)
        dialog.title("選擇加入方式")
        dialog.geometry("400x180")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg_dark'])

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        Label(
            dialog,
            text="請選擇加入資料夾的方式：",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['bg_dark'],
            fg=self.colors['fg_primary'],
            pady=20
        ).pack()

        button_frame = Frame(dialog, bg=self.colors['bg_dark'])
        button_frame.pack(pady=10)

        def single_mode():
            dialog.destroy()
            self._add_single_folder()

        def multi_mode():
            dialog.destroy()
            self._add_multiple_folders()

        Button(
            button_frame,
            text="📁 單一資料夾\n(選擇一個資料夾)",
            command=single_mode,
            bg=self.colors['accent_blue'],
            fg='#000000',
            font=('Helvetica', 10, 'bold'),
            padx=20,
            pady=15,
            width=18,
            cursor='hand2',
            relief=FLAT,
            activebackground='#5aa3e8',
            activeforeground='#000000',
            disabledforeground='#000000'
        ).pack(side=LEFT, padx=10)

        Button(
            button_frame,
            text="📂 多選模式\n(從父資料夾選擇多個)",
            command=multi_mode,
            bg=self.colors['accent_purple'],
            fg='#000000',
            font=('Helvetica', 10, 'bold'),
            padx=20,
            pady=15,
            width=18,
            cursor='hand2',
            relief=FLAT,
            activebackground='#9d7ddc',
            activeforeground='#000000',
            disabledforeground='#000000'
        ).pack(side=LEFT, padx=10)

        dialog.wait_window()

    def _add_single_folder(self):
        """Add a single folder"""
        folder = filedialog.askdirectory(title="選取資料夾")
        if folder:
            if folder not in self.selected_folders:
                self.selected_folders.append(folder)
                self.folder_listbox.insert(END, folder)
            else:
                messagebox.showinfo("資訊", "此資料夾已在列表中")

            # Ask if user wants to add more
            if messagebox.askyesno("加入更多", "是否要加入更多資料夾？"):
                self.add_folders()

    def _add_multiple_folders(self):
        """Add multiple folders from a parent directory"""
        parent_folder = filedialog.askdirectory(title="選取父資料夾（將顯示其中的子資料夾供您選擇）")
        if not parent_folder:
            return

        parent_path = Path(parent_folder)

        # Get all subdirectories
        subdirs = [d for d in parent_path.iterdir() if d.is_dir()]

        if not subdirs:
            messagebox.showinfo("資訊", "此資料夾內沒有子資料夾")
            return

        # Create selection dialog
        select_dialog = Toplevel(self.root)
        select_dialog.title(f"選擇要加入的資料夾 - {parent_path.name}")
        select_dialog.geometry("600x500")
        select_dialog.transient(self.root)
        select_dialog.grab_set()
        select_dialog.configure(bg=self.colors['bg_dark'])

        # Center the dialog
        select_dialog.update_idletasks()
        x = (select_dialog.winfo_screenwidth() // 2) - (select_dialog.winfo_width() // 2)
        y = (select_dialog.winfo_screenheight() // 2) - (select_dialog.winfo_height() // 2)
        select_dialog.geometry(f"+{x}+{y}")

        Label(
            select_dialog,
            text=f"父資料夾: {parent_folder}",
            font=('Helvetica', 10),
            bg=self.colors['bg_medium'],
            fg=self.colors['fg_primary'],
            pady=10
        ).pack(fill=X)

        Label(
            select_dialog,
            text=f"請選擇要加入的子資料夾 (找到 {len(subdirs)} 個):",
            font=('Helvetica', 11, 'bold'),
            bg=self.colors['bg_dark'],
            fg=self.colors['fg_primary'],
            pady=10
        ).pack()

        # Frame for checkboxes with scrollbar
        canvas_frame = Frame(select_dialog, bg=self.colors['bg_dark'])
        canvas_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        canvas = ttk.Scrollbar(canvas_frame, orient=VERTICAL)

        checkbox_frame = Frame(canvas_frame, bg=self.colors['bg_dark'])

        scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, bg=self.colors['bg_medium'])
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create a frame inside canvas for checkboxes
        checkbox_container = Frame(canvas_frame, bg=self.colors['bg_dark'])
        checkbox_container.pack(side=LEFT, fill=BOTH, expand=True)

        # Dictionary to store checkbox variables
        checkbox_vars = {}

        # Add "Select All" option
        select_all_var = BooleanVar(value=False)

        def toggle_all():
            value = select_all_var.get()
            for var in checkbox_vars.values():
                var.set(value)

        select_all_frame = Frame(checkbox_container, bg=self.colors['bg_light'], pady=5)
        select_all_frame.pack(fill=X, pady=(0, 10))

        Checkbutton(
            select_all_frame,
            text="✓ 全選 / 全不選",
            variable=select_all_var,
            command=toggle_all,
            font=('Helvetica', 10, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['fg_primary'],
            selectcolor=self.colors['bg_medium'],
            activebackground=self.colors['bg_light'],
            activeforeground=self.colors['fg_primary'],
            cursor='hand2'
        ).pack(anchor=W, padx=5)

        # Create scrollable frame for checkboxes
        scrollable_frame = Frame(checkbox_container, bg=self.colors['bg_dark'])
        scrollable_frame.pack(fill=BOTH, expand=True)

        # Add checkboxes for each subdirectory
        for subdir in sorted(subdirs, key=lambda x: x.name.lower()):
            var = BooleanVar(value=False)
            checkbox_vars[str(subdir)] = var

            cb = Checkbutton(
                scrollable_frame,
                text=f"  📁 {subdir.name}",
                variable=var,
                font=('Helvetica', 10),
                cursor='hand2',
                anchor=W,
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_primary'],
                selectcolor=self.colors['bg_light'],
                activebackground=self.colors['bg_dark'],
                activeforeground=self.colors['fg_primary']
            )
            cb.pack(fill=X, pady=2, padx=5)

        # Buttons frame
        button_frame = Frame(select_dialog, bg=self.colors['bg_dark'], pady=15)
        button_frame.pack()

        def confirm_selection():
            selected = [path for path, var in checkbox_vars.items() if var.get()]

            if not selected:
                messagebox.showwarning("警告", "請至少選擇一個資料夾")
                return

            added_count = 0
            duplicate_count = 0

            for folder_path in selected:
                if folder_path not in self.selected_folders:
                    self.selected_folders.append(folder_path)
                    self.folder_listbox.insert(END, folder_path)
                    added_count += 1
                else:
                    duplicate_count += 1

            select_dialog.destroy()

            message = f"已加入 {added_count} 個資料夾"
            if duplicate_count > 0:
                message += f"\n（{duplicate_count} 個已在列表中，已略過）"

            messagebox.showinfo("完成", message)

        def cancel_selection():
            select_dialog.destroy()

        Button(
            button_frame,
            text="✓ 確認加入",
            command=confirm_selection,
            bg=self.colors['accent_green'],
            fg='#000000',
            font=('Helvetica', 11, 'bold'),
            padx=30,
            pady=10,
            cursor='hand2',
            relief=FLAT,
            activebackground='#5ac966',
            activeforeground='#000000',
            disabledforeground='#000000'
        ).pack(side=LEFT, padx=10)

        Button(
            button_frame,
            text="✗ 取消",
            command=cancel_selection,
            bg=self.colors['accent_gray'],
            fg='#000000',
            font=('Helvetica', 11, 'bold'),
            padx=30,
            pady=10,
            cursor='hand2',
            relief=FLAT,
            activebackground='#6b7885',
            activeforeground='#000000',
            disabledforeground='#000000'
        ).pack(side=LEFT, padx=10)

        select_dialog.wait_window()

    def _on_drop(self, event):
        """Handle drag and drop events"""
        # Parse the dropped files/folders
        # On macOS, the data might be a space-separated string or a proper list
        if isinstance(event.data, str):
            # Handle both space-separated and newline-separated formats
            if '\n' in event.data:
                files = event.data.strip().split('\n')
            else:
                # Try to parse as Tcl list first
                try:
                    files = self.root.tk.splitlist(event.data)
                except:
                    # Fallback to space-separated
                    files = [event.data.strip()]
        else:
            files = [event.data]

        added_count = 0
        duplicate_count = 0
        invalid_count = 0

        for file_path in files:
            # Remove curly braces and quotes if present
            file_path = str(file_path).strip('{}').strip().strip('"').strip("'")

            if not file_path:
                continue

            # Check if it's a directory
            if os.path.isdir(file_path):
                if file_path not in self.selected_folders:
                    self.selected_folders.append(file_path)
                    self.folder_listbox.insert(END, file_path)
                    added_count += 1
                else:
                    duplicate_count += 1
            else:
                invalid_count += 1

        # Show feedback
        if added_count > 0:
            message = f"已加入 {added_count} 個資料夾"
            if duplicate_count > 0:
                message += f"\n（{duplicate_count} 個已在列表中，已略過）"
            if invalid_count > 0:
                message += f"\n（{invalid_count} 個非資料夾項目已略過）"

            # Use a simple status update instead of a popup for better UX
            self.progress_label.config(text=message, fg=self.colors['accent_green'])
            self.root.after(3000, lambda: self.progress_label.config(text="準備開始...", fg=self.colors['fg_secondary']))
        elif invalid_count > 0:
            message = f"⚠️ {invalid_count} 個項目不是資料夾"
            self.progress_label.config(text=message, fg=self.colors['accent_red'])
            self.root.after(3000, lambda: self.progress_label.config(text="準備開始...", fg=self.colors['fg_secondary']))

    def remove_selected(self):
        """Remove selected items from the list"""
        selected_indices = self.folder_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "請先選取要移除的項目")
            return

        # Remove in reverse order to avoid index shifting
        for index in reversed(selected_indices):
            self.folder_listbox.delete(index)
            del self.selected_folders[index]

    def clear_list(self):
        """Clear all items from the list"""
        if self.selected_folders and messagebox.askyesno("確認", "確定要清空所有項目？"):
            self.folder_listbox.delete(0, END)
            self.selected_folders.clear()

    def zip_folder(self, folder_path, output_path):
        """
        Zip a folder to output_path using 7zip or built-in zipfile

        Args:
            folder_path: Path to the folder to zip
            output_path: Path where to save the zip file
        """
        if self.use_7zip.get() and self.sevenzip_path:
            return self._zip_with_7zip(folder_path, output_path)
        else:
            return self._zip_with_builtin(folder_path, output_path)

    def _zip_with_7zip(self, folder_path, output_path):
        """Zip using 7zip for better compression"""
        try:
            # Use 7zip command line
            # -tzip: zip format, -mx=9: maximum compression
            cmd = [
                self.sevenzip_path,
                'a',  # add to archive
                '-tzip',  # zip format
                '-mx=9',  # maximum compression
                str(output_path),
                str(folder_path)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            raise Exception(f"7-Zip 錯誤: {e.stderr}")
        except Exception as e:
            raise Exception(f"7-Zip 壓縮失敗: {str(e)}")

    def _zip_with_builtin(self, folder_path, output_path):
        """Zip using Python's built-in zipfile module"""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            folder_path = Path(folder_path)
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    # Calculate the relative path for the archive
                    arcname = file_path.relative_to(folder_path.parent)
                    zipf.write(file_path, arcname)
        return True

    def process_folders(self):
        """Process all folders in the list"""
        if not self.selected_folders:
            messagebox.showwarning("警告", "請先加入要壓縮的資料夾")
            return

        mode = self.operation_mode.get()
        total = len(self.selected_folders)
        success_count = 0
        error_count = 0
        errors = []

        self.progress_bar['maximum'] = total
        self.progress_bar['value'] = 0

        for i, folder_path in enumerate(self.selected_folders):
            try:
                folder_path = Path(folder_path)
                if not folder_path.exists():
                    error_count += 1
                    errors.append(f"{folder_path.name}: 資料夾不存在")
                    continue

                if not folder_path.is_dir():
                    error_count += 1
                    errors.append(f"{folder_path.name}: 不是有效的資料夾")
                    continue

                # Update progress label
                self.progress_label.config(
                    text=f"正在壓縮 ({i+1}/{total}): {folder_path.name}"
                )
                self.root.update()

                # Create zip file with the same name as the folder
                zip_path = folder_path.parent / f"{folder_path.name}.zip"

                # Zip the folder
                self.zip_folder(folder_path, zip_path)

                # If mode is delete, remove the original folder
                if mode == 'delete':
                    shutil.rmtree(folder_path)

                success_count += 1

            except Exception as e:
                error_count += 1
                errors.append(f"{folder_path.name}: {str(e)}")

            finally:
                self.progress_bar['value'] = i + 1
                self.root.update()

        # Show completion message
        self.progress_label.config(text="完成！")

        message = f"批次壓縮完成！\n\n成功: {success_count}\n失敗: {error_count}"
        if errors:
            message += "\n\n錯誤詳情:\n" + "\n".join(errors[:5])
            if len(errors) > 5:
                message += f"\n... 以及其他 {len(errors) - 5} 個錯誤"

        messagebox.showinfo("完成", message)

        # Re-enable the start button
        self.start_button.config(state=NORMAL)

        # Clear the list after successful operation
        if success_count > 0 and messagebox.askyesno("清空列表", "是否要清空已處理的項目？"):
            self.clear_list()

    def start_batch_zip(self):
        """Start the batch zip process"""
        if not self.selected_folders:
            messagebox.showwarning("警告", "請先加入要壓縮的資料夾")
            return

        mode = self.operation_mode.get()
        mode_text = "更新並取代" if mode == 'replace' else "更新並刪除"

        # Confirm before starting
        confirm_message = f"即將使用「{mode_text}」模式壓縮 {len(self.selected_folders)} 個資料夾。"
        if mode == 'delete':
            confirm_message += "\n\n⚠️ 警告：原始資料夾將會被刪除！"
        confirm_message += "\n\n確定要繼續嗎？"

        if not messagebox.askyesno("確認", confirm_message):
            return

        # Disable the start button
        self.start_button.config(state=DISABLED)

        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_folders, daemon=True)
        thread.start()


def main():
    """Main entry point"""
    # Use TkinterDnD if available, otherwise regular Tk
    if HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = Tk()

    app = BatchZipGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
