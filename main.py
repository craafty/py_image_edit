import tkinter as tk

root = tk.Tk()
root.title("window title")
root.geometry("400x300")

label = tk.Label(root, text="Hello World", font=("Arial", 16))
label.pack(pady=20)

root.mainloop()

