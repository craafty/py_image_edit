import tkinter as tk
from PIL import Image

img = Image.open("example.jpg")
r, g, b = img.split()  # Split into individual channels

# Reduce red by 50%
g = g.point(lambda i: i * 0.0)

# Recombine channels
new_img = Image.merge("RGB", (r, g, b))
new_img.save("reduced_red.jpg")

"""
root = tk.Tk()
root.title("window title")
root.geometry("400x300")

label = tk.Label(root, text="Hello World", font=("Arial", 16))
label.pack(pady=20)

root.mainloop()
"""