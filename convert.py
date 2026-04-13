import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import os
import sys
import threading

selected_files = []
dark_mode = True


# 🌙 Theme
def apply_theme():
    global dark_mode

    if dark_mode:
        bg = "#1e1e1e"
        fg = "#ffffff"
        accent = "#2d2d2d"
    else:
        bg = "#f0f0f0"
        fg = "#000000"
        accent = "#ffffff"

    root.configure(bg=bg)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TProgressbar", troughcolor=accent, background="#4caf50")

    for w in (drop_label, listbox, frame, btn_select, btn_output, btn_convert, toggle_btn, entry_output):
        try:
            if isinstance(w, (tk.Entry, tk.Listbox)):
                w.config(bg=accent, fg=fg, insertbackground=fg)
            elif isinstance(w, tk.Frame):
                w.config(bg=bg)
            else:
                w.config(bg=accent, fg=fg)
        except:
            pass


def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()


def select_files():
    files = filedialog.askopenfilenames(
        title="MOV Dateien auswählen",
        filetypes=[("MOV files", "*.mov")]
    )
    if files:
        selected_files.clear()
        selected_files.extend(files)
        update_file_list()


def drop_files(event):
    files = root.tk.splitlist(event.data)
    selected_files.clear()
    selected_files.extend(files)
    update_file_list()


def update_file_list():
    listbox.delete(0, tk.END)
    for f in selected_files:
        listbox.insert(tk.END, f)


def select_output_folder():
    folder = filedialog.askdirectory(title="Zielordner wählen")
    if folder:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, folder)


def convert():
    if not selected_files:
        messagebox.showerror("Fehler", "Keine Dateien ausgewählt")
        return

    output_folder = entry_output.get()
    if not output_folder:
        messagebox.showerror("Fehler", "Bitte Zielordner wählen")
        return

    thread = threading.Thread(target=run_conversion, args=(output_folder,))
    thread.start()


def run_conversion(output_folder):
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    ffmpeg_path = os.path.join(base_dir, "ffmpeg.exe")

    if not os.path.exists(ffmpeg_path):
        root.after(0, lambda: messagebox.showerror("Fehler", "ffmpeg.exe nicht gefunden"))
        return

    progress["maximum"] = len(selected_files)
    progress["value"] = 0

    for i, input_file in enumerate(selected_files):
        filename = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_folder, filename + ".mp4")

        command = [
            ffmpeg_path,
            "-y",
            "-i", input_file,
            "-c", "copy",
            output_file
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            root.after(0, lambda f=input_file: messagebox.showerror("Fehler", f"Fehler bei:\n{f}"))
            return

        progress["value"] = i + 1
        root.update_idletasks()

    root.after(0, lambda: messagebox.showinfo("Fertig", "Alle Dateien wurden konvertiert 🎉"))


# ================= GUI =================

root = TkinterDnD.Tk()
root.title("MOV → MP4 Converter PRO")
root.geometry("600x450")

# Drag & Drop
drop_label = tk.Label(root, text="Dateien hier reinziehen", relief="ridge", height=3)
drop_label.pack(fill="x", padx=10, pady=10)
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", drop_files)

# Liste
listbox = tk.Listbox(root)
listbox.pack(fill="both", expand=True, padx=10)

# Buttons
frame = tk.Frame(root)
frame.pack(pady=10)

btn_select = tk.Button(frame, text="Dateien wählen", command=select_files)
btn_select.grid(row=0, column=0, padx=5)

btn_output = tk.Button(frame, text="Zielordner wählen", command=select_output_folder)
btn_output.grid(row=0, column=1, padx=5)

toggle_btn = tk.Button(frame, text="Dark Mode", command=toggle_theme)
toggle_btn.grid(row=0, column=2, padx=5)

# Output
entry_output = tk.Entry(root, width=60)
entry_output.pack(pady=5)

# Progressbar
progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=10)

# Convert
btn_convert = tk.Button(root, text="Konvertieren", command=convert)
btn_convert.pack(pady=10)

# Theme anwenden
apply_theme()

root.mainloop()
