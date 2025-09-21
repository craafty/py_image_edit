import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from image_functions import (
    adjust_rgb,
    adjust_saturation,
    adjust_brightness,
    adjust_sharpness,
    adjust_blur,
    stretch_image,
)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1000x800")
        self.root.configure(bg="#2c2c2c")

        # Load default image
        self.original_img = Image.open("example.jpg").convert("RGB")
        self.current_img = self.original_img.copy()

        # Canvas for image (use label; we'll scale the image to fit available window)
        self.canvas = tk.Label(root, bg="#2c2c2c")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        button_frame = tk.Frame(root, bg="#2c2c2c")
        button_frame.pack(fill="x", pady=(0, 5))
        self.add_button(button_frame, "Open Image", self.open_image)
        self.add_button(button_frame, "RGB", self.show_rgb_panel)
        self.add_button(button_frame, "Brightness", self.show_brightness_panel)
        self.add_button(button_frame, "Saturation", self.show_saturation_panel)
        self.add_button(button_frame, "Blur", self.show_blur_panel)
        self.add_button(button_frame, "Stretch", self.show_stretch_panel)
        self.add_button(button_frame, "Reset", self.reset_image, bg="#f44336")
        self.add_button(button_frame, "Save As", self.save_as, bg="#2196F3")

        # Panel frame (sliders will appear here)
        self.panel_frame = tk.Frame(root, bg="#3a3a3a")
        self.panel_frame.pack(fill="x", padx=20, pady=(0, 10))

        # Create all sliders once
        self.create_sliders()

        # initial draw
        self.update_image()

    # --- Image display: scale to fit available area but preserve stretched aspect ratio ---
    def draw_image(self, img):
        # ensure geometry info is up to date
        self.root.update_idletasks()

        # compute available area (leave margins for UI)
        avail_w = max(self.root.winfo_width() - 40, 200)
        # estimate available height: window height minus space for controls
        # panel_frame + button_frame heights are small; give a safe default
        avail_h = max(self.root.winfo_height() - self.panel_frame.winfo_height() - 120, 200)

        img_w, img_h = img.size
        # scale down/up proportionally so the stretched image fits inside available area
        scale = min(avail_w / img_w, avail_h / img_h)
        # avoid zero
        new_w = max(1, int(img_w * scale))
        new_h = max(1, int(img_h * scale))

        img_resized = img.resize((new_w, new_h), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img_resized)
        self.canvas.configure(image=self.tk_image)
        self.canvas.image = self.tk_image

    # --- Update image using all slider values ---
    def update_image(self, _=None):
        # start from original each time (edits are cumulative in this pipeline)
        img = self.original_img.copy()

        # color / enhancements
        img = adjust_rgb(img, self.r_slider.get(), self.g_slider.get(), self.b_slider.get())
        img = adjust_brightness(img, self.bright_slider.get())
        img = adjust_sharpness(img, self.sharp_slider.get())
        img = adjust_saturation(img, self.sat_slider.get())
        img = adjust_blur(img, self.blur_slider.get())

        # apply stretching (non-uniform)
        # clamp the slider values to reasonable range to avoid accidental 0 or negative
        w_factor = max(0.05, min(self.width_slider.get(), 10.0))
        h_factor = max(0.05, min(self.height_slider.get(), 10.0))
        img = stretch_image(img, width_factor=w_factor, height_factor=h_factor)

        self.current_img = img
        self.draw_image(img)

    # --- Buttons ---
    def add_button(self, parent, text, command, bg="#4CAF50"):
        btn = tk.Button(parent, text=text, command=command,
                        font=("Arial", 12, "bold"),
                        bg=bg, fg="white",
                        relief="flat", padx=12, pady=8)
        btn.pack(side="left", padx=6)

    # --- Create all sliders ---
    def create_sliders(self):
        # RGB sliders
        self.r_slider = tk.Scale(self.panel_frame, from_=0, to=2, resolution=0.05, orient="horizontal",
                                 label="Red", command=self.update_image)
        self.g_slider = tk.Scale(self.panel_frame, from_=0, to=2, resolution=0.05, orient="horizontal",
                                 label="Green", command=self.update_image)
        self.b_slider = tk.Scale(self.panel_frame, from_=0, to=2, resolution=0.05, orient="horizontal",
                                 label="Blue", command=self.update_image)
        for s in (self.r_slider, self.g_slider, self.b_slider):
            s.set(1.0)

        # Brightness & Sharpness
        self.bright_slider = tk.Scale(self.panel_frame, from_=0, to=2, resolution=0.05, orient="horizontal",
                                      label="Brightness", command=self.update_image)
        self.sharp_slider = tk.Scale(self.panel_frame, from_=0, to=3, resolution=0.05, orient="horizontal",
                                     label="Sharpness", command=self.update_image)
        self.bright_slider.set(1.0)
        self.sharp_slider.set(1.0)

        # Saturation
        self.sat_slider = tk.Scale(self.panel_frame, from_=0, to=3, resolution=0.05, orient="horizontal",
                                   label="Saturation", command=self.update_image)
        self.sat_slider.set(1.0)

        # Blur
        self.blur_slider = tk.Scale(self.panel_frame, from_=0, to=10, resolution=0.5, orient="horizontal",
                                    label="Blur", command=self.update_image)
        self.blur_slider.set(0)

        # Stretch sliders (width and height multipliers)
        # Use float range with fine resolution; 1 = original, <1 shrink, >1 expand
        self.width_slider = tk.Scale(self.panel_frame, from_=0.2, to=3.0, resolution=0.02, orient="horizontal",
                                     label="Width Stretch", command=self.update_image)
        self.height_slider = tk.Scale(self.panel_frame, from_=0.2, to=3.0, resolution=0.02, orient="horizontal",
                                      label="Height Stretch", command=self.update_image)
        self.width_slider.set(1.0)
        self.height_slider.set(1.0)

        # Hide all sliders initially
        for s in (self.r_slider, self.g_slider, self.b_slider,
                  self.bright_slider, self.sharp_slider,
                  self.sat_slider, self.blur_slider,
                  self.width_slider, self.height_slider):
            s.pack_forget()

    # --- Show panels ---
    def show_rgb_panel(self):
        self.clear_panel()
        for s in (self.r_slider, self.g_slider, self.b_slider):
            s.pack(fill="x", padx=12, pady=2)
        self.update_image()

    def show_brightness_panel(self):
        self.clear_panel()
        for s in (self.bright_slider, self.sharp_slider):
            s.pack(fill="x", padx=12, pady=2)
        self.update_image()

    def show_saturation_panel(self):
        self.clear_panel()
        self.sat_slider.pack(fill="x", padx=12, pady=2)
        self.update_image()

    def show_blur_panel(self):
        self.clear_panel()
        self.blur_slider.pack(fill="x", padx=12, pady=2)
        self.update_image()

    def show_stretch_panel(self):
        self.clear_panel()
        self.width_slider.pack(fill="x", padx=12, pady=2)
        self.height_slider.pack(fill="x", padx=12, pady=2)
        self.update_image()

    def clear_panel(self):
        for widget in self.panel_frame.winfo_children():
            widget.pack_forget()

    # --- Extra Features ---
    def reset_image(self):
        self.original_img = self.original_img  # keep same original
        self.current_img = self.original_img.copy()
        self.draw_image(self.current_img)
        # Reset sliders
        for s in (self.r_slider, self.g_slider, self.b_slider,
                  self.bright_slider, self.sharp_slider,
                  self.sat_slider, self.blur_slider):
            if s is self.blur_slider:
                s.set(0)
            else:
                s.set(1.0)
        self.width_slider.set(1.0)
        self.height_slider.set(1.0)

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
            self.original_img = Image.open(file_path).convert("RGB")
            self.current_img = self.original_img.copy()
            # reset sliders to sensible defaults (keeps user from accidentally applying previous stretch)
            self.width_slider.set(1.0)
            self.height_slider.set(1.0)
            self.reset_image()
