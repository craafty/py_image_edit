import tkinter as tk
from PIL import Image, ImageTk
import time
from imageFunctions import adjust_rgb

class App():

    def __init__(self, root):
        self.root = root
        self.root.title("image editor")
        self.root.geometry("800x800")
        self.win_width, self.win_height = 800, 800
        self.margin = 40
        
        self.current_image = "example.jpg"
        self.draw_image(self.current_image)

        self.r_slider = tk.Scale(root, from_=0, to=2, resolution=0.1,
                                 orient="horizontal", label="Red", command=self.update_image)
        self.r_slider.set(1.0)
        self.r_slider.place(x=100, y=700)

        self.g_slider = tk.Scale(root, from_=0, to=2, resolution=0.1,
                                 orient="horizontal", label="Green", command=self.update_image)
        self.g_slider.set(1.0)
        self.g_slider.place(x=300, y=700)

        self.b_slider = tk.Scale(root, from_=0, to=2, resolution=0.1,
                                 orient="horizontal", label="Blue", command=self.update_image)
        self.b_slider.set(1.0)
        self.b_slider.place(x=500, y=700)

        self.button = tk.Button(root, text="test", command=lambda: 
            (
                adjust_rgb("example.jpg", 1.0, 1.0, 0.0, "new_example.jpg"),
                self.draw_image("new_example.jpg")
            ))
        self.button.update_idletasks()  # calculate button width
        btn_width = self.button.winfo_reqwidth()
        btn_height = self.button.winfo_reqheight()
        self.button.place(x=(self.win_width - btn_width)//2, y=self.win_height - btn_height - 10)
        
        
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
        self.resized_img = self.resize_for_window(Image.open(path))
        self.tk_image = ImageTk.PhotoImage(self.resized_img)

        if hasattr(self, "labelImage"):  # if label already exists, just update it
            self.labelImage.configure(image=self.tk_image)
            self.labelImage.image = self.tk_image
            self.center_image()
        else:  # first time, actually create it
            self.labelImage = tk.Label(self.root, image=self.tk_image)
            self.labelImage.image = self.tk_image
            self.center_image()


    def save_func(self):
        print("saved the image")

    def update_image(self, _=None):
        r = self.r_slider.get()
        g = self.g_slider.get()
        b = self.b_slider.get()

        adjust_rgb("example.jpg", r, g, b, "preview.jpg")
        self.draw_image("preview.jpg")