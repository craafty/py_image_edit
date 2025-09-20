import tkinter as tk
from PIL import Image, ImageTk
import time

class App():

    def __init__(self, root):
        self.root = root
        self.root.title("image editor")
        self.root.geometry("800x800")
        self.win_width, self.win_height = 800, 800
        self.margin = 40
        
        img = Image.open("example.jpg")
        self.resized_img = self.resize_for_window(img)
        self.tk_image = ImageTk.PhotoImage(self.resized_img)
        
        self.labelImage = tk.Label(root, image=self.tk_image)
        self.center_image()

        self.button = tk.Button(root, text="save", command=self.save_func)
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

    def save_func(self):
        print("saved the image")

