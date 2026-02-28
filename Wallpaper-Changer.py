import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import ctypes
from pathlib import Path
import threading
import sys


class WallpaperChanger:
    def __init__(self):
        # Налаштування вікна
        self.window = ctk.CTk()
        self.window.title("Wallpaper Changer")
        self.window.geometry("550x650")
        ctk.set_appearance_mode("dark")

        # Змінні
        self.timer_id = None
        self.wallpaper_dir = Path.home() / "Pictures" / "Wallpapers"
        self.wallpaper_dir.mkdir(exist_ok=True)

        # Категорії та інтервали
        self.categories = {
            "Природа": "nature",
            "Космос": "space",
            "Технології": "technology"
        }

        self.intervals = {
            "Вимкнено": 0,
            "1 хв": 60000,
            "5 хв": 300000
        }

        self.create_ui()

    def create_ui(self):
        # Заголовок
        ctk.CTkLabel(
            self.window,
            text="🖼️ Wallpaper Changer",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # Фрейм налаштувань
        frame = ctk.CTkFrame(self.window)
        frame.pack(pady=10, padx=20, fill="x")

        # Категорія
        ctk.CTkLabel(
            frame,
            text="Категорія:",
            font=("Arial", 12, "bold")
        ).pack(pady=(10, 5))

        self.category_combo = ctk.CTkComboBox(
            frame,
            values=list(self.categories.keys()),
            width=250,
            state="readonly"
        )
        self.category_combo.set("Природа")
        self.category_combo.pack(pady=(0, 10))

        # Таймер
        ctk.CTkLabel(
            frame,
            text="Автооновлення:",
            font=("Arial", 12, "bold")
        ).pack(pady=(5, 5))

        self.timer_combo = ctk.CTkComboBox(
            frame,
            values=list(self.intervals.keys()),
            width=250,
            state="readonly",
            command=self.on_timer_change
        )
        self.timer_combo.set("Вимкнено")
        self.timer_combo.pack(pady=(0, 10))

        # Кнопка
        self.btn = ctk.CTkButton(
            self.window,
            text="Змінити шпалери",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.change_wallpaper
        )
        self.btn.pack(pady=15, padx=20, fill="x")

        # ProgressBar
        self.progress = ctk.CTkProgressBar(
            self.window,
            width=500,
            mode="indeterminate"
        )

        # Статус
        self.status = ctk.CTkLabel(
            self.window,
            text="Готовий",
            text_color="gray"
        )
        self.status.pack(pady=5)

        # Preview
        self.preview_frame = ctk.CTkFrame(
            self.window,
            width=510,
            height=285
        )
        self.preview_frame.pack(pady=15, padx=20)
        self.preview_frame.pack_propagate(False)

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="Попередній перегляд з'явиться тут",
            text_color="gray"
        )
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

    # ---------------------------
    # Завантаження зображення
    # ---------------------------
    def download_image(self, category):
        try:
            self.window.after(0, lambda: self.status.configure(
                text="Завантаження...", text_color="yellow"))
            self.window.after(0, self.progress.pack, {"pady": 5})
            self.window.after(0, self.progress.start)

            url = f"https://loremflickr.com/1920/1080/{category}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            image_path = self.wallpaper_dir / f"wallpaper_{category}.jpg"

            with open(image_path, "wb") as f:
                f.write(response.content)

            self.window.after(0, self.progress.stop)
            self.window.after(0, self.progress.pack_forget)
            self.window.after(0, lambda: self.status.configure(
                text="Завантажено!", text_color="green"))

            return str(image_path)

        except requests.exceptions.ConnectionError:
            self.window.after(0, self.progress.stop)
            self.window.after(0, self.progress.pack_forget)
            self.window.after(0, lambda: self.status.configure(
                text="Немає інтернету", text_color="red"))
            self.window.after(0, lambda: messagebox.showerror(
                "Помилка", "Перевірте інтернет-з'єднання"))
            return None

        except Exception as e:
            self.window.after(0, self.progress.stop)
            self.window.after(0, self.progress.pack_forget)
            self.window.after(0, lambda: self.status.configure(
                text="Помилка", text_color="red"))
            self.window.after(0, lambda: messagebox.showerror(
                "Помилка", str(e)))
            return None

    # ---------------------------
    # Встановлення шпалер
    # ---------------------------
    def set_wallpaper(self, image_path):
        if sys.platform != "win32":
            self.window.after(0, lambda: messagebox.showerror(
                "Помилка", "Зміна шпалер працює тільки на Windows"))
            return False

        try:
            ctypes.windll.user32.SystemParametersInfoW(
                20, 0, image_path, 3
            )
            self.window.after(0, lambda: self.status.configure(
                text="Шпалери змінено!", text_color="green"))
            return True

        except Exception as e:
            self.window.after(0, lambda: self.status.configure(
                text="Помилка зміни", text_color="red"))
            self.window.after(0, lambda: messagebox.showerror(
                "Помилка", f"Не вдалося змінити шпалери: {e}"))
            return False

    # ---------------------------
    # Preview
    # ---------------------------
    def show_preview(self, image_path):
        try:
            image = Image.open(image_path)
            image.thumbnail((510, 285), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            def update_ui():
                if hasattr(self, 'preview_img'):
                    self.preview_img.configure(image=photo)
                    self.preview_img.image = photo
                else:
                    self.preview_label.destroy()
                    self.preview_img = ctk.CTkLabel(
                        self.preview_frame,
                        image=photo,
                        text=""
                    )
                    self.preview_img.image = photo
                    self.preview_img.place(
                        relx=0.5, rely=0.5, anchor="center")

            self.window.after(0, update_ui)

        except Exception as e:
            print("Preview error:", e)

    # ---------------------------
    # Основна зміна шпалер
    # ---------------------------
    def change_wallpaper(self):
        def task():
            category = self.categories[self.category_combo.get()]
            image_path = self.download_image(category)

            if image_path:
                if self.set_wallpaper(image_path):
                    self.show_preview(image_path)

            self.window.after(0, lambda: self.btn.configure(state="normal"))

        self.btn.configure(state="disabled")
        threading.Thread(target=task, daemon=True).start()

    # ---------------------------
    # Таймер
    # ---------------------------
    def on_timer_change(self, choice):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

        interval = self.intervals[choice]

        if interval > 0:
            self.status.configure(
                text=f"Автооновлення: {choice}",
                text_color="blue"
            )
            self.start_timer(interval)
        else:
            self.status.configure(text="Готовий", text_color="gray")

    def start_timer(self, interval):
        def callback():
            self.change_wallpaper()
            self.timer_id = self.window.after(interval, callback)

        self.timer_id = self.window.after(interval, callback)

    # ---------------------------
    # Запуск
    # ---------------------------
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = WallpaperChanger()
    app.run()