import cv2
import pytesseract
from easyocr import Reader
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    print(np.__version__)
    img = cv2.imread("./images/00a66ef9770f9d2d.jpg")
    # _, binary_image = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    # for contour in contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # text = pytesseract.image_to_string(binary_image, lang='eng')
    reader = Reader(['en'])
    results = reader.readtext(img)
    for result in results:
        cv2.rectangle(img, result[0][0], result[0][2], (0, 255, 0), 5)
        print(f'Text: {result[1]}, Confidence: {result[2]:.2f}')

    plt.imshow(img)
    plt.show()

    # print(text)


