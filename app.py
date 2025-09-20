import tkinter as tk
from PIL import Image, ImageTk
from imageFunctions import (adjust_rgb, adjust_brightness_sharpness, adjust_saturation, adjust_blur)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1000x800")
        self.root.configure(bg="#2c2c2c")  # dark theme

        self.current_image = "example.jpg"   # original
        self.preview_image = "preview.jpg"   # edited

        # --- Canvas for image ---
        self.canvas = tk.Label(root, bg="#2c2c2c")
        self.canvas.pack(pady=20)
        self.draw_image(self.current_image)

        # --- Buttons Row ---
        button_frame = tk.Frame(self.root, bg="#2c2c2c")
        button_frame.pack(pady=10)

        self.add_button(button_frame, "RGB", self.show_rgb_panel)
        self.add_button(button_frame, "Brightness", self.show_brightness_panel)
        self.add_button(button_frame, "Saturation", self.show_saturation_panel)
        self.add_button(button_frame, "Blur", self.show_blur_panel)
        self.add_button(button_frame, "Reset", self.reset_image, bg="#f44336")  # red button
        self.add_button(button_frame, "Save As", self.save_as, bg="#2196F3")   # blue button

        # --- Dynamic Panel Area ---
        self.panel_frame = tk.Frame(self.root, bg="#3a3a3a")
        self.panel_frame.pack(fill="x", padx=20, pady=10)

    def add_button(self, parent, text, command, bg="#4CAF50"):
        """Create styled buttons."""
        btn = tk.Button(
            parent, text=text, command=command,
            font=("Arial", 12, "bold"),
            bg=bg, fg="white",
            relief="flat", padx=15, pady=10
        )
        btn.pack(side="left", padx=10)

    def clear_panel(self):
        """Remove old sliders before showing new ones."""
        for widget in self.panel_frame.winfo_children():
            widget.destroy()

    def draw_image(self, path):
        img = Image.open(path)
        img = img.resize((600, 400))  # scale to fit
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.configure(image=self.tk_image)
        self.canvas.image = self.tk_image

    def update_image(self, func, *args):
        func(self.current_image, *args, save_path=self.preview_image)
        self.draw_image(self.preview_image)

    # --- Panel Creators ---
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
        """Save edited image as a new file."""
        from tkinter import filedialog
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

