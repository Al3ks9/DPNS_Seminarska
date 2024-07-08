import cv2
import pytesseract
from easyocr import Reader
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    img = cv2.imread("./images/00a0db6495982c1d.jpg")
    reader = Reader(['en'])
    results = reader.readtext(img)
    print(results)
    for result in results:
        bbox = result[0]
        top_left = tuple((int(i) for i in bbox[0]))
        bottom_right = tuple((int(i) for i in bbox[2]))
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 5)
        print(f'Text: {result[1]}, Confidence: {result[2]:.2f}')

    plt.imshow(img)
    plt.show()


