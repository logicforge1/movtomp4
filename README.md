# 🎬 MOV → MP4 Converter PRO

A simple and powerful GUI tool to convert `.mov` files to `.mp4` using FFmpeg — fast, lossless, and easy to use.

---

## 🚀 Features

* 🎥 Convert MOV to MP4
* ⚡ Lossless conversion (`-c copy`)
* 📂 Select custom output folder
* 🖱️ Drag & Drop support
* 📚 Batch processing (multiple files at once)
* 📊 Progress bar
* 💻 Simple and clean GUI (Tkinter)

---

## 🖥️ Screenshot

*(Add a screenshot here if you like)*

---

## 📦 Requirements

* Python 3.x
* FFmpeg (included as `ffmpeg.exe` in the same folder)
* https://mega.nz/folder/S2phUCQa#2farCnUBUpRea-FBpQdTIA

### Install dependencies

```bash
pip install tkinterdnd2
```

---

## ▶️ Usage

1. Start the program:

```bash
python main.py
```

2. Add your `.mov` files:

   * Click **"Dateien wählen"**
   * or drag & drop files into the window

3. Select an output folder

4. Click **"Konvertieren"**

---

## ⚙️ How it works

The converter uses FFmpeg with:

```bash
-c copy
```

This means:

* ✅ No quality loss
* ⚡ Very fast
* ❗ Works only if codecs are compatible with MP4

---

## 🔧 Optional: Re-encoding

If you run into compatibility issues, replace:

```bash
-c copy
```

with:

```bash
-c:v libx264 -c:a aac
```

---

## 📁 Project Structure

```
.
├── main.py
├── ffmpeg.exe
└── README.md
```

---

## 🧠 Future Improvements

* ⏱️ Estimated time remaining (ETA)
* 🌙 Dark mode
* 📜 FFmpeg log output
* 📦 Export as .exe
* 🎛️ Codec selection in GUI

---

## ⚠️ Disclaimer

This tool is for educational and personal use.

---

## ❤️ Credits

* GUI built with Tkinter
* Drag & Drop via tkinterdnd2
* Powered by FFmpeg

---

## 📜 License

MIT License
