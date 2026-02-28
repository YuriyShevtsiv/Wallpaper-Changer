

---

# 🖼️ Wallpaper Changer

A modern desktop application for automatically downloading and changing Windows wallpapers by category.

Built with:

* 🖥️ `customtkinter` (modern UI)
* 🐍 Python
* 🌐 `requests`
* 🖼️ `Pillow`
* 🧵 `threading`
* 🪟 Windows API (`ctypes`)

---

## ✨ Features

* 🎨 Choose wallpaper category:

  * Nature
  * Space
  * Technology
* 🔄 Manual wallpaper change
* ⏱ Auto-update timer (1 or 5 minutes)
* 🖼 Image preview inside the app
* 📥 Automatic image download
* 📁 Saves wallpapers to:
  `~/Pictures/Wallpapers`
* 🧵 Non-blocking UI (threaded downloads)
* 🌙 Dark mode interface

---

## 🖥️ Platform Support

⚠️ **Wallpaper changing works only on Windows**

The app uses Windows API (`SystemParametersInfoW`) to set the wallpaper.

You can run the UI on other systems, but wallpaper changing will not work.

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/wallpaper-changer.git
cd wallpaper-changer
```

### 2️⃣ Install dependencies

```bash
pip install customtkinter pillow requests
```

---

## ▶️ Running the Application

```bash
python main.py
```

Make sure you're running it on **Windows** for full functionality.

---

## 🧠 How It Works

### 🔹 Image Download

The app downloads random images using:

```
https://loremflickr.com/1920/1080/{category}
```

Categories:

* `nature`
* `space`
* `technology`

### 🔹 Wallpaper Change (Windows Only)

Uses:

```python
ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
```

To apply the downloaded image as the desktop wallpaper.

### 🔹 Auto Update

* Uses `Tkinter.after()` for scheduling
* Cancels previous timer before setting a new one
* Runs wallpaper change in a separate thread

---

## 🗂 Project Structure

```
wallpaper-changer/
│
├── main.py
├── README.md
└── Pictures/
    └── Wallpapers/
```

Wallpapers are automatically saved in:

```
C:\Users\YourName\Pictures\Wallpapers
```

---

## 🎛 UI Overview

* Category selection (ComboBox)
* Timer selection (ComboBox)
* Change wallpaper button
* Progress bar while downloading
* Status indicator
* Live image preview

---

## ❗ Error Handling

The app handles:

* ❌ No internet connection
* ❌ Download errors
* ❌ Unsupported OS
* ❌ Windows API errors

All errors show message boxes with details.

---

## 🚀 Future Improvements (Optional Ideas)

* Add more categories
* Add custom image folder option
* Multi-monitor support
* Image history
* Linux/macOS wallpaper support
* EXE build with PyInstaller

---

## 🛠 Build as EXE (Optional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

The executable will be inside the `dist/` folder.

---

## 📄 License

MIT License (or your preferred license)

---

## 👨‍💻 Author

Your Name
GitHub: [https://github.com/yourusername](https://github.com/yourusername)

🚀
