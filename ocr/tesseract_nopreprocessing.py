import pytesseract
from new_ids import ids
from processing_script import *
import cv2

if __name__ == '__main__':
    source_folder = './images/'
    overall_accuracy = 0
    i = 0
    for image_id in ids:
        print(i)
        i += 1
        original = cv2.imread(source_folder + image_id + '.jpg')
        true_text = process_true_text(image_id)
        output_text_processed = pytesseract.image_to_string(original)
        processed_text = process_tesseract_text(output_text_processed)
        accuracy = levenshtein_accuracy(processed_text, true_text)

        overall_accuracy += accuracy

    print(overall_accuracy / 423)
