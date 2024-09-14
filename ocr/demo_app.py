import tkinter as tk
from tkinter import filedialog, Text, Label
from PIL import Image, ImageTk
from processing_script import *
from easyocr import Reader
import pytesseract
import cv2


def process_image(path):
    original_image = cv2.imread(path)
    processed_image = preprocess_image(path)
    reader = Reader(['en'])
    ez_original = reader.readtext(original_image)
    tess_original = pytesseract.image_to_string(original_image)
    ez_processed = reader.readtext(processed_image)
    tess_processed = pytesseract.image_to_string(processed_image)
    easyocr_original_text = ''
    for res in ez_original:
        easyocr_original_text += res[1] + '\n'
    tesseract_original_text = ''
    for line in tess_original.split('\n'):
        if not line == '':
            tesseract_original_text += line + '\n'
    easyocr_processed_text = ''
    for res in ez_processed:
        easyocr_processed_text += res[1] + '\n'
    tesseract_processed_text = ''
    for line in tess_processed.split('\n'):
        if not line == '':
            tesseract_processed_text += line + '\n'
    return easyocr_original_text, easyocr_processed_text, tesseract_original_text, tesseract_processed_text


def open_file():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All Files", "*.*"))
    )
    if file_path:
        output_text = process_image(file_path)
        text_box_easyocr_o.delete(1.0, tk.END)
        text_box_easyocr_o.insert(tk.END, output_text[0])

        text_box_easyocr_p.delete(1.0, tk.END)
        text_box_easyocr_p.insert(tk.END, output_text[1])

        text_box_tesseract_o.delete(1.0, tk.END)
        text_box_tesseract_o.insert(tk.END, output_text[2])

        text_box_tesseract_p.delete(1.0, tk.END)
        text_box_tesseract_p.insert(tk.END, output_text[3])

        img = Image.open(file_path)
        aspect_ratio = img.width / img.height
        if img.width > img.height:
            new_width = 300
            new_height = int(300 / aspect_ratio)
        else:
            new_width = int(300 * aspect_ratio)
            new_height = 300
        img = img.resize((new_width, new_height))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Image Processing App")

    open_button = tk.Button(root, text="Open Image", command=open_file)
    open_button.grid(row=0, column=1, padx=50, pady=20)

    image_label = Label(root)
    image_label.grid(row=0, column=2, padx=20, pady=20)

    text_box_easyocr_o = Text(root, wrap='word', height=37, width=50)
    text_box_easyocr_p = Text(root, wrap='word', height=37, width=50)
    text_box_tesseract_o = Text(root, wrap='word', height=37, width=50)
    text_box_tesseract_p = Text(root, wrap='word', height=37, width=50)

    label1 = tk.Label(root, text="EasyOCR Original Image")
    label2 = tk.Label(root, text="EasyOCR Preprocessed Image")
    label3 = tk.Label(root, text="Tesseract Original Image")
    label4 = tk.Label(root, text="Tesseract Preprocessed Image")

    label1.grid(row=1, column=0, padx=5)
    text_box_easyocr_o.grid(row=2, column=0, padx=5)

    label2.grid(row=1, column=1, padx=5)
    text_box_easyocr_p.grid(row=2, column=1, padx=5)

    label3.grid(row=1, column=2, padx=5)
    text_box_tesseract_o.grid(row=2, column=2, padx=5)

    label4.grid(row=1, column=3, padx=5)
    text_box_tesseract_p.grid(row=2, column=3, padx=5)

    root.mainloop()
