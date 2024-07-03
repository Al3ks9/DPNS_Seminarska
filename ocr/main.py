import cv2
import pytesseract


if __name__ == '__main__':
    img = cv2.imread("./images/image (1).png", cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    text = pytesseract.image_to_string(binary_image, lang='eng')

    print(text)

