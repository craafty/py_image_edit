import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from image_functions import (
    adjust_rgb,
    adjust_saturation,
    adjust_brightness,
    adjust_sharpness,
    adjust_blur,
    adjust_stretch,
    adjust_flip
)
import customtkinter as ctk

# --- Set CustomTkinter appearance ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("600x700")
        self.root.configure(bg="#2c2c2c")
        self.root.resizable(False, False)

        # --- Image variables ---
        #self.current_image_path = "example.jpg"
        #self.original_image = Image.open(self.current_image_path)
        #self.current_image_obj = self.original_image.copy()

        self.current_image_path = None
        self.original_image = None
        self.current_image_obj = None

        # Store cumulative slider values
        self.values = {
            "Red": 1.0,
            "Green": 1.0,
            "Blue": 1.0,
            "Brightness": 1.0,
            "Sharpness": 1.0,
            "Saturation": 1.0,
            "Blur": 0.0,
            "Flip_H": False,
            "Flip_V": False,
            "Stretch_H": 1.0,
            "Stretch_V": 1.0
        }

        # Crop mode variables
        self.crop_mode = False
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.offset_x = 0
        self.offset_y = 0
        self.scale = 1.0

        # --- Main Layout ---
        self.main_frame = tk.Frame(self.root, bg="#2c2c2c")
        self.main_frame.pack(fill="both", expand=True)

        # Left: Buttons Sidebar
        self.btn_frame = tk.Frame(self.main_frame, bg="#2c2c2c")
        self.btn_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.btn_frame.grid_rowconfigure(99, weight=1)

        # Right: Image + Sliders
        self.right_frame = tk.Frame(self.main_frame, bg="#2c2c2c")
        self.right_frame.pack(side="right", expand=True, fill="both")

        # --- Image Canvas ---
        self.canvas_w, self.canvas_h = 450, 450
        self.canvas = tk.Canvas(
            self.right_frame,
            width=self.canvas_w,
            height=self.canvas_h,
            bg="#2c2c2c",
            highlightthickness=0
        )
        self.canvas.pack(pady=20, padx=20)
        self.tk_image = None
        #self.draw_image(self.current_image_obj)
        self.canvas.create_text(
            self.canvas_w // 2,
            self.canvas_h // 2,
            text="No Image Loaded",
            fill="white",
            font=("Arial", 14, "bold")
        )

        # Bind crop events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # --- Dynamic Panel Area ---
        self.panel_frame = tk.Frame(self.right_frame, bg="#3a3a3a")
        self.panel_frame.pack(fill="x", padx=20, pady=10)

        # --- Buttons ---
        #self.add_button("Close", self.root.destroy, "#f44336")
        self.add_button("Open Image", self.open_image, "#2196F3")
        self.add_button("RGB", self.show_rgb_panel, "#4CAF50")
        self.add_button("Brightness", self.show_brightness_panel, "#4CAF50")
        self.add_button("Sharpness", self.show_sharpness_panel, "#4CAF50")
        self.add_button("Saturation", self.show_saturation_panel, "#4CAF50")
        self.add_button("Blur", self.show_blur_panel, "#4CAF50")
        self.add_button("Crop", self.enable_crop_mode, "#4CAF50")
        self.add_button("Stretch", self.show_stretch_panel, "#4CAF50")
        self.add_button("Flip", self.show_flip_panel, "#4CAF50")
        self.add_button("Reset", self.reset_image, "#f44336")
        self.add_button("Save As", self.save_as, "#2196F3")

    def require_image(func):
        def wrapper(self, *args, **kwargs):
            if self.original_image is None:
                return  # no image loaded → ignore button press
            return func(self, *args, **kwargs)
        return wrapper

    # --- Button Helper ---
    def add_button(self, text, command, bg):
        row = len([w for w in self.btn_frame.grid_slaves() if isinstance(w, tk.Button)])
        btn = tk.Button(
            self.btn_frame, text=text, command=command,
            font=("Arial", 11, "bold"),
            bg=bg, fg="white", relief="flat",
            width=14, height=2
        )
        btn.grid(row=row + 1, column=0, pady=6, sticky="n")
        def on_enter(e): btn.config(bg="#333333")
        def on_leave(e): btn.config(bg=bg)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def clear_panel(self):
        for widget in self.panel_frame.winfo_children():
            widget.destroy()

    # --- Draw Image ---
    def draw_image(self, img_source):
        img = img_source.copy() if isinstance(img_source, Image.Image) else Image.open(img_source)
        orig_w, orig_h = img.size
        self.scale = min(self.canvas_w / orig_w, self.canvas_h / orig_h)
        new_w, new_h = int(orig_w * self.scale), int(orig_h * self.scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.offset_x = (self.canvas_w - new_w) // 2
        self.offset_y = (self.canvas_h - new_h) // 2
        self.canvas.create_image(self.canvas_w // 2, self.canvas_h // 2, image=self.tk_image)

    # --- Apply all active sliders ---
    def apply_all_adjustments(self):
        img = self.original_image.copy()
        # RGB
        img = adjust_rgb(img, self.values["Red"], self.values["Green"], self.values["Blue"])
        # Brightness & Sharpness
        img = adjust_brightness(img, self.values["Brightness"])
        img = adjust_sharpness(img, self.values["Sharpness"])
        # Saturation
        img = adjust_saturation(img, self.values["Saturation"])
        # Blur
        img = adjust_blur(img, self.values["Blur"])
        # Stretch
        img = adjust_stretch(img, self.values["Stretch_H"], self.values["Stretch_V"])
        # Flips
        img = adjust_flip(img, self.values["Flip_H"], self.values["Flip_V"])

        self.current_image_obj = img
        self.draw_image(img)


    # --- Crop Mode ---
    def enable_crop_mode(self):
        self.crop_mode = True
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None

    def on_button_press(self, event):
        if not self.crop_mode:
            return
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        if not self.rect:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.rect)

        # Convert canvas coords to original image coords
        left = int((min(x1, x2) - self.offset_x) / self.scale)
        top = int((min(y1, y2) - self.offset_y) / self.scale)
        right = int((max(x1, x2) - self.offset_x) / self.scale)
        bottom = int((max(y1, y2) - self.offset_y) / self.scale)

        # Account for horizontal flip
        if self.values["Flip_H"]:
            w, _ = self.original_image.size
            left, right = w - right, w - left

        # Account for vertical flip
        if self.values["Flip_V"]:
            _, h = self.original_image.size
            top, bottom = h - bottom, h - top

        # Crop the original image
        self.original_image = self.original_image.crop((left, top, right, bottom))
        self.apply_all_adjustments()
        self.crop_mode = False
        self.rect = None

    # --- Panel Creators ---
    @require_image
    def show_rgb_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="RGB Adjustments", bg="#3a3a3a", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
        sliders = {}

        def update_rgb(val=None):
            self.values["Red"] = sliders["Red"].get()
            self.values["Green"] = sliders["Green"].get()
            self.values["Blue"] = sliders["Blue"].get()
            self.apply_all_adjustments()

        for color in ("Red", "Green", "Blue"):
            tk.Label(self.panel_frame, text=color, bg="#3a3a3a", fg="white").pack(anchor="w", padx=10)
            slider = ctk.CTkSlider(self.panel_frame, from_=0, to=2, number_of_steps=20, command=update_rgb)
            slider.set(self.values[color])
            slider.pack(fill="x", padx=20, pady=5)
            sliders[color] = slider

    @require_image
    def show_brightness_panel(self):
        self.clear_panel()
        tk.Label(
            self.panel_frame,
            text="Brightness",
            bg="#3a3a3a",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        slider = ctk.CTkSlider(
            self.panel_frame,
            from_=0,
            to=2,
            number_of_steps=20,
            command=lambda val: self.update_slider("Brightness", val)
        )
        slider.set(self.values["Brightness"])
        slider.pack(fill="x", padx=20, pady=5)

    @require_image
    def show_sharpness_panel(self):
        self.clear_panel()
        tk.Label(
            self.panel_frame,
            text="Sharpness",
            bg="#3a3a3a",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        slider = ctk.CTkSlider(
            self.panel_frame,
            from_=0,
            to=3,
            number_of_steps=20,
            command=lambda val: self.update_slider("Sharpness", val)
        )
        slider.set(self.values["Sharpness"])
        slider.pack(fill="x", padx=20, pady=5)

    @require_image
    def show_stretch_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Stretch Image", bg="#3a3a3a", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
        sliders = {}

        def update_stretch(val=None):
            self.values["Stretch_H"] = sliders["Horizontal"].get()
            self.values["Stretch_V"] = sliders["Vertical"].get()
            self.apply_all_adjustments()

        for label, key in [("Horizontal", "Stretch_H"), ("Vertical", "Stretch_V")]:
            tk.Label(self.panel_frame, text=label, bg="#3a3a3a", fg="white").pack(anchor="w", padx=10)
            slider = ctk.CTkSlider(
                self.panel_frame, from_=0.1, to=3, number_of_steps=29,
                command=update_stretch
            )
            slider.set(self.values[key])
            slider.pack(fill="x", padx=20, pady=5)
            sliders[label] = slider

    @require_image
    def show_saturation_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Saturation", bg="#3a3a3a", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
        slider = ctk.CTkSlider(self.panel_frame, from_=0, to=3, number_of_steps=30, command=lambda val: self.update_slider("Saturation", val))
        slider.set(self.values["Saturation"])
        slider.pack(fill="x", padx=20, pady=5)

    @require_image
    def show_blur_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Blur", bg="#3a3a3a", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
        slider = ctk.CTkSlider(self.panel_frame, from_=0, to=10, number_of_steps=20, command=lambda val: self.update_slider("Blur", val))
        slider.set(self.values["Blur"])
        slider.pack(fill="x", padx=20, pady=5)

    @require_image
    def update_slider(self, key, val):
        self.values[key] = float(val)
        self.apply_all_adjustments()

    @require_image
    def show_flip_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Flip Image", bg="#3a3a3a", fg="white", font=("Arial", 12, "bold")).pack(pady=5)

        def toggle_h():
            self.values["Flip_H"] = not self.values["Flip_H"]
            self.apply_all_adjustments()

        def toggle_v():
            self.values["Flip_V"] = not self.values["Flip_V"]
            self.apply_all_adjustments()

        flip_h_switch = ctk.CTkSwitch(
            self.panel_frame,
            text="Flip Horizontal",
            command=toggle_h
        )
        flip_h_switch.select() if self.values["Flip_H"] else flip_h_switch.deselect()
        flip_h_switch.pack(pady=10, padx=20, anchor="w")

        flip_v_switch = ctk.CTkSwitch(
            self.panel_frame,
            text="Flip Vertical",
            command=toggle_v
        )
        flip_v_switch.select() if self.values["Flip_V"] else flip_v_switch.deselect()
        flip_v_switch.pack(pady=10, padx=20, anchor="w")


    def apply_flip(self):
        self.values["Flip_H"] = self.flip_h_var.get()
        self.values["Flip_V"] = self.flip_v_var.get()
        self.apply_all_adjustments()


    # --- Extra features ---
    def reset_image(self):
        self.original_image = Image.open(self.current_image_path).convert("RGB")
        # Reset numeric values
        self.reset_values()
        self.apply_all_adjustments()

    def reset_values(self):
        self.values.update({
            "Red": 1.0,
            "Green": 1.0,
            "Blue": 1.0,
            "Brightness": 1.0,
            "Sharpness": 1.0,
            "Saturation": 1.0,
            "Blur": 0.0,
            "Flip_H": False,
            "Flip_V": False,
            "Stretch_H": 1.0,
            "Stretch_V": 1.0
        })

    def save_as(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
        )
        if save_path:
            self.current_image_obj.save(save_path)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.bmp *.gif"), ("All files", "*.*")]
        )
        if file_path:
            self.current_image_path = file_path  # <-- update the path
            self.original_image = Image.open(file_path).convert("RGB")
            self.current_image_obj = self.original_image.copy()

            # Reset all slider values
            self.reset_values()

            # Redraw image
            self.apply_all_adjustments()

