import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from imageFunctions import (adjust_rgb, adjust_brightness_sharpness, adjust_saturation, adjust_blur)
import customtkinter as ctk

# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # options: "blue", "green", "dark-blue"
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
        self.root.geometry("700x700")
        self.root.configure(bg="#2c2c2c")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        # --- Image variables ---
        self.current_image_path = "example.jpg"
        self.current_image_obj = Image.open(self.current_image_path)
        self.preview_image = "preview.jpg"

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
        self.btn_frame.grid_rowconfigure(0, weight=1)
        self.btn_frame.grid_rowconfigure(99, weight=1)

        # Right: Image + Sliders
        self.right_frame = tk.Frame(self.main_frame, bg="#2c2c2c")
        self.right_frame.pack(side="right", expand=True, fill="both")

        # --- Image Canvas ---
        self.canvas_w, self.canvas_h = 650, 450
        self.canvas = tk.Canvas(self.right_frame, width=self.canvas_w, height=self.canvas_h, bg="#2c2c2c", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.displayed_img = None
        self.tk_image = None
        self.draw_image(self.current_image_obj)

        # Bind crop events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # --- Dynamic Panel Area ---
        self.panel_frame = tk.Frame(self.right_frame, bg="#3a3a3a")
        self.panel_frame.pack(fill="x", padx=20, pady=10)

        # --- Buttons ---
        self.add_button("RGB", self.show_rgb_panel, "#4CAF50")
        self.add_button("Brightness", self.show_brightness_panel, "#4CAF50")
        self.add_button("Saturation", self.show_saturation_panel, "#4CAF50")
        self.add_button("Blur", self.show_blur_panel, "#4CAF50")
        self.add_button("Crop", self.enable_crop_mode, "#FFC107")
        self.add_button("Reset", self.reset_image, "#f44336")
        self.add_button("Save As", self.save_as, "#2196F3")

    # --- Button Helper ---
    def add_button(self, text, command, bg):
        row = len([w for w in self.btn_frame.grid_slaves() if isinstance(w, tk.Button)])
        btn = tk.Button(
            self.btn_frame, text=text, command=command,
            font=("Arial", 11, "bold"),
            bg=bg, fg="white", relief="flat",
            width=14, height=2
        )
        btn.grid(row=row+1, column=0, pady=6, sticky="n")
        def on_enter(e): btn.config(bg="#333333")
        def on_leave(e): btn.config(bg=bg)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def clear_panel(self):
        for widget in self.panel_frame.winfo_children():
            widget.destroy()

    # --- Draw Image ---
    def draw_image(self, img_source):
        if isinstance(img_source, Image.Image):
            img = img_source.copy()
        else:
            img = Image.open(img_source)

        orig_w, orig_h = img.size
        scale = min(self.canvas_w / orig_w, self.canvas_h / orig_h)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)

        self.displayed_img = img.copy()
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.offset_x = (self.canvas_w - new_w)//2
        self.offset_y = (self.canvas_h - new_h)//2
        self.scale = scale
        self.canvas.create_image(self.canvas_w//2, self.canvas_h//2, image=self.tk_image)

    # --- Update Image ---
    def update_image(self, func, *args):
        func(self.current_image_obj, *args, save_path=self.preview_image)
        self.current_image_obj = Image.open(self.preview_image)
        self.draw_image(self.current_image_obj)

    # --- Crop Mode ---
    def enable_crop_mode(self):
        self.crop_mode = True
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None

    def on_button_press(self, event):
        if not self.crop_mode or self.displayed_img is None:
            return
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_drag(self, event):
        if not self.crop_mode or self.rect is None:
            return
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        if not self.crop_mode or self.rect is None:
            return

        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        left = int((min(x1, x2) - self.offset_x) / self.scale)
        top = int((min(y1, y2) - self.offset_y) / self.scale)
        right = int((max(x1, x2) - self.offset_x) / self.scale)
        bottom = int((max(y1, y2) - self.offset_y) / self.scale)

        cropped_img = self.current_image_obj.crop((left, top, right, bottom))
        self.current_image_obj = cropped_img
        self.draw_image(self.current_image_obj)

        self.crop_mode = False
        self.rect = None

    # --- Panel Creators with CustomTkinter sliders ---
    def show_rgb_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="RGB Adjustments", bg="#3a3a3a", fg="white").pack()

        r_slider = tk.Scale(
            self.panel_frame, from_=0, to=2, resolution=0.1, orient="horizontal",
            label="Red", command=lambda _: self.update_image(adjust_rgb, r_slider.get(), g_slider.get(), b_slider.get())
        )
        r_slider.set(1.0)
        r_slider.pack(fill="x", padx=20)

        g_slider = tk.Scale(
            self.panel_frame, from_=0, to=2, resolution=0.1, orient="horizontal",
            label="Green", command=lambda _: self.update_image(adjust_rgb, r_slider.get(), g_slider.get(), b_slider.get())
        )
        g_slider.set(1.0)
        g_slider.pack(fill="x", padx=20)

        b_slider = tk.Scale(
            self.panel_frame, from_=0, to=2, resolution=0.1, orient="horizontal",
            label="Blue", command=lambda _: self.update_image(adjust_rgb, r_slider.get(), g_slider.get(), b_slider.get())
        )
        b_slider.set(1.0)
        b_slider.pack(fill="x", padx=20)

    def show_brightness_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Brightness & Sharpness", bg="#3a3a3a", fg="white").pack()

        bright_slider = tk.Scale(
            self.panel_frame, from_=0, to=2, resolution=0.1, orient="horizontal",
            label="Brightness", command=lambda _: self.update_image(adjust_brightness_sharpness, bright_slider.get(), sharp_slider.get())
        )
        bright_slider.set(1.0)
        bright_slider.pack(fill="x", padx=20)

        sharp_slider = tk.Scale(
            self.panel_frame, from_=0, to=3, resolution=0.1, orient="horizontal",
            label="Sharpness", command=lambda _: self.update_image(adjust_brightness_sharpness, bright_slider.get(), sharp_slider.get())
        )
        sharp_slider.set(1.0)
        sharp_slider.pack(fill="x", padx=20)

    def show_saturation_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Saturation", bg="#3a3a3a", fg="white").pack()

        sat_slider = tk.Scale(
            self.panel_frame, from_=0, to=3, resolution=0.1, orient="horizontal",
            label="Saturation", command=lambda _: self.update_image(adjust_saturation, sat_slider.get())
        )
        sat_slider.set(1.0)
        sat_slider.pack(fill="x", padx=20)

    def show_blur_panel(self):
        self.clear_panel()
        tk.Label(self.panel_frame, text="Blur", bg="#3a3a3a", fg="white").pack()

        blur_slider = tk.Scale(
            self.panel_frame, from_=0, to=10, resolution=0.5, orient="horizontal",
            label="Blur", command=lambda _: self.update_image(adjust_blur, blur_slider.get())
        )
        blur_slider.set(0.0)
        blur_slider.pack(fill="x", padx=20)

    # --- Extra Features ---
    def reset_image(self):
        """Reload original image (clear edits)."""
        self.draw_image(self.current_image)

    def save_as(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
        )
        if save_path:
            Image.open(self.preview_image).save(save_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

