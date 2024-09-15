from new_ids import ids
from easyocr import Reader
from processing_script import *
import cv2

if __name__ == '__main__':
    source_folder = './images/'
    overall_accuracy = 0
    i = 0
    reader = Reader(['en'])
    for image_id in ids:
        i += 1
        print(i)
        original = cv2.imread(source_folder + image_id + '.jpg')
        results_processed = reader.readtext(original)
        processed_text = process_easyocr_text(results_processed)
        true_text = process_true_text(image_id)
        accuracy = levenshtein_accuracy(processed_text, true_text)

        overall_accuracy += accuracy

    print(overall_accuracy / 423)
