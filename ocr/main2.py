import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from pytesseract import Output
import os

if __name__ == '__main__':
    source_folder = './images/'
    output_folder = './output_images/'
    text_output = open('tesseract_text_outputs.txt', 'w')

    image_files = [img for img in os.listdir(source_folder)]
    i = 0

    for image_file in image_files:
        print(i)
        i += 1
        path = source_folder + image_file
        img = cv2.imread(path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        d = pytesseract.image_to_data(gray, output_type=Output.DICT)
        n_boxes = len(d['level'])
        for k in range(n_boxes):
            (x, y, w, h) = (d['left'][k], d['top'][k], d['width'][k], d['height'][k])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)

        text = pytesseract.image_to_string(gray, lang='eng')
        image_id = os.path.basename(image_file)
        text_output.write(image_id + '\n')
        text_output.write(text)
        text_output.write('\n')
        cv2.imwrite(output_folder + image_id, img)

