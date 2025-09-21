import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import time
from imageFunctions import adjust_rgb, adjust_brightness_sharpness, adjust_saturation, rotate_image, flip_image, adjust_blur

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1000x800")
        
        self.current_image = "example.jpg"
        self.preview_image = "preview.jpg"

        # --- Canvas for image ---
        self.canvas = tk.Label(root)
        self.canvas.pack(pady=20)

        self.draw_image(self.current_image)

        # --- Settings panels ---
        self.create_rgb_panel()
        self.create_brightness_panel()
        self.create_saturation_panel()
        
        
    # scales image to fit inside window
    def resize_for_window(self, img):
        img_width, img_height = img.size

        available_width = self.win_width - 2 * self.margin
        available_height = self.win_height - 2 * self.margin

        scale = min(available_width / img_width, available_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        return img.resize((new_width, new_height))

    # centers image in window
    def center_image(self):
        img_width, img_height = self.resized_img.size
        self.labelImage.place(x=(self.win_width - img_width)//2,
                              y=(self.win_height - img_height)//2)

    def draw_image(self, path):
        img = Image.open(path)
        img = img.resize((600,400))  # scale to fit
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.configure(image=self.tk_image)
        self.canvas.image = self.tk_image

    def update_image(self, func, *args):
        func(self.current_image, *args, save_path=self.preview_image)
        self.draw_image(self.preview_image)

    def create_rgb_panel(self):
        frame = tk.LabelFrame(self.root, text="RGB Adjustments", padx=10, pady=10)
        frame.pack(fill="x", padx=20, pady=5)

        self.r_slider = tk.Scale(frame, from_=0, to=2, resolution=0.1, orient="horizontal", label="Red",
                                 command=lambda _: self.update_image(adjust_rgb, self.r_slider.get(), self.g_slider.get(), self.b_slider.get()))
        self.r_slider.set(1.0)
        self.r_slider.pack(side="left", padx=5)

        self.g_slider = tk.Scale(frame, from_=0, to=2, resolution=0.1, orient="horizontal", label="Green",
                                 command=lambda _: self.update_image(adjust_rgb, self.r_slider.get(), self.g_slider.get(), self.b_slider.get()))
        self.g_slider.set(1.0)
        self.g_slider.pack(side="left", padx=5)

        self.b_slider = tk.Scale(frame, from_=0, to=2, resolution=0.1, orient="horizontal", label="Blue",
                                 command=lambda _: self.update_image(adjust_rgb, self.r_slider.get(), self.g_slider.get(), self.b_slider.get()))
        self.b_slider.set(1.0)
        self.b_slider.pack(side="left", padx=5)

    def create_brightness_panel(self):
        frame = tk.LabelFrame(self.root, text="Brightness & Sharpness", padx=10, pady=10)
        frame.pack(fill="x", padx=20, pady=5)

        self.bright_slider = tk.Scale(frame, from_=0, to=2, resolution=0.1, orient="horizontal", label="Brightness",
                                      command=lambda _: self.update_image(adjust_brightness_sharpness, self.bright_slider.get(), self.sharp_slider.get()))
        self.bright_slider.set(1.0)
        self.bright_slider.pack(side="left", padx=5)

        self.sharp_slider = tk.Scale(frame, from_=0, to=3, resolution=0.1, orient="horizontal", label="Sharpness",
                                     command=lambda _: self.update_image(adjust_brightness_sharpness, self.bright_slider.get(), self.sharp_slider.get()))
        self.sharp_slider.set(1.0)
        self.sharp_slider.pack(side="left", padx=5)

    def create_saturation_panel(self):
        frame = tk.LabelFrame(self.root, text="Saturation", padx=10, pady=10)
        frame.pack(fill="x", padx=20, pady=5)

        self.sat_slider = tk.Scale(frame, from_=0, to=3, resolution=0.1, orient="horizontal", label="Saturation",
                                   command=lambda _: self.update_image(adjust_saturation, self.sat_slider.get()))
        self.sat_slider.set(1.0)
        self.sat_slider.pack(side="left", padx=5)
