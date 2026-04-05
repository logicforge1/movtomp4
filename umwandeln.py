import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import os
import sys
import threading

selected_files = []

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
        messagebox.showerror("Fehler", "ffmpeg.exe nicht gefunden")
        return

    progress["maximum"] = len(selected_files)
    progress["value"] = 0

    for i, input_file in enumerate(selected_files):
        filename = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_folder, filename + ".mp4")

        command = [
            ffmpeg_path,
            "-i", input_file,
            "-c", "copy",
            output_file
        ]

        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            messagebox.showerror("Fehler", f"Fehler bei:\n{input_file}")
            return

        progress["value"] = i + 1
        root.update_idletasks()

    messagebox.showinfo("Fertig", "Alle Dateien wurden konvertiert 🎉")

# GUI
root = TkinterDnD.Tk()
root.title("MOV → MP4 Converter PRO")
root.geometry("600x400")

# Drag & Drop Bereich
drop_label = tk.Label(root, text="Dateien hier reinziehen", relief="ridge", height=3)
drop_label.pack(fill="x", padx=10, pady=10)
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", drop_files)

# Liste
listbox = tk.Listbox(root)
listbox.pack(fill="both", expand=True, padx=10)

# Buttons Frame
frame = tk.Frame(root)
frame.pack(pady=10)

btn_select = tk.Button(frame, text="Dateien wählen", command=select_files)
btn_select.grid(row=0, column=0, padx=5)

btn_output = tk.Button(frame, text="Zielordner wählen", command=select_output_folder)
btn_output.grid(row=0, column=1, padx=5)

entry_output = tk.Entry(root, width=60)
entry_output.pack(pady=5)

# Progressbar
progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=10)

# Convert Button
btn_convert = tk.Button(root, text="Konvertieren", command=convert)
btn_convert.pack(pady=10)

root.mainloop()