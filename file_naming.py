"""
=============================================================================
Interactive Batch File Renamer (GUI)
=============================================================================
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox


def run_rename():
    #retrieve user inputs from the GUI
    folder_path = entry_path.get().strip()
    target_ext = entry_ext.get().strip().lower()
    keyword = entry_keyword.get().strip().lower()
    prefix = entry_prefix.get().strip()
    padding_str = entry_padding.get().strip()

    #input validation
    if not folder_path or not prefix:
        messagebox.showwarning("Warning", "Folder path and prefix cannot be empty!")
        return
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", "Directory not found. Please check the path.")
        return

    #validate padding input (must be a positive integer)
    try:
        padding = int(padding_str)
        if padding < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Number of digits must be a positive integer (e.g., 2, 3).")
        return

    try:
        raw_files = os.listdir(folder_path)
        target_files = []

        #1. collect and filter valid files first
        for filename in raw_files:
            #match extensions
            match_ext = (target_ext == "" or filename.lower().endswith(target_ext))
            #match keywords
            match_keyword = (keyword == "" or keyword in filename.lower())

            if match_ext and match_keyword:
                old_filepath = os.path.join(folder_path, filename)
                # Ensure it's a file, not a folder
                if not os.path.isdir(old_filepath):
                    target_files.append(filename)

        #check if any files were found
        if not target_files:
            messagebox.showinfo("Info", "No files matching the criteria found in this folder.")
            return

        #2. sort files chronologically by last modified time (oldest first)
        target_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))

        #3. generate a preview for the Confirmation Dialog
        first_file = target_files[0]
        _, first_ext = os.path.splitext(first_file)
        first_new_name = f"{prefix}{1:0{padding}d}{first_ext}"

        preview_msg = (
            f"Found {len(target_files)} files to rename.\n"
            f"Files will be numbered in chronological order (oldest first).\n\n"
            f"Preview Example:\n"
            f"'{first_file}'  -->  '{first_new_name}'\n\n"
            f"Do you want to proceed?"
        )

        # pop up the yes/no confirmation window
        if not messagebox.askyesno("Confirm Rename", preview_msg):
            return  # stop execution if user clicks 'No'

        #4. execute renaming if user clicked 'Yes'
        count = 1
        for filename in target_files:
            old_filepath = os.path.join(folder_path, filename)
            _, ext = os.path.splitext(filename)

            new_name = f"{prefix}{count:0{padding}d}{ext}"
            new_filepath = os.path.join(folder_path, new_name)

            os.rename(old_filepath, new_filepath)
            count += 1

        #success notification
        messagebox.showinfo("Success", f"Task completed!\nSuccessfully renamed {len(target_files)} files.")

    except Exception as e:
        #handle unexpected system errors
        messagebox.showerror("Error", f"An error occurred during renaming:\n{str(e)}")


def browse_folder():
    """Open a system dialog to select a directory"""
    folder = filedialog.askdirectory()
    if folder:
        # clear existing text and insert the selected path
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder)

# =========================================
# GUI Setup
# =========================================

# initialize main window
root = tk.Tk()
root.title("Lab Data Renamer v1.3")
root.geometry("500x420") # 修复点 3：拉高了窗口，防止按钮被挤压
root.config(padx=20, pady=20)

#1. directory selection area
tk.Label(root, text="1. Target Directory:").pack(anchor="w")
frame_path = tk.Frame(root)
frame_path.pack(fill="x", pady=(0, 10))
entry_path = tk.Entry(frame_path, width=40)
entry_path.pack(side="left", fill="x", expand=True)
btn_browse = tk.Button(frame_path, text="Browse...", command=browse_folder)
btn_browse.pack(side="right", padx=(5, 0))

#2. file extension area
tk.Label(root, text="2. Target Extension (e.g., .tif, .csv, or leave blank for all):").pack(anchor="w")
entry_ext = tk.Entry(root)
entry_ext.insert(0, ".tif")  # Default value
entry_ext.pack(fill="x", pady=(0, 10))

#3. filtering keywords area
tk.Label(root, text="3. Must Contain Keyword (Optional, e.g., 'WT' or 'DAPI'):").pack(anchor="w")
entry_keyword = tk.Entry(root)
entry_keyword.pack(fill="x", pady=(0, 10))

#4. naming prefix area
tk.Label(root, text="4. Naming Prefix (e.g., 20260427_Ventilator_Exp_):").pack(anchor="w")
entry_prefix = tk.Entry(root)
entry_prefix.pack(fill="x", pady=(0, 10))

#5. number padding area
tk.Label(root, text="5. Number of Digits (e.g., enter '3' for 001):").pack(anchor="w")
entry_padding = tk.Entry(root)
entry_padding.insert(0, "3")  # Default padding is 3
entry_padding.pack(fill="x", pady=(0, 20))

#6. execution button
btn_run = tk.Button(root, text="Run Batch Rename", bg="lightblue", font=("Arial", 12, "bold"), command=run_rename)
btn_run.pack(fill="x", pady=10)

# event loop
root.mainloop()
