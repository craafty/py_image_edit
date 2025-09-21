import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from image_functions import (
    adjust_rgb,
    adjust_saturation,
    adjust_brightness,
    adjust_sharpness,
    adjust_blur,
    stretch_image
)
import customtkinter as ctk

# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("700x700")
        self.root.configure(bg="#2c2c2c")

        # --- Image variables ---
        self.current_image_path = "example.jpg"
        self.original_img = Image.open(self.current_image_path).convert("RGB")
        self.current_img = self.original_img.copy()
        self.displayed_img = None
        self.tk_image = None

        # --- Layout ---
        self.main_frame = tk.Frame(self.root, bg="#2c2c2c")
        self.main_frame.pack(fill="both", expand=True)

        self.btn_frame = tk.Frame(self.main_frame, bg="#2c2c2c")
        self.btn_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame = tk.Frame(self.main_frame, bg="#2c2c2c")
        self.right_frame.pack(side="right", expand=True, fill="both")

        # Canvas
        self.canvas_w, self.canvas_h = 650, 450
        self.canvas = tk.Canvas(
            self.right_frame,
            width=self.canvas_w,
            height=self.canvas_h,
            bg="#2c2c2c",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        self.draw_image(self.current_img)

        # Panel frame
        self.panel_frame = tk.Frame(self.right_frame, bg="#3a3a3a")
        self.panel_frame.pack(fill="x", padx=20, pady=10)

        # Buttons
        self.add_button("Open Image", self.open_image)
        self.add_button("RGB", self.show_rgb_panel)
        self.add_button("Brightness", self.show_brightness_panel)
        self.add_button("Saturation", self.show_saturation_panel)
        self.add_button("Blur", self.show_blur_panel)
        self.add_button("Stretch", self.show_stretch_panel)
        self.add_button("Reset", self.reset_image, "#f44336")
        self.add_button("Save As", self.save_as, "#2196F3")

    # --- Button helper ---
    def add_button(self, text, command, bg="#4CAF50"):
        row = len([w for w in self.btn_frame.grid_slaves() if isinstance(w, tk.Button)])
        btn = tk.Button(
            self.btn_frame,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            bg=bg,
            fg="white",
            relief="flat",
            width=14,
            height=2
        )
        btn.grid(row=row + 1, column=0, pady=6, sticky="n")

    def clear_panel(self):
        for widget in self.panel_frame.winfo_children():
            widget.destroy()

    # --- Draw image ---
    def draw_image(self, img):
        orig_w, orig_h = img.size
        scale = min(self.canvas_w / orig_w, self.canvas_h / orig_h)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        img_resized = img.resize((new_w, new_h), Image.LANCZOS)
        self.displayed_img = img_resized.copy()
        self.tk_image = ImageTk.PhotoImage(img_resized)
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas_w // 2, self.canvas_h // 2, image=self.tk_image)

    # --- Panels ---
    def show_rgb_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="RGB Adjustments", bg="#3a3a3a", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
        sliders = {}

        def slider_update(_=None):
            r = sliders["Red"].get()
            g = sliders["Green"].get()
            b = sliders["Blue"].get()
            self.current_img = adjust_rgb(self.current_img, r, g, b)
            self.draw_image(self.current_img)

        for color in ("Red", "Green", "Blue"):
            tk.Label(self.panel_frame, text=color, bg="#3a3a3a", fg="white").pack()
            slider = ctk.CTkSlider(self.panel_frame, from_=0, to=2, number_of_steps=20, command=slider_update)
            slider.set(1.0)
            slider.pack(fill="x", padx=20, pady=5)
            sliders[color] = slider

    def show_brightness_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Brightness & Sharpness", bg="#3a3a3a", fg="white").pack(pady=5)

        def update(_=None):
            b_val = bright_slider.get()
            s_val = sharp_slider.get()
            self.current_img = adjust_brightness(self.current_img, b_val)
            self.current_img = adjust_sharpness(self.current_img, s_val)
            self.draw_image(self.current_img)

        tk.Label(self.panel_frame, text="Brightness", bg="#3a3a3a", fg="white").pack()
        bright_slider = ctk.CTkSlider(self.panel_frame, from_=0, to=2, number_of_steps=20, command=update)
        bright_slider.set(1.0)
        bright_slider.pack(fill="x", padx=20, pady=5)

        tk.Label(self.panel_frame, text="Sharpness", bg="#3a3a3a", fg="white").pack()
        sharp_slider = ctk.CTkSlider(self.panel_frame, from_=0, to=3, number_of_steps=30, command=update)
        sharp_slider.set(1.0)
        sharp_slider.pack(fill="x", padx=20, pady=5)

    def show_saturation_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Saturation", bg="#3a3a3a", fg="white").pack(pady=5)

        def update(val):
            self.current_img = adjust_saturation(self.current_img, float(val))
            self.draw_image(self.current_img)

        sat_slider = ctk.CTkSlider(self.panel_frame, from_=0, to=3, number_of_steps=30, command=update)
        sat_slider.set(1.0)
        sat_slider.pack(fill="x", padx=20, pady=5)

    def show_blur_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Blur", bg="#3a3a3a", fg="white").pack(pady=5)

        def update(val):
            self.current_img = adjust_blur(self.current_img, float(val))
            self.draw_image(self.current_img)

        blur_slider = ctk.CTkSlider(self.panel_frame, from_=0, to=10, number_of_steps=20, command=update)
        blur_slider.set(0)
        blur_slider.pack(fill="x", padx=20, pady=5)

    def show_stretch_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Stretch", bg="#3a3a3a", fg="white").pack(pady=5)

        def update(_=None):
            w_factor = max(0.05, width_slider.get())
            h_factor = max(0.05, height_slider.get())
            self.current_img = stretch_image(self.current_img, width_factor=w_factor, height_factor=h_factor)
            self.draw_image(self.current_img)

        tk.Label(self.panel_frame, text="Width Stretch", bg="#3a3a3a", fg="white").pack()
        width_slider = ctk.CTkSlider(self.panel_frame, from_=0.2, to=3.0, number_of_steps=28, command=update)
        width_slider.set(1.0)
        width_slider.pack(fill="x", padx=20, pady=5)

        tk.Label(self.panel_frame, text="Height Stretch", bg="#3a3a3a", fg="white").pack()
        height_slider = ctk.CTkSlider(self.panel_frame, from_=0.2, to=3.0, number_of_steps=28, command=update)
        height_slider.set(1.0)
        height_slider.pack(fill="x", padx=20, pady=5)

    # --- Extra features ---
    def reset_image(self):
        self.current_img = self.original_img.copy()
        self.draw_image(self.current_img)

    def save_as(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
        )
        if save_path:
            self.current_img.save(save_path)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        )
        if file_path:
            self.current_image_path = file_path
            self.original_img = Image.open(file_path).convert("RGB")
            self.current_img = self.original_img.copy()
            self.draw_image(self.current_img)
