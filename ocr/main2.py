import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from pytesseract import Output

if __name__ == '__main__':
    img = cv2.imread("./images/00a2ac61646c039e.jpg")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    d = pytesseract.image_to_data(gray, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)

    text = pytesseract.image_to_string(gray, lang='eng')

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    print(text)
