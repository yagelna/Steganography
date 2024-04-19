from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from stegano import lsb

def center_window(window, width, height):
    x = (window.winfo_screenwidth()/2) - (width/2)
    y = (window.winfo_screenheight()/2) - (height/2)
    window.geometry("%dx%d+%d+%d" % (width, height, x, y))

def open_image():
    global file_path
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("PNG files", "*.png"),("JPG Files","*.jpg")])
    
    if file_path:
        image = Image.open(file_path)
        image = image.resize((400, 400))
        photo = ImageTk.PhotoImage(image)
        canvas.delete("image")
        canvas.create_image(0, 0, anchor=tk.NW, image=photo, tags="image")
        canvas.image = photo

def save_image():
    try:
        encoded.save("EncodedMessage.png")
    except NameError:
        messagebox.showwarning("No Image", "Please open and encode some image!")
    
def encode_message():
    global encoded
    text = text_box.get(1.0, END)
    if text:
        try:
            encoded = lsb.hide(str(file_path), text)
            text_box.delete(1.0, END)
        except NameError:
            messagebox.showwarning("No Image", "Please open some image!")
    else:
        messagebox.showwarning("No Text", "The text box is empty, Please enter some text!")

def decode_message():
    try:
        decoded = lsb.reveal(file_path)
        text_box.delete(1.0, END)
        text_box.insert(END, decoded)
    except (NameError, IndexError):
        messagebox.showwarning("No Image", "Please open some encoded image!")

root = tk.Tk()
root.title("Steganography - Yagel Nahshon")
root.resizable(False, False)
center_window(root, 800, 800)

title_label = tk.Label(root, text="Steganography - Mini Project", font=("Arial", 20))
title_label.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

button1 = tk.Button(button_frame, text="Open Image", width=15, height=1, command=open_image)
button1.pack(side=tk.LEFT, padx=15)

button2 = tk.Button(button_frame, text="Save Image", width=15, height=1, command=save_image)
button2.pack(side=tk.LEFT, padx=15)

canvas_frame = tk.Frame(root)
canvas_frame.pack(pady=20)

canvas = tk.Canvas(canvas_frame, width=400, height=400, bg="lightgray")
canvas.pack(side=tk.LEFT, padx=10)

steg_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
steg_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

text_box = tk.Text(steg_frame, width=20, height=10)
text_box.insert("1.0","Enter your text here.")
text_box.pack(side=tk.LEFT, padx=(10, 5), pady=10, fill=tk.BOTH, expand=True)

enc_button = tk.Button(steg_frame, text="Encode", width=20, command=encode_message)
enc_button.pack(side=tk.TOP, padx=(5, 10), pady=50)

dec_button = tk.Button(steg_frame, text="Decode", width=20, command=decode_message)
dec_button.pack(side=tk.TOP, padx=(5, 10), pady=5)

root.mainloop()

