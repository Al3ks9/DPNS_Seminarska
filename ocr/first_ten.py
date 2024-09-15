import os
from easyocr import Reader
from processing_script import *
import pytesseract

if __name__ == '__main__':
    ids = [id.split("_")[2] for id in os.listdir('./compare_images_pairs')]
    source_folder = './images/'
    i = 0
    ez_acc = 0
    ts_acc = 0
    reader = Reader(["en"])
    for id in ids[:10]:
        print(i)
        i += 1
        image = cv2.imread(source_folder + id)
        easyocr_results = reader.readtext(image)
        easyocr_text = process_easyocr_text(easyocr_results)
        tesseract_results = pytesseract.image_to_string(image)
        tesseract_text = process_tesseract_text(tesseract_results)
        true_text = process_true_text(id.split('.')[0])
        ez_acc += levenshtein_accuracy(easyocr_text, true_text)
        ts_acc += levenshtein_accuracy(tesseract_text, true_text)

    print("Ez: " + str(ez_acc))
    print("Tess: " + str(ts_acc))
